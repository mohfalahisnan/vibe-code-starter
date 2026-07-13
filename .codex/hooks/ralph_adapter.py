#!/usr/bin/env python3
"""Portable Codex bridge for the vendored Ralph Wiggum loop."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = REPO_ROOT / ".claude" / "ralph-loop.local.md"
HELP = """Ralph Loop - interactive self-referential development loop

Usage:
  $ralph-loop PROMPT [--max-iterations N] [--completion-promise TEXT]

The Codex adapter shares `.claude/ralph-loop.local.md` with Claude Code.
Completion requires `<promise>TEXT</promise>` with an exact, truthful promise.
"""


def normalized_text(value: str) -> str:
    return " ".join(value.split())


def parse_state(path: Path | None = None) -> dict[str, Any]:
    if path is None:
        path = STATE_FILE
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$", content)
    if not match:
        raise ValueError("missing YAML frontmatter")

    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip()

    try:
        iteration = int(frontmatter["iteration"])
        max_iterations = int(frontmatter["max_iterations"])
    except (KeyError, ValueError) as error:
        raise ValueError("iteration fields are invalid") from error
    if iteration < 1 or max_iterations < 0:
        raise ValueError("iteration fields are out of range")

    raw_promise = frontmatter.get("completion_promise", "null")
    if raw_promise in {"", "null", "~"}:
        completion_promise = None
    else:
        try:
            completion_promise = json.loads(raw_promise)
        except json.JSONDecodeError:
            completion_promise = raw_promise.strip('"').strip("'")

    prompt = match.group(2).strip()
    if not prompt:
        raise ValueError("prompt is empty")
    started_at = frontmatter.get("started_at", "")
    if started_at.startswith('"') and started_at.endswith('"'):
        try:
            started_at = json.loads(started_at)
        except json.JSONDecodeError:
            started_at = started_at.strip('"')

    return {
        "iteration": iteration,
        "max_iterations": max_iterations,
        "completion_promise": completion_promise,
        "started_at": started_at,
        "prompt": prompt,
    }


def render_state(state: dict[str, Any]) -> str:
    promise = state.get("completion_promise")
    promise_yaml = "null" if promise is None else json.dumps(str(promise), ensure_ascii=False)
    started_at = state.get("started_at") or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return (
        "---\n"
        "active: true\n"
        f"iteration: {state['iteration']}\n"
        f"max_iterations: {state['max_iterations']}\n"
        f"completion_promise: {promise_yaml}\n"
        f"started_at: \"{started_at}\"\n"
        "---\n\n"
        f"{state['prompt']}\n"
    )


def write_state(state: dict[str, Any], path: Path | None = None) -> None:
    if path is None:
        path = STATE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    temporary.write_text(render_state(state), encoding="utf-8")
    os.replace(temporary, path)


def parse_start_arguments(arguments: list[str]) -> dict[str, Any]:
    prompt_parts: list[str] = []
    max_iterations = 0
    completion_promise: str | None = None
    index = 0
    while index < len(arguments):
        item = arguments[index]
        if item == "--":
            index += 1
            continue
        if item in {"-h", "--help"}:
            return {"help": True}
        if item == "--max-iterations":
            if index + 1 >= len(arguments) or not arguments[index + 1].isdigit():
                raise ValueError("--max-iterations requires a positive integer or 0")
            max_iterations = int(arguments[index + 1])
            index += 2
            continue
        if item == "--completion-promise":
            if index + 1 >= len(arguments):
                raise ValueError("--completion-promise requires text")
            completion_promise = arguments[index + 1]
            index += 2
            continue
        prompt_parts.append(item)
        index += 1

    prompt = " ".join(prompt_parts).strip()
    if not prompt:
        raise ValueError("Ralph needs a task prompt")
    return {
        "help": False,
        "prompt": prompt,
        "max_iterations": max_iterations,
        "completion_promise": completion_promise,
    }


def start(arguments: list[str]) -> int:
    try:
        options = parse_start_arguments(arguments)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    if options["help"]:
        print(HELP)
        return 0

    state = {
        "iteration": 1,
        "max_iterations": options["max_iterations"],
        "completion_promise": options["completion_promise"],
        "started_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "prompt": options["prompt"],
    }
    write_state(state)
    maximum = state["max_iterations"] or "unlimited"
    promise = state["completion_promise"] or "none"
    print(f"Ralph loop activated. Iteration: 1; max: {maximum}; completion promise: {promise}")
    print(state["prompt"])
    return 0


def cancel() -> int:
    if not STATE_FILE.exists():
        print("No active Ralph loop found.")
        return 0
    try:
        iteration = parse_state()["iteration"]
    except ValueError:
        iteration = "unknown"
    STATE_FILE.unlink()
    print(f"Cancelled Ralph loop (was at iteration {iteration}).")
    return 0


def stop() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if not STATE_FILE.exists():
        return 0

    try:
        state = parse_state()
    except ValueError as error:
        print(f"Ralph loop state is invalid ({error}); stopping loop.", file=sys.stderr)
        STATE_FILE.unlink(missing_ok=True)
        return 0

    if state["max_iterations"] > 0 and state["iteration"] >= state["max_iterations"]:
        print(f"Ralph loop reached max iterations ({state['max_iterations']}).", file=sys.stderr)
        STATE_FILE.unlink(missing_ok=True)
        return 0

    last_message = str(payload.get("last_assistant_message") or "")
    promise = state["completion_promise"]
    if promise:
        match = re.search(r"<promise>([\s\S]*?)</promise>", last_message)
        if match and normalized_text(match.group(1)) == normalized_text(str(promise)):
            print(f"Ralph loop completion promise detected: {promise}", file=sys.stderr)
            STATE_FILE.unlink(missing_ok=True)
            return 0

    state["iteration"] += 1
    write_state(state)
    if promise:
        system_message = (
            f"Ralph iteration {state['iteration']} | To stop: output <promise>{promise}</promise> "
            "only when the statement is true."
        )
    else:
        system_message = f"Ralph iteration {state['iteration']} | No completion promise; loop continues."
    print(
        json.dumps(
            {
                "decision": "block",
                "reason": state["prompt"],
                "systemMessage": system_message,
            }
        )
    )
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(HELP, file=sys.stderr)
        return 2
    command = sys.argv[1]
    if command == "start":
        return start(sys.argv[2:])
    if command == "cancel":
        return cancel()
    if command == "stop":
        return stop()
    if command in {"help", "--help", "-h"}:
        print(HELP)
        return 0
    print(f"Unknown Ralph adapter command: {command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
