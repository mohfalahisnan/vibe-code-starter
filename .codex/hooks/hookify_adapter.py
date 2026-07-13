#!/usr/bin/env python3
"""Translate native Codex hook payloads to the vendored Hookify implementation."""

from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPO_ROOT / ".claude" / "plugins" / "hookify"
EVENT_FILES = {
    "pretooluse": ("PreToolUse", "pretooluse.py"),
    "posttooluse": ("PostToolUse", "posttooluse.py"),
    "stop": ("Stop", "stop.py"),
    "userpromptsubmit": ("UserPromptSubmit", "userpromptsubmit.py"),
}


def added_patch_content(patch: str) -> str:
    """Return added lines so Claude file rules see Edit.new_string semantics."""
    return "\n".join(
        line[1:]
        for line in patch.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def first_patch_path(patch: str) -> str:
    patterns = (
        r"^\*\*\* (?:Add|Update|Delete) File:\s*(.+)$",
        r"^\+\+\+\s+(?:b/)?(.+)$",
    )
    for pattern in patterns:
        match = re.search(pattern, patch, flags=re.MULTILINE)
        if match and match.group(1) != "/dev/null":
            return match.group(1).strip()
    return ""


def normalize_payload(payload: dict[str, Any], event_name: str) -> dict[str, Any]:
    normalized = copy.deepcopy(payload)
    normalized.setdefault("hook_event_name", event_name)

    if event_name == "UserPromptSubmit" and "user_prompt" not in normalized:
        normalized["user_prompt"] = normalized.get("prompt", "")

    tool_name = normalized.get("tool_name", "")
    tool_input = normalized.setdefault("tool_input", {})
    if tool_name == "apply_patch":
        patch = tool_input.get("command") or tool_input.get("patch") or ""
        normalized["codex_tool_name"] = tool_name
        normalized["tool_name"] = "Edit"
        tool_input.setdefault("file_path", first_patch_path(patch))
        tool_input.setdefault("new_string", added_patch_content(patch))
        tool_input.setdefault("content", tool_input.get("new_string", ""))
    elif tool_name == "shell_command":
        normalized["codex_tool_name"] = tool_name
        normalized["tool_name"] = "Bash"

    if event_name == "Stop" and "reason" not in normalized:
        normalized["reason"] = normalized.get("last_assistant_message", "")

    return normalized


def adapt_result(event_name: str, result: dict[str, Any]) -> dict[str, Any]:
    hook_output = result.get("hookSpecificOutput")
    if not isinstance(hook_output, dict) or hook_output.get("permissionDecision") != "deny":
        return result

    message = result.get("systemMessage") or "Blocked by a Hookify rule."
    if event_name == "PreToolUse":
        hook_output["hookEventName"] = "PreToolUse"
        hook_output["permissionDecisionReason"] = message
        return result
    if event_name == "PostToolUse":
        return {"decision": "block", "reason": message, "systemMessage": message}
    return result


def evaluate(event_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    event_name, script_name = EVENT_FILES[event_key]
    normalized = normalize_payload(payload, event_name)
    temporary_transcript: str | None = None

    if event_name == "Stop" and not normalized.get("transcript_path") and normalized.get("last_assistant_message"):
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False)
        handle.write(str(normalized["last_assistant_message"]))
        handle.close()
        temporary_transcript = handle.name
        normalized["transcript_path"] = temporary_transcript

    environment = os.environ.copy()
    environment["CLAUDE_PLUGIN_ROOT"] = str(PLUGIN_ROOT)
    try:
        process = subprocess.run(
            [sys.executable, str(PLUGIN_ROOT / "hooks" / script_name)],
            input=json.dumps(normalized),
            text=True,
            capture_output=True,
            cwd=REPO_ROOT,
            env=environment,
            check=False,
        )
    finally:
        if temporary_transcript:
            try:
                Path(temporary_transcript).unlink()
            except OSError:
                pass

    if process.stderr:
        print(process.stderr, file=sys.stderr, end="")
    if process.returncode != 0:
        return {"systemMessage": f"Hookify adapter failed open (exit {process.returncode})."}

    try:
        result = json.loads(process.stdout.strip() or "{}")
    except json.JSONDecodeError:
        return {"systemMessage": "Hookify adapter received invalid canonical hook output; operation allowed."}
    return adapt_result(event_name, result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("event", choices=EVENT_FILES)
    options = parser.parse_args()
    try:
        payload = json.load(sys.stdin)
        result = evaluate(options.event, payload)
        print(json.dumps(result))
    except Exception as error:  # Fail open, matching the canonical Hookify hooks.
        print(json.dumps({"systemMessage": f"Hookify adapter error: {error}"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
