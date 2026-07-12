# Vibe Code Starter — `.claude/` Configuration

This directory is the portable agent config that ships with the starter template.
It is a **reference for setup**, not a live per-project configuration — the first time
you open the template, an agent reads [`setup.md`](../setup.md) and uses the files here
to bootstrap your project.

## Source of truth: `setup.config.json`

All setup decisions are declared in **[`setup.config.json`](setup.config.json)**. Edit
that file to change what the template installs; [`setup.md`](../setup.md) reads it and
[`CLAUDE.md`](../CLAUDE.md) documents the result. Its sections:

| Key | What it declares |
| --- | --- |
| `marketplaces` | Plugin marketplaces to add (`vibe-code-starter` local + `karimo` GitHub) |
| `plugins.required` / `plugins.optional` | Plugins to install, and from which marketplace |
| `outputStyles` | Output-style plugins delivered as skills-dir plugins |
| `skills` | Auto-loading `SKILL.md` skills that must be present |
| `brand` | The user's brand identity (filled in during setup) |
| `files` | Where the guide/config files live |
| `state` | Idempotency flags updated as each setup phase completes |

## What gets set up

### Plugins  → installed from a marketplace

Vendored under `plugins/` and inert until installed. `setup.md` adds the **local
marketplace** ([`../.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json))
and installs them by name.

**Required:** `agent-sdk-dev` · `code-review` · `commit-commands` · `feature-dev` ·
`hookify` · `plugin-dev` · `karimo` *(from `opensesh/KARIMO`)*
**Optional:** `ralph-wiggum` · `pr-review-toolkit`

### Skills  → auto-load at project scope

Live under `skills/` and load automatically once the workspace is trusted — no install.

**Required:** `bos-code-quality` · `brand-guidelines` · `frontend-design` ·
`incremental-commits` · `security-guidance` · `subagent-driven-development` ·
`systematic-debugging` · `verification-before-completion` · `writing-plans`

### Output styles  → skills-dir plugins

`learning-output-style` (required) and `explanatory-output-style` (optional) live under
`skills/` but are plugins (they have `.claude-plugin/plugin.json` + hooks). They auto-load
with the other skills-dir entries after trust + `/reload-plugins`.

### Brand identity

`brand-guidelines` and `brand/` ship as **placeholder templates** (`<PLACEHOLDER>`
fields, no real brand). Setup interviews you and fills them in for **your** brand, then
sets `brand.configured = true`.

## Directory map

```
.claude/
├── README.md            # This file — config documentation
├── setup.config.json    # Source of truth (edit this)
├── claude.md            # Thin pointer to root CLAUDE.md (no project content)
├── settings.json        # Permissions
├── plugins/             # Vendored plugins (install via local marketplace)
├── skills/              # Auto-loading skills + output-style plugins
├── commands/            # Slash commands
├── brand/               # Brand identity & writing guides
└── reference/           # Design-system reference

../.claude-plugin/marketplace.json   # Local marketplace manifest
../setup.md                          # The setup runbook
../CLAUDE.md  ../AGENTS.md           # Agent guides (AGENTS.md → CLAUDE.md)
```

## Running / re-running setup

Tell your agent: **"follow setup.md"**. It is idempotent — it health-checks first and
only changes what's missing, asking approval before installing anything. See
[`setup.md`](../setup.md) for the full phased runbook and a command quick-reference.
