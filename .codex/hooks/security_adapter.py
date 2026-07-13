#!/usr/bin/env python3
"""Feed Codex apply_patch edits through the canonical Claude security hook."""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_HOOK = REPO_ROOT / ".claude" / "skills" / "security-guidance" / "hooks" / "security_reminder_hook.py"


def patch_changes(patch: str) -> list[tuple[str, str]]:
    """Extract target paths and added content from apply_patch or unified diff text."""
    changes: dict[str, list[str]] = {}
    current_path: str | None = None

    for line in patch.splitlines():
        file_header = re.match(r"^\*\*\* (?:Add|Update|Delete) File:\s*(.+)$", line)
        if file_header:
            current_path = file_header.group(1).strip()
            changes.setdefault(current_path, [])
            continue

        unified_header = re.match(r"^\+\+\+\s+(?:b/)?(.+)$", line)
        if unified_header and unified_header.group(1) != "/dev/null":
            current_path = unified_header.group(1).strip()
            changes.setdefault(current_path, [])
            continue

        if current_path and line.startswith("+") and not line.startswith("+++"):
            changes[current_path].append(line[1:])

    return [(file_path, "\n".join(content)) for file_path, content in changes.items()]


def run_canonical(payload: dict[str, Any]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CANONICAL_HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=REPO_ROOT,
        env=os.environ.copy(),
        check=False,
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if payload.get("tool_name") != "apply_patch":
        process = run_canonical(payload)
        if process.returncode == 2:
            print(process.stderr, file=sys.stderr, end="")
            return 2
        return 0

    tool_input = payload.get("tool_input", {})
    patch = tool_input.get("command") or tool_input.get("patch") or ""
    for file_path, added_content in patch_changes(patch):
        translated = copy.deepcopy(payload)
        translated["codex_tool_name"] = "apply_patch"
        translated["tool_name"] = "Edit"
        translated["tool_input"] = {
            **tool_input,
            "file_path": file_path,
            "new_string": added_content,
        }
        process = run_canonical(translated)
        if process.returncode == 2:
            print(process.stderr, file=sys.stderr, end="")
            return 2
        if process.returncode != 0 and process.stderr:
            print(f"Security adapter failed open: {process.stderr.strip()}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
