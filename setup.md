# Setup Runbook

> **You are an AI coding agent (Claude Code or Codex). A user has just opened this
> starter template and asked you to set it up.** Follow this runbook top to bottom.
> It is a *reference for setup*, not a description of an already-configured project.

The single source of truth is **[`.claude/setup.config.json`](.claude/setup.config.json)**.
Everything below reads from it. Human-readable docs for that config live in
**[`.claude/README.md`](.claude/README.md)**.

---

## When to run this

- The **first time** the template is opened in a new project, or
- Whenever the user says "run setup", "set up the template", "bootstrap", or similar.

It is **idempotent** — safe to re-run. Each phase checks current state before acting
and updates the `state` flags in the config when it finishes.

## Ground rules for the agent

1. **Ask before every side effect.** Installing plugins, adding marketplaces, and
   editing standing config all require the user's explicit approval. Present the
   exact command, wait for a clear "yes", then run it. Never install silently.
2. **Read `.claude/setup.config.json` first** and treat its `required` / `optional`
   lists as authoritative. If this runbook and the config ever disagree, the config wins.
3. **Report, don't assume.** After each phase, show the user what changed and what is
   still missing. Do not claim success without running the verification command.
4. **Codex users:** you have no plugin marketplace. Do Phase 3–6 only, and read the
   [Codex notes](#codex-notes) at the end.

---

## Phase 0 — Load config & detect environment

1. Read `.claude/setup.config.json`.
2. Detect the harness:
   - **Claude Code** if the `claude` CLI is available (`claude --version`).
   - **Codex** otherwise (or if the user says so).
3. Confirm the workspace is **trusted**. In Claude Code, project-scope skills and
   skills-dir plugins under `.claude/skills/` only load after the trust dialog is
   accepted. If untrusted, tell the user to accept trust, then continue.

Summarize to the user: harness detected, whether this looks like a first run
(`state.setupCompleted === false`), and the plan (Phases 1–6).

---

## Phase 1 — Health check (report only, no changes)

Gather the current state. **Run these read-only commands and report a table.**

**Marketplaces**
```bash
claude plugin marketplace list
```
Check whether each entry in `config.marketplaces[].name` is already configured.

**Plugins**
```bash
claude plugin list --json
```
For each `config.plugins.required[]` and `config.plugins.optional[]`, mark:
`installed & enabled` / `installed but disabled` / `missing`.

**Output styles** (skills-dir plugins) — they appear under
"Skills-directory plugins" in `claude plugin list`. For each in
`config.outputStyles`, mark loaded / not loaded.

**Skills** — verify each `config.skills.required[]` directory exists and has a
`SKILL.md`:
```bash
ls .claude/skills
```
Skills auto-load at project scope, so "present + workspace trusted" = healthy.

Present a single **health report** (✔ ok / ⚠ disabled / ✘ missing) covering marketplaces,
required plugins, optional plugins, output styles, and required skills. Then move on.

---

## Phase 2 — Install marketplaces & plugins (needs approval)

Only for items the health check flagged as missing. **Ask before each group.**

### 2a. Add marketplaces

For every marketplace in `config.marketplaces` not already configured, propose its
`add` command. The two shipped with this template:

```bash
# Local marketplace — bundles the plugins vendored in .claude/plugins/ (offline, self-contained)
claude plugin marketplace add .

# KARIMO — external GitHub marketplace
claude plugin marketplace add opensesh/KARIMO
```

Verify with `claude plugin marketplace list`.

### 2b. Install required plugins

For each missing `config.plugins.required[]`, install from its marketplace at user scope:

```bash
claude plugin install agent-sdk-dev@vibe-code-starter
claude plugin install code-review@vibe-code-starter
claude plugin install commit-commands@vibe-code-starter
claude plugin install feature-dev@vibe-code-starter
claude plugin install hookify@vibe-code-starter
claude plugin install plugin-dev@vibe-code-starter
claude plugin install karimo@karimo
```

### 2c. Offer optional plugins

List `config.plugins.optional[]` and let the user pick. Install only what they choose:

```bash
claude plugin install ralph-wiggum@vibe-code-starter
claude plugin install pr-review-toolkit@vibe-code-starter
```

### 2d. Apply & verify

Plugins load on restart. Ask the user to run `/reload-plugins` (or relaunch), then
re-run `claude plugin list` and confirm every required plugin is **enabled**. Set
`state.pluginsInstalled = true` in the config once confirmed.

> If a `claude plugin install` fails, do **not** retry blindly. Report the error,
> check `claude plugin marketplace list`, and confirm the marketplace was added first.

---

## Phase 3 — Verify skills & output styles

These are vendored under `.claude/skills/` and **auto-load** — no install, just trust + reload.

1. Confirm every `config.skills.required[]` dir exists with a `SKILL.md`.
2. Confirm `config.outputStyles.required[]` (learning-output-style) and any opted-in
   optional ones are present.
3. If the workspace was just trusted, have the user run `/reload-plugins`.
4. Re-run `claude plugin list` and confirm the skills-dir plugins show as **loaded**.

Report which skills/output-styles are active. Do not proceed to brand setup until
required skills are confirmed present.

---

## Phase 4 — Configure brand identity (needs user input)

The vendored **brand-guidelines** skill, the `.claude/brand/` docs, and
`.claude/reference/design-system.md` all ship as **placeholder templates** —
`<PLACEHOLDER>` and `<COLOR_*>` / `<FONT_*>` fields, no real brand. Fill them in with
the user's own brand. (Do not apply the placeholder values literally before this.)

1. If `config.brand.configured === true`, skip unless the user asks to redo it.
2. **Interview** the user for the fields in `config.brand.identity`:
   - Company / product name and tagline
   - Colors: **primary**, **background**, **accent** (hex). Remind them of the ratio
     rule: primary + background ≈ 45–50% each, **accent max 10%**.
   - Typography: display, body, mono font families
   - Tone / personality (a sentence or two)
3. **Write the values** into `config.brand.identity` in `.claude/setup.config.json`.
4. **Fill in the placeholders** in `.claude/skills/brand-guidelines/SKILL.md` — replace
   `<COMPANY_NAME>`, `<COLOR_*>`, `<FONT_*>`, `<TONE>`, etc. with the user's values.
   Keep the frontmatter `name: brand-guidelines`; update its `description` to name the
   brand and drop the "template" note once configured.
5. **Fill in the placeholders** in `.claude/brand/**` (identity + writing templates) and
   `.claude/reference/design-system.md` (`<PROJECT>`, `<COLOR_*>`, `<FONT_*>`). If the
   user has their own brand docs, offer to drop them in instead.
6. Set `config.brand.configured = true` and `state.brandConfigured = true`.

Show a before/after of the key brand values and confirm with the user.

---

## Phase 5 — Initialize CLAUDE.md & AGENTS.md

1. **`CLAUDE.md`** (repo root) is the project guide. It ships as a generic template
   with `<PLACEHOLDER>` fields. Fill in project name, stack, commands, and conventions
   from what the user tells you (or from the codebase once they add one).
2. **`AGENTS.md`** (repo root) is a thin pointer to `CLAUDE.md` so Codex and other
   agents read the same guidance — do not duplicate content there.
3. **`.claude/claude.md`** is already a thin pointer to root `CLAUDE.md` (no project
   content). Leave it as-is unless the user wants to remove it.
4. Set `state.guidesInitialized = true`.

---

## Phase 6 — Final verification & report

1. Re-run the Phase 1 health check.
2. Confirm: all required plugins enabled, required skills + learning-output-style
   loaded, brand configured, `CLAUDE.md`/`AGENTS.md` filled in.
3. Set `state.setupCompleted = true` in `.claude/setup.config.json`.
4. Give the user a short **"what's installed / what's next"** summary, including any
   optional plugins they skipped and how to add them later.

Only claim setup is complete after the verification command output confirms it.

---

## Codex notes

Codex has **no plugin marketplace**. For Codex:

- **Skip Phase 2** (plugins). Codex reads `AGENTS.md` and discovers skills; it does not
  install marketplace plugins.
- **AGENTS.md** is Codex's entry point — it points to `CLAUDE.md`, which carries the
  real project guidance. Keep both in sync via that pointer (never duplicate).
- Do **Phases 3–6**: verify vendored skills, configure brand, initialize the guide files.
- Plugin-only capabilities (feature-dev agents, karimo commands, hookify) are
  Claude-Code-only. Note this to Codex users rather than pretending they installed.

---

## Quick reference

| Action | Command |
| --- | --- |
| List marketplaces | `claude plugin marketplace list` |
| Add local marketplace | `claude plugin marketplace add .` |
| Add KARIMO marketplace | `claude plugin marketplace add opensesh/KARIMO` |
| List installed plugins | `claude plugin list --json` |
| Install a plugin | `claude plugin install <name>@<marketplace>` |
| Enable / disable | `claude plugin enable <name>` · `claude plugin disable <name>` |
| Reload after changes | `/reload-plugins` (or relaunch) |
| Validate the marketplace manifest | `claude plugin validate .` |
