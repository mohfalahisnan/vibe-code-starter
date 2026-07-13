# Claude-to-Codex Compatibility Contract

`.claude/` is the canonical behavior source for this repository. Generated Codex
adapters under `.agents/skills/` and `.codex/agents/` must read that source and keep
the same workflow order, approval gates, safety rules, and verification standard.

Only platform syntax changes:

| Claude Code surface | Codex surface |
| --- | --- |
| Slash command `/name args` | Project skill `$name args` |
| `Read`, `Glob`, `Grep` | Available read/search tools; prefer `rg` for repository search |
| `Bash` | Shell command tool for the current platform |
| `Write`, `Edit`, `MultiEdit` | `apply_patch` for intentional file edits |
| `Task` / named plugin agent | Codex agent with the namespaced entry in `.codex/agents/` |
| `AskUserQuestion` | Codex user-input tool when available, otherwise one concise question |
| `${CLAUDE_PLUGIN_ROOT}` | The matching canonical directory under `<repo>/.claude/plugins/` |
| Claude plugin hook input | Native Codex hook input normalized by `.codex/hooks/` adapters |

Rules:

1. Resolve `<repo>` with `git rev-parse --show-toplevel`; never store a machine-specific
   absolute path in a generated adapter.
2. Read the canonical source completely before executing its workflow. Resolve linked
   files relative to the source skill or plugin directory unless it explicitly says otherwise.
3. Preserve user arguments and intent. Do not silently skip a phase because a Claude
   tool name differs.
4. Agent names are namespaced in Codex to prevent collisions. Find the exact mapping in
   `.agents/capability-map.json`.
5. KARIMO is an exception to generated wrappers: Codex uses the native `karimo` plugin
   on the machine. The parity checker verifies its installed version without recording
   its absolute path.
6. Direct user/system instructions and repository `AGENTS.md` constraints still win.
7. Change canonical behavior in `.claude/` once, then run:

   ```bash
   node scripts/sync-agent-adapters.mjs --write
   node scripts/sync-agent-adapters.mjs --check --machine
   ```

Do not hand-edit generated adapters. A stale or unmapped Claude capability is a failed
parity check, not an accepted platform difference.
