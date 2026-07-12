# /audit-components — React Architecture Audit

Scan all feature components against the 7 architecture principles in `.claude/reference/react-architecture.md`, produce a structured report with pass/fail per check, and output a prioritized fix plan.

## Usage

```
/audit-components
```

**This command is read-only and never modifies files.**

## Scope

- All `.tsx` files under `app/` and `components/`
- Excludes `components/uui/**` (vendor library code)
- Excludes `lib/`, `hooks/`, `utils/`, `types/` (not components)

## Behavior

Run all checks below in order. Use Grep and Glob tools (not Bash) for all searches. Collect findings per check, then produce the final report.

---

### Check 1: Component Size (Principle 2 — Single Responsibility)

For every `.tsx` file in scope, count lines (excluding blank lines, import lines, and type/interface declaration blocks).

- **PASS**: under 150 lines
- **WARN**: 150–200 lines
- **FAIL**: over 200 lines

Record each WARN and FAIL file with its line count.

---

### Check 2: devProps Compliance (devProps Requirement)

Use Grep to find files that call `devProps(` and files that export PascalCase components.

- Files in the component set that are NOT in the compliant set are missing devProps
- Apply exemptions from `/audit-devprops`: UUI vendor code, `theme-provider.tsx`, `layout.tsx`, `template.tsx`, `loading.tsx`, fragment-root pages (`page.tsx`, `about/page.tsx`), R3F components (`crt-tv-model.tsx`)

Calculate compliance percentage. **PASS** if 100%, **WARN** if 90–99%, **FAIL** if under 90%.

---

### Check 3: Shared Component Bypass (Principle 6)

Search for these patterns that indicate a shared component is being bypassed:

**SectionLabel bypass:**
- Grep pattern: `className="[^"]*section-label` and `className={[^}]*section-label` in `.tsx` files
- Exclude `components/shared/section-label.tsx` itself and any CSS files
- Each match is a FAIL — should use `<SectionLabel>` instead

**ScrollReveal bypass:**
- Grep pattern: `useInView` in component files under `components/` (not hooks/)
- Cross-reference: if the same file does NOT import from `scroll-reveal`, it is rolling its own reveal
- Each match is a WARN — should consider using `<ScrollReveal>`

---

### Check 4: Hardcoded Business Strings (Principle 7)

Search for hardcoded business values in component files:

- Grep pattern: `<CONTACT_EMAIL>` (e.g. your support/contact email) — should be in constants
- Grep pattern: `<BOOKING_URL>` (e.g. a scheduling link) — should be in constants
- Grep pattern: `<COMPANY_DOMAIN>` (excluding import paths and comments) — review each match
- Grep pattern: `\$[0-9,]+` in `.tsx` files (pricing strings) — should be in data files

Each match is a WARN. If `lib/constants.ts` exists and exports these values, downgrade matching files that import from it to PASS.

---

### Check 5: Props Typing (Props Typing Convention)

Search for anti-patterns:

**defaultProps usage:**
- Grep pattern: `\.defaultProps\s*=` in `.tsx` files
- Each match is a FAIL — React 19 deprecated

**Inline prop types:**
- Grep pattern: `function [A-Z]\w+\([^)]*:\s*\{` in `.tsx` files (inline destructured object types)
- Exclude single-prop cases like `{ children }` — only flag complex inline types (3+ properties)
- Each match is a WARN — should use a named `interface`

**`any` type usage:**
- Grep pattern: `: any` or `as any` in `.tsx` files in the project (exclude `uui/`)
- Each match is a FAIL

---

### Check 6: Duplicated Patterns (Principle 3 — DRY)

Check for known duplication patterns:

**Word-split headline animation:**
- Grep pattern: `\.split\(" "\)\.map` in `.tsx` files
- If found in 2+ files, flag as WARN with file list

**Form submission state machine:**
- Grep pattern: `"idle" \| "loading" \| "success" \| "error"` (or similar union) in `.tsx` files
- If found in 2+ files, flag as WARN with file list

**Image placeholder pattern:**
- Grep pattern: `bg-bg-tertiary` combined with centered placeholder text in component files
- If found in 3+ files, flag as WARN

---

### Check 7: Prop Drilling (Principle 4)

This check is heuristic. For each component that accepts props:

- If a prop name appears in a parent component's props AND is passed through unchanged to a child, note it
- Only flag if the same prop passes through 3+ levels

Since this is hard to detect statically, use a lighter approach:
- Grep for components that accept and pass the same prop name to a child: pattern `(\w+)=\{\1\}` (passing prop with same name)
- Cross-reference the parent to see if it also received that prop
- Flag chains of 3+ as WARN

If no clear violations are found, report as PASS with a note that this was a heuristic check.

---

## Report Format

Output this structure:

```markdown
## React Architecture Audit Report

**Date:** {today}
**Files scanned:** {n} (excluding {n} UUI vendor files)

### Summary

| Check | Status | Details |
|-------|--------|---------|
| Component Size | {PASS/WARN/FAIL} | {n} files over limit |
| devProps Compliance | {PASS/WARN/FAIL} | {pct}% compliant |
| Shared Component Usage | {PASS/WARN/FAIL} | {n} bypasses found |
| Hardcoded Strings | {PASS/WARN/FAIL} | {n} hardcoded values |
| Props Typing | {PASS/WARN/FAIL} | {n} issues |
| DRY / Duplication | {PASS/WARN/FAIL} | {n} patterns duplicated |
| Prop Drilling | {PASS/WARN/FAIL} | {n} chains found |

**Overall: {n}/7 checks passing**

### Findings

#### {Check name} — {PASS/WARN/FAIL}

{For each non-passing check, list every finding with:}
- File path
- What was found
- Severity (FAIL or WARN)
- Suggested fix (one line)

### Fix Plan

{Generate a prioritized list of fixes, ordered by:}
1. FAILs first (must fix)
2. WARNs second (should fix)
3. Group related fixes together (e.g., all SectionLabel migrations in one task)

Format each fix as:

#### Fix {n}: {short description}
**Priority:** {FAIL/WARN}
**Files:** {list of affected files}
**Action:** {what to do — be specific}
**Estimated scope:** {one-line, small/medium/large}
```

## Implementation Notes

- Use Grep (not Bash) for all searches. Prefer `files_with_matches` mode for existence checks and `content` mode when you need line-level detail.
- Use Glob to count files in scope.
- The report is a point-in-time snapshot. Re-run after fixes to verify.
- This command is purely diagnostic — do not modify any files.
- Cross-reference findings with `.claude/reference/react-architecture.md` for the authoritative rules.
- When the same file appears in multiple checks, consolidate in the fix plan so it only needs to be touched once.
