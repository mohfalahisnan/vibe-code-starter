# <PROJECT_NAME> — Agent Development Guide

> Canonical guidance for AI coding agents (Claude Code, Codex) working in this repo.
> `AGENTS.md` points here so every agent reads the same guide. Fill in the
> `<PLACEHOLDER>` fields during **Phase 5** of [`setup.md`](setup.md).

## First-time setup

If this template hasn't been set up yet (`.claude/setup.config.json` →
`state.setupCompleted` is `false`), **follow [`setup.md`](setup.md)** before doing
feature work. It installs the curated plugins, verifies skills, configures the brand,
and initializes these guide files.

## Project overview

<ONE_PARAGRAPH: what this project is and who it's for.>

## Tech stack

- **Framework**: <e.g. Next.js / none yet>
- **Language**: <e.g. TypeScript>
- **Styling**: <e.g. Tailwind CSS>
- **Other**: <libraries, tooling>

## Essential commands

```bash
<npm run dev>      # start dev server
<npm run build>    # production build
<npm run lint>     # lint
<npm test>         # tests
```

## Conventions

- **File/code hygiene**: the `codebase-structure` skill is authoritative — reuse before
  creating, classify (page vs component, global vs feature-specific, frontend vs backend),
  place correctly, promote on second use.
- <other coding conventions the agent must follow>
- <naming, testing expectations>

## Agent configuration

This repo ships a curated `.claude/` config. See:

| Path | Purpose |
| --- | --- |
| [`setup.md`](setup.md) | First-load setup runbook |
| [`.claude/setup.config.json`](.claude/setup.config.json) | Source of truth: plugins, skills, brand |
| [`.claude/README.md`](.claude/README.md) | Config documentation |
| `.claude/skills/` | Auto-loading skills (incl. `brand-guidelines`) |
| `.claude/plugins/` | Vendored plugins (install via the local marketplace) |
| `.claude/brand/` | Brand identity & writing guides |
| [`.agents/capability-map.json`](.agents/capability-map.json) | Generated Claude → Codex capability mapping |
| `.agents/skills/` | Generated Codex skill/command adapters |
| `.codex/agents/` · [`.codex/hooks.json`](.codex/hooks.json) | Codex agent and hook adapters |

### Installed capabilities (after setup)

- **Plugins**: agent-sdk-dev, code-review, commit-commands, feature-dev, hookify,
  plugin-dev, karimo (+ optional: ralph-wiggum, pr-review-toolkit)
- **Skills**: bos-code-quality, brand-guidelines, codebase-structure, frontend-design,
  incremental-commits, security-guidance, subagent-driven-development, systematic-debugging,
  verification-before-completion, writing-plans
- **Output styles**: learning-output-style (+ optional: explanatory-output-style)

Claude Code invokes commands with `/name`; Codex invokes the mapped project skill with
`$name`. Both read the same canonical source under `.claude/`. Codex KARIMO comes from
the native machine plugin and is never copied from the Claude command files.

## Validation

Before claiming a task is done, run the project's checks and confirm the output:

```bash
<npm run build>
<npm run lint>
node scripts/sync-agent-adapters.mjs --check --machine
```

## Instruction precedence

When instructions conflict, follow this order (highest first):

1. Direct user instructions in chat
2. This file (`CLAUDE.md`)
3. Harness-level user guidance (`~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`)
4. Skills (auto-activated, supplement the above)
