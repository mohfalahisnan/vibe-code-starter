# AGENTS.md

This project's agent guidance lives in **[`CLAUDE.md`](CLAUDE.md)** — read it first.
`AGENTS.md` exists only so Codex and other agents that look for `AGENTS.md` find the
same guide, without duplicating content.

## Setup

If the template hasn't been bootstrapped yet, follow **[`setup.md`](setup.md)**.

## Shared Claude/Codex behavior

`.claude/` is the canonical behavior source. Codex loads generated project adapters
from `.agents/skills/`, `.codex/agents/`, and `.codex/hooks.json`; do not maintain a
second copy of the workflows by hand.

After changing any Claude skill, command, agent, hook, or vendored plugin, run:

```bash
node scripts/sync-agent-adapters.mjs --write
node scripts/sync-agent-adapters.mjs --check --machine
```

KARIMO is not copied from `.claude/commands/karimo/`. Codex uses the machine's native
`karimo` plugin, whose presence and version are checked by the parity script. Full
mapping lives in [`.agents/capability-map.json`](.agents/capability-map.json).

---

➡️ **Full guide: [`CLAUDE.md`](CLAUDE.md)**
