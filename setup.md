# Setup Runbook

> **You are an AI coding agent (Claude Code or Codex). A user has just opened this
> starter template and asked you to set it up.** Follow this runbook top to bottom.
> It is a *reference for setup*, not a description of an already-configured project.

The desired capability set is declared in
**[`.claude/setup.config.json`](.claude/setup.config.json)** and canonical behavior lives
under `.claude/`. Codex platform mappings live in `.agents/parity.config.json`; the
generated inventory is `.agents/capability-map.json`. Human-readable docs live in
**[`.claude/README.md`](.claude/README.md)**.

---

## When to run this

- The **first time** the template is opened in a new project, or
- Whenever the user says "run setup", "set up the template", "bootstrap", or similar.

It is **idempotent** — safe to re-run. Each phase checks current state before acting
and updates the `state` flags in the config when it finishes.

## Ground rules for the agent

**This template is for "vibe coders" — assume the user may not know how to code.** Do the
work *for* them. Don't hand them a list of commands to paste; **you run every command
yourself**, explain in plain language what each step does and why, verify it worked, and
fix failures without making them debug. Ask for a plain-language **"yes, go ahead"** at
each side-effecting step — not for command syntax.

1. **Get consent, then do it yourself.** Installing plugins/tools, adding marketplaces,
   and editing standing config need a clear "yes". Say what you're about to install and
   what it does, wait for yes, **then run the command yourself**. Never install silently.
2. **Offer bypass-permissions mode for a smooth install.** A non-technical user will hit
   many approval prompts across a multi-tool install. Offer to let them switch Claude Code
   into **bypass-permissions mode** (cycle modes with **Shift+Tab**, or launch with
   `claude --dangerously-skip-permissions`) so you can install without a prompt on every
   command. Explain plainly: it lets you run install commands without asking each time,
   it's their choice, and they can switch back (Shift+Tab) the moment setup is done. If
   they decline, proceed with per-command approvals — never pressure them.
3. **Read `.claude/setup.config.json` first** and treat its `required` / `optional`
   lists as authoritative. If this runbook and the config ever disagree, the config wins.
4. **Report, don't assume.** After each phase, show the user what changed and what is
   still missing. Do not claim success without running the verification command.
