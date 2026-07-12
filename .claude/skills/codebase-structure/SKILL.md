---
name: codebase-structure
description: Use BEFORE creating any component, page, function, hook, util, service, or file. Forces reuse before creation and correct placement so the codebase stays clean and maintainable. Triggers on "add/create a component", "new page", "write a function", "add an endpoint", or any new file. Pattern-agnostic — not DDD, not Atomic — just good file/code hygiene.
---

# Codebase Structure

Do NOT generate a new component/function on every task. **Reuse first, then place correctly.**
This is a behavior, not a framework. No DDD, no Atomic Design — just three rules.

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

## Rule 3 — Promote on second use

When a feature-specific unit is needed by a **second** feature: **move it to the global
location and update imports** — do not copy it. Global things earn their place by being
reused, not by being guessed up front (YAGNI).

## Check before finishing

- Did I search for an existing one? (name it, or say "none found")
- Is a page holding logic that belongs in a component/hook? Extract it.
- Am I about to duplicate something? Reuse or promote instead.

Match an existing project layout when there is one; these defaults are the fallback, not a mandate.
