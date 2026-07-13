---
name: codebase-structure
description: Use BEFORE creating or editing any component, page, function, hook, util, service, or file. Forces reuse before creation, correct placement, single responsibility (no GOD files), and consistent naming so the codebase stays clean and maintainable. Triggers on "add/create a component", "new page", "write a function", "add an endpoint", any new file, or any file growing large. Pattern-agnostic — not DDD, not Atomic — just good file/code hygiene.
---

# Codebase Structure

Do NOT generate a new component/function on every task. **Reuse first, then place correctly.**
This is a behavior, not a framework. No DDD, no Atomic Design — just five rules.

## Rule 1 — Reuse before you create

Before writing a new component, function, hook, or util, **search the codebase for one
that already does it** (grep by name, by purpose, and by nearby feature). Then, in order:

1. **Exists already?** Import and use it. Stop.
2. **Almost exists?** Extend it (a prop, a param, a variant) instead of forking a copy.
3. **Only if nothing fits:** create it — and place it per Rule 2.

Never copy-paste a component/util to tweak it. Duplication is the thing this skill exists to prevent.

## Rule 2 — Classify, then place

Answer two questions before creating the file:

**A. What is it?**
- **Page / route** → it only *orchestrates*: fetches data and composes components. No reusable
  UI or business logic lives inline in a page. If a page grows logic, extract it into a component/hook.
- **Component / hook / util / service** → reusable unit. Go to B.

**B. Global or feature-specific?**
- **Global** — generic, no knowledge of one feature, usable by 2+ features (buttons, inputs,
  formatters, api client, shared middleware).
- **Feature-specific** — only meaningful inside one feature.

Then place it (follow the project's existing layout if it already has one; otherwise default to):

| What | Global | Feature-specific |
|------|--------|------------------|
| Page / route | `app/` or `pages/` (orchestrate only) | — |
| UI component | `components/ui/` | `features/<feature>/components/` |
| Hook / util | `lib/` or `hooks/` | `features/<feature>/` |
| Backend (service / handler / util) | `server/shared/` | `server/features/<feature>/` |

## Rule 3 — One responsibility per file (no GOD files)

A file does **one thing** and exports one primary concern. The moment a file starts doing
several unrelated jobs, split it — don't let it grow into a GOD file that everything imports
and nobody dares touch.

Split when you see any of these smells:
- **Mixed concerns** — UI + data fetching + business logic in one file, or an HTTP handler
  that also validates, queries the DB, and formats the response. Separate them (component ↔ hook ↔
  service ↔ util).
- **Two exports that aren't variations of one thing** — that's two files.
- **A "utils"/"helpers"/"index" dumping ground** — grouping *cohesive* helpers is fine; a bag of
  unrelated functions is not. Split by purpose (`date.ts`, `currency.ts`), not by "misc".
- **Size as a signal, not a law** — a file past ~200–300 lines or a function past ~50 is a *prompt
  to look*, not an automatic error. Split when responsibilities are tangled, not just because it's long.

Extraction must not duplicate — pull the shared piece out and import it (Rules 1 & 5 still apply).

## Rule 4 — Consistent naming

Match the **naming convention already in the project** — one casing per kind, no second style
introduced. If the project has none, default to:

| Kind | Convention | Example |
|------|-----------|---------|
| Component file + export | `PascalCase` | `UserCard.tsx` → `UserCard` |
| Hook | `useX` camelCase | `useAuth.ts` → `useAuth` |
| Util / function / var | `camelCase` | `formatCurrency.ts` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Folder | match project (kebab or camel) | `user-profile/` |

- **Name for what it does**, not how it's built or a vague label — `sendInvoiceEmail`, not
  `handleThing` / `utils2` / `data`.
- **File name matches its main export.** One casing style per kind across the whole repo — never
  `UserCard.tsx` next to `user_card.tsx`.
- Before naming, grep a sibling file of the same kind and copy its convention exactly.

## Rule 5 — Promote on second use

When a feature-specific unit is needed by a **second** feature: **move it to the global
location and update imports** — do not copy it. Global things earn their place by being
reused, not by being guessed up front (YAGNI).

## Check before finishing

- Did I search for an existing one? (name it, or say "none found")
- Is a page holding logic that belongs in a component/hook? Extract it.
- Does this file do **one** thing? If it mixed concerns or grew into a GOD file, split it.
- Does the name and casing match a sibling file of the same kind?
- Am I about to duplicate something? Reuse or promote instead.

Match an existing project layout when there is one; these defaults are the fallback, not a mandate.