5. **Use the active harness path.** Claude Code installs the vendored marketplace
   plugins. Codex uses generated project adapters plus Codex-native plugins such as
   KARIMO. Read the [Codex notes](#codex-notes) before Phase 2.

---

## Phase 0 — Load config & detect environment

1. Read `.claude/setup.config.json`.
2. Detect the **active agent runtime** from the current session; CLI presence is only a
   diagnostic because both CLIs may be installed. The user's explicit choice wins.
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

For Codex, use its own marketplace and parity checks instead:

```bash
codex plugin marketplace list
codex plugin list
node scripts/sync-agent-adapters.mjs --check --machine
```

The last command verifies every generated adapter and required native dependency,
including `karimo@personal >= 9.11.0`, without storing its machine path in the repo.

**Output styles** (skills-dir plugins) — they appear under
"Skills-directory plugins" in `claude plugin list`. For each in
`config.outputStyles`, mark loaded / not loaded.

**Skills** — on Claude, verify each `config.skills.required[]` directory exists and has
a `SKILL.md`:
```bash
ls .claude/skills
```
Skills auto-load at project scope, so "present + workspace trusted" = healthy.
On Codex, verify the matching generated skills under `.agents/skills/` through the
parity check above.

**Optional tools** (`config.optionalTools`) — external CLIs, check presence only:
```bash
rtk --version 2>/dev/null; graphify --version 2>/dev/null
```

Present a single **health report** (✔ ok / ⚠ disabled / ✘ missing) covering marketplaces,
required plugins, optional plugins, output styles, required skills, and optional tools.
Then move on.

---

## Phase 2 — Install marketplaces & plugins (needs approval)

Only for items the health check flagged as missing. **Ask before each group.**

### Codex path

The vendored Claude plugins are already expanded into project-scoped Codex skills,
agents, and hooks. Do not install or copy them into a Codex plugin cache. Run the sync
writer after canonical source changes:

```bash
node scripts/sync-agent-adapters.mjs --write
```

KARIMO is the native-machine exception. If the health check says it is missing or old,
ask approval, confirm the `personal` marketplace is configured, then install/upgrade
the Codex version (not the Claude marketplace version):

```bash
codex plugin marketplace list
codex plugin add karimo@personal
node scripts/sync-agent-adapters.mjs --check --machine
```

Ponytail remains optional and only has cross-harness parity when the user opts in and a
Codex-native Ponytail plugin is available. After Codex passes the machine check, continue
with Phase 2e; skip Claude-only steps 2a–2d below.

### Claude Code path

Steps 2a–2d below apply only to Claude Code.

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

List `config.plugins.optional[]` with descriptions and let the user pick. Install only
what they choose. **ponytail** lives on its own marketplace — add it first (2a) if chosen:

```bash
claude plugin install ralph-wiggum@vibe-code-starter
claude plugin install pr-review-toolkit@vibe-code-starter
# ponytail (token-efficiency; needs `node` on PATH) — from the DietrichGebert/ponytail marketplace
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail
```

### 2d. Apply & verify

Plugins load on restart. Ask the user to run `/reload-plugins` (or relaunch), then
re-run `claude plugin list` and confirm every required plugin is **enabled**. Set
`state.pluginsInstalled = true` in the config once confirmed.

> If a `claude plugin install` fails, do **not** retry blindly. Report the error,
> check `claude plugin marketplace list`, and confirm the marketplace was added first.

### 2e. Offer token-efficiency tools (optional, EXTERNAL)

`config.optionalTools` are **external CLIs, not Claude Code plugins**. **Offer each with
a plain-language description; install only what the user opts into — and install it FOR
them** (detect the platform, pick the method that works, run it, verify). First check
what's already present and pick accordingly:
```bash
rtk --version 2>/dev/null; graphify --version 2>/dev/null   # already installed?
uv --version; node --version; cargo --version               # what installers exist?
```

- **rtk** (Rust Token Killer, `rtk-ai/rtk`) — a proxy that compresses command output
  before it reaches the model (60-90% fewer tokens from tool output). Integrates via a
  hook. Pick by platform:
  ```bash
  # macOS / Linux:
  brew install rtk
  # OR (any OS with Rust toolchain — e.g. Windows):
  cargo install --git https://github.com/rtk-ai/rtk
  # Windows without Rust: download rtk-x86_64-pc-windows-msvc.zip from the repo's
  #   Releases and put rtk.exe on PATH.
  rtk --version && rtk gain          # verify (rtk gain must work → correct package)
  ```
  ⚠️ **Never** `cargo install rtk` from crates.io (that's a different project). Use
  `--git`. After install, register the hook per the repo's INSTALL.md (`rtk hook claude`),
  and put `ripgrep` (`rg`) on PATH so its filters work.

- **graphify** (`Graphify-Labs/graphify`) — maps the project into a queryable knowledge
  graph so the agent queries it instead of grepping files.
  ```bash
  uv tool install graphifyy   # or: pipx install graphifyy
  graphify install            # registers the /graphify skill
  graphify --version
  ```
  Then `/graphify .` builds `graphify-out/{graph.html, GRAPH_REPORT.md, graph.json}`.

Do not auto-install these silently — they pull external toolchains. But once the user
says yes, **run the install yourself**, verify with the health-check, and troubleshoot
failures. Record which the user accepted; note skipped ones in the final report.

---

## Phase 3 — Verify skills & output styles

For Claude Code:

1. Confirm every `config.skills.required[]` dir exists with a `SKILL.md`.
2. Confirm `config.outputStyles.required[]` and opted-in optional styles are present.
3. If the workspace was just trusted, have the user run `/reload-plugins`.
4. Re-run `claude plugin list` and confirm skills-dir plugins show as loaded.

For Codex:

1. Confirm the workspace is trusted so project config, hooks, and skills load.
2. Run `node scripts/sync-agent-adapters.mjs --check --machine`.
3. Confirm `.agents/skills/`, `.codex/agents/`, and `.codex/hooks.json` are present.
4. Learning output style is the SessionStart default. Set
   `CODEX_OUTPUT_STYLE=explanatory` before launch for the optional style, or `none` to
   disable output-style context.

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

1. Re-run the Phase 1 health check for the active harness.
2. Run `node scripts/sync-agent-adapters.mjs --check --machine` and confirm parity.
3. Confirm: required plugins/adapters enabled, required skills + learning-output-style
   loaded, brand configured, `CLAUDE.md`/`AGENTS.md` filled in.
4. Set `state.setupCompleted = true` in `.claude/setup.config.json`.
5. Give the user a short **"what's installed / what's next"** summary, including any
   optional plugins they skipped and how to add them later.

Only claim setup is complete after the verification command output confirms it.

---

## Codex notes

Codex supports native plugins, project skills, custom agents, and hooks. This repo uses
all four without changing Claude's working files:

- `AGENTS.md` points to canonical `CLAUDE.md` guidance.
- `.agents/skills/` wraps Claude skills and commands.
- `.codex/agents/` maps vendored plugin agents with collision-safe names.
- `.codex/hooks.json` bridges Hookify, security reminders, output style, and Ralph state.
- KARIMO uses the installed Codex-native `karimo@personal` plugin. The Claude KARIMO
  command/standard files are mapped to its native skills, never copied.
- `.agents/capability-map.json` lists every mapping. Any new unmapped Claude capability
  makes the parity check fail.

Invocation syntax differs only at the surface: `/feature-dev` in Claude becomes
`$feature-dev` in Codex. Workflow behavior and gates still come from the same source.

---

## Quick reference

| Action | Command |
| --- | --- |
| List marketplaces | `claude plugin marketplace list` |
| List Codex marketplaces | `codex plugin marketplace list` |
| List Codex plugins | `codex plugin list` |
| Install native Codex KARIMO | `codex plugin add karimo@personal` |
| Sync Codex adapters | `node scripts/sync-agent-adapters.mjs --write` |
| Check Claude/Codex parity | `node scripts/sync-agent-adapters.mjs --check --machine` |
| Add local marketplace | `claude plugin marketplace add .` |
| Add KARIMO marketplace | `claude plugin marketplace add opensesh/KARIMO` |
| Add ponytail marketplace | `claude plugin marketplace add DietrichGebert/ponytail` |
| Install ponytail (token-eff.) | `claude plugin install ponytail@ponytail` |
| Install rtk (token-eff., external) | `brew install rtk` (see repo INSTALL.md on Windows) |
| Install graphify (external) | `uv tool install graphifyy && graphify install` |
| List installed plugins | `claude plugin list --json` |
| Install a plugin | `claude plugin install <name>@<marketplace>` |
| Enable / disable | `claude plugin enable <name>` · `claude plugin disable <name>` |
| Reload after changes | `/reload-plugins` (or relaunch) |
| Validate the marketplace manifest | `claude plugin validate .` |
