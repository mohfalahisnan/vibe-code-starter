#!/usr/bin/env python3
"""Load Codex SessionStart context directly from the canonical Claude handler."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
VALID_MODES = {"learning", "explanatory"}


def canonical_context(mode: str) -> dict:
    handler = REPO_ROOT / ".claude" / "skills" / f"{mode}-output-style" / "hooks-handlers" / "session-start.sh"
    content = handler.read_text(encoding="utf-8")
    match = re.search(r"cat\s+<<\s*['\"]?EOF['\"]?\r?\n([\s\S]*?)\r?\nEOF", content)
    if not match:
        raise ValueError(f"Cannot extract canonical output style from {handler}")
    return json.loads(match.group(1))


def main() -> int:
    mode = os.environ.get("CODEX_OUTPUT_STYLE", "learning").strip().lower()
    if mode in {"none", "off", "disabled"}:
        return 0
    if mode not in VALID_MODES:
        print(f"Unknown CODEX_OUTPUT_STYLE={mode!r}; using learning.", file=sys.stderr)
        mode = "learning"
    print(json.dumps(canonical_context(mode)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
