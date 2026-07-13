#!/usr/bin/env python3
"""Unit tests for platform translation that must not change canonical Claude assets."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / ".codex" / "hooks"))

import hookify_adapter  # noqa: E402
import ralph_adapter  # noqa: E402
import security_adapter  # noqa: E402
import session_context  # noqa: E402


class AdapterTests(unittest.TestCase):
    def test_hookify_normalizes_apply_patch(self) -> None:
        payload = {
            "tool_name": "apply_patch",
            "tool_input": {
                "command": "*** Begin Patch\n*** Update File: src/app.js\n+eval(input)\n*** End Patch"
            },
        }
        normalized = hookify_adapter.normalize_payload(payload, "PreToolUse")
        self.assertEqual(normalized["tool_name"], "Edit")
        self.assertEqual(normalized["tool_input"]["file_path"], "src/app.js")
        self.assertEqual(normalized["tool_input"]["new_string"], "eval(input)")

    def test_hookify_translates_blocking_output(self) -> None:
        canonical = {
            "hookSpecificOutput": {"permissionDecision": "deny"},
            "systemMessage": "blocked",
        }
        pre = hookify_adapter.adapt_result("PreToolUse", canonical)
        self.assertEqual(pre["hookSpecificOutput"]["permissionDecisionReason"], "blocked")
        post = hookify_adapter.adapt_result("PostToolUse", canonical)
        self.assertEqual(post["decision"], "block")
        self.assertEqual(post["reason"], "blocked")

    def test_security_extracts_each_changed_file(self) -> None:
        patch_text = (
            "*** Begin Patch\n"
            "*** Update File: src/a.js\n"
            "+eval(input)\n"
            "*** Add File: src/b.js\n"
            "+safe()\n"
            "*** End Patch"
        )
        self.assertEqual(
            security_adapter.patch_changes(patch_text),
            [("src/a.js", "eval(input)"), ("src/b.js", "safe()")],
        )

    def test_security_bridge_blocks_canonical_warning(self) -> None:
        payload = {
            "session_id": "adapter-test",
            "tool_name": "apply_patch",
            "tool_input": {
                "command": "*** Begin Patch\n*** Update File: src/a.js\n+eval(input)\n*** End Patch"
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            stderr = StringIO()
            with (
                patch.object(sys, "stdin", StringIO(json.dumps(payload))),
                patch.dict(os.environ, {"HOME": directory, "USERPROFILE": directory}),
                redirect_stderr(stderr),
            ):
                result = security_adapter.main()
        self.assertEqual(result, 2)
        self.assertIn("eval()", stderr.getvalue())

    def test_session_context_comes_from_canonical_handler(self) -> None:
        payload = session_context.canonical_context("learning")
        self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("learning", payload["hookSpecificOutput"]["additionalContext"].lower())

    def test_ralph_state_round_trip(self) -> None:
        state = {
            "iteration": 2,
            "max_iterations": 5,
            "completion_promise": "DONE: true",
            "started_at": "2026-01-01T00:00:00Z",
            "prompt": "Fix the bug",
        }
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "ralph.md"
            ralph_adapter.write_state(state, target)
            self.assertEqual(ralph_adapter.parse_state(target), state)

    def test_ralph_argument_parity(self) -> None:
        parsed = ralph_adapter.parse_start_arguments(
            ["Fix", "auth", "--max-iterations", "3", "--completion-promise", "DONE"]
        )
        self.assertEqual(parsed["prompt"], "Fix auth")
        self.assertEqual(parsed["max_iterations"], 3)
        self.assertEqual(parsed["completion_promise"], "DONE")

    def test_ralph_stop_bridge_continues_then_completes(self) -> None:
        state = {
            "iteration": 1,
            "max_iterations": 5,
            "completion_promise": "DONE",
            "started_at": "2026-01-01T00:00:00Z",
            "prompt": "Finish task",
        }
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "ralph.md"
            with patch.object(ralph_adapter, "STATE_FILE", target):
                ralph_adapter.write_state(state)
                stdout = StringIO()
                with (
                    patch.object(sys, "stdin", StringIO(json.dumps({"last_assistant_message": "working"}))),
                    redirect_stdout(stdout),
                ):
                    self.assertEqual(ralph_adapter.stop(), 0)
                response = json.loads(stdout.getvalue())
                self.assertEqual(response["decision"], "block")
                self.assertEqual(ralph_adapter.parse_state()["iteration"], 2)

                with (
                    patch.object(
                        sys,
                        "stdin",
                        StringIO(json.dumps({"last_assistant_message": "<promise>DONE</promise>"})),
                    ),
                    redirect_stderr(StringIO()),
                ):
                    self.assertEqual(ralph_adapter.stop(), 0)
                self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
