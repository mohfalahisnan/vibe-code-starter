# <PROJECT> Code Quality

> This skill activates during code review, PR review, quality checks, or when phrases like "check quality", "review code", "verify compliance", or "design system check" appear. Auto-activates after any UI component work.

---

## Core Purpose

Ensure all code meets <PROJECT> standards for design system compliance, accessibility, and brand consistency. This skill integrates with code reviews to add <PROJECT>-specific quality gates.

---

## Quality Dimensions

### 1. Design System Compliance

#### Color Usage

```
✅ CORRECT                           ❌ WRONG
var(--bg-primary)                    bg-white
var(--fg-secondary)                  text-gray-500
var(--border-primary)                border-slate-200
```

**Verification Command:**

```bash
# Find hardcoded colors (should return empty)
grep -rE "#[0-9A-Fa-f]{3,6}|rgb\(|rgba\(" --include="*.tsx" --include="*.css" | grep -v "var(--"

# Find forbidden Tailwind classes
grep -rE "bg-white|bg-black|text-white|text-black|border-white|border-black" --include="*.tsx"
```

#### Border Patterns (Style 2 Syntax)

```tsx
// ✅ CORRECT - Subtle, supportive (Style 2 mapped classes)
className = 'border border-border-secondary hover:border-border-primary';

// ❌ WRONG - Harsh, dominant
className = 'border-2 border-white';
className = 'border border-brand'; // Never brand color for borders
```

#### Brand Color (Accent <COLOR_ACCENT>) Usage

```
ALLOWED                              FORBIDDEN
─────────────────────────────────────────────────────
Primary CTA buttons                  Borders
Active/selected states               Backgrounds (except buttons)
Badge accents                        Decorative elements
Link hover states                    Large areas
```

### 2. Component Patterns

#### React Aria Requirement

All interactive elements MUST use React Aria Components:

```tsx
// ✅ CORRECT
import { Button, Input, Select } from 'react-aria-components';

// ❌ WRONG
<button onClick={...}>  // Missing accessibility
<input type="text" />   // Missing ARIA support
```

#### Card Pattern (Style 2 Syntax)

```tsx
// ✅ Standard <PROJECT> Card
<div className={cn(
  "bg-bg-secondary",
  "border border-border-secondary",
  "rounded-xl",
  "hover:bg-bg-secondary-hover",
  "hover:border-border-primary",
  "transition-colors duration-150"
)}>

// ❌ Wrong patterns
<div className="bg-white rounded-lg shadow">  // Hardcoded
<div className="bg-gray-100 border-2">        // Wrong token
```

#### Button Variants (Style 2 Syntax)

```tsx
// Primary (Accent accent)
className = 'bg-brand-solid text-white hover:bg-brand-solid_hover';

// Secondary (transparent)
className = 'bg-transparent border border-border-primary hover:bg-bg-secondary-hover';

// Tertiary (text only)
className = 'text-fg-secondary hover:text-fg-primary hover:underline';
```

### 3. Accessibility Standards

#### Focus Management (Style 2 Syntax)

```tsx
// ✅ Focus visible and styled
className="focus:outline-none focus:ring-2 focus:ring-brand focus:ring-offset-2"

// ✅ Skip link for keyboard users
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to content
</a>
```

#### Color Contrast

```
Minimum Requirements:
- Normal text: 4.5:1 ratio (AA)
- Large text: 3:1 ratio (AA)
- UI components: 3:1 ratio

<PROJECT> Palette Compliance:
- Paper on Ink: 18.5:1 ✅ AAA
- Ink on Paper: 18.5:1 ✅ AAA
- Accent on Ink: 5.5:1 ✅ AA (large text)
```

#### Screen Reader Support

```tsx
// ✅ Descriptive labels
<Button aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</Button>

// ✅ Live regions for dynamic content
<div role="status" aria-live="polite">
  {statusMessage}
</div>
```

### 4. Typography

#### Font Usage

```css
/* Headlines */
font-family: '<FONT_DISPLAY>', system-ui, sans-serif;

/* Body */
font-family: '<FONT_BODY>', system-ui, sans-serif;

/* Accent/Display */
font-family: '<FONT_MONO>', monospace;

/* Code */
font-family: 'SF Mono', Consolas, Monaco, monospace;
```

#### Never Use

- Generic sans-serif for headlines
- System fonts where brand fonts should appear
- <FONT_MONO> for body text (accent only)

### 5. React Architecture Compliance

> Full rules: `.claude/reference/react-architecture.md`

#### Component Size

- **Flag** any component file over 200 lines (excluding imports and type definitions)
- **Warn** on files over 150 lines
- Exemptions: `page.tsx` thin server wrappers, UUI vendor components in `components/uui/`

#### Single Responsibility Check

When reviewing a component, verify it has ONE primary job:
- Renders UI OR manages state OR handles data — not all three
- If a component does layout + data fetching + complex state, flag for extraction

#### DRY Pattern Detection

Flag these known duplication patterns if found in new code:
- Inline `useInView` + `motion.div` animation — should use `<ScrollReveal>` from `components/shared/scroll-reveal.tsx`
- Raw `<p className="section-label">` — should use `<SectionLabel>` from `components/shared/section-label.tsx`
- Duplicated `idle | loading | success | error` state machine — should use a shared `useFormSubmission` hook (once extracted)
- Hardcoded emails/URLs — should import from `@/lib/constants`

#### devProps Check

- Every feature component (not UUI vendor code) must have `{...devProps('ComponentName')}` on its root element
- Import: `import { devProps } from '@/utils/dev-props'`
- Run `/audit-devprops` for a full compliance report

#### Prop Drilling Check

- If a prop is passed through 2+ intermediate components unchanged, flag it
- Suggest: React Context, component composition, or URL state

### 6. Animation Standards

#### Approved Libraries

```tsx
// Complex choreography
import { motion } from 'framer-motion';

// High-performance scroll/timeline
import gsap from 'gsap';

// Simple transitions
className = 'transition-colors duration-150';
```

#### Timing Guidelines

```css
/* Micro-interactions: 150ms */
transition-duration: 150ms;

/* UI transitions: 200-300ms */
transition-duration: 200ms;

/* Page transitions: 300-500ms */
transition-duration: 300ms;
```

---

## Quality Checklist

Use this checklist for every code review:

```markdown
## <PROJECT> Quality Review

### Design System (Style 2 Syntax)

- [ ] All colors use mapped Tailwind classes (bg-bg-_, text-fg-_, border-border-\*)
- [ ] No hardcoded hex/rgb values
- [ ] Borders use semantic tokens (border-secondary for containers, border-primary for interactive)
- [ ] Brand color (Accent) used appropriately
- [ ] Warm neutrals (Ink/Paper) not black/white

### Components

- [ ] Interactive elements use React Aria
- [ ] Card pattern matches <PROJECT> standard (bg-bg-secondary, border-border-secondary)
- [ ] Button variants are correct
- [ ] Focus states visible and styled (ring-brand)

### Accessibility

- [ ] Color contrast meets AA minimum
- [ ] Focus management implemented
- [ ] ARIA labels present
- [ ] Keyboard navigation works

### Typography

- [ ] Correct font families used
- [ ] <FONT_MONO> only for accents
- [ ] Font sizes from scale

### Animation

- [ ] Uses approved libraries
- [ ] Timing follows guidelines
- [ ] No jarring transitions

### React Architecture

- [ ] Component under 200 lines (soft limit 150)
- [ ] Single responsibility (one job per component)
- [ ] No duplicated patterns (uses shared components where they exist)
- [ ] `devProps` on root element of feature components
- [ ] No prop drilling past 2 levels
- [ ] No hardcoded business strings (emails, URLs, pricing)
- [ ] Heavy components lazy-loaded (`next/dynamic` or `React.lazy`)
```

---

## Automated Checks

### Pre-commit Hook (hookify integration)

```bash
# Block hardcoded colors
if grep -rE "#[0-9A-Fa-f]{6}" --include="*.tsx" | grep -v "var(--"; then
  echo "ERROR: Hardcoded colors found. Use CSS variables."
  exit 1
fi

# Warn on missing React Aria
if grep -rE "<button|<input|<select" --include="*.tsx" | grep -v "react-aria"; then
  echo "WARNING: Native elements found. Consider React Aria."
fi
```

### CI Quality Gate

```yaml
bos-quality-check:
  runs-on: ubuntu-latest
  steps:
    - name: Check Design System Compliance
      run: |
        # No hardcoded colors
        ! grep -rE "#[0-9A-Fa-f]{3,6}" --include="*.tsx" | grep -v "var(--"

    - name: Check Accessibility
      run: npx axe-core --include "src/**/*.tsx"
```

---

## Issue Severity Levels

### Critical (Must Fix Before Merge)

- Hardcoded colors bypassing design system
- Missing accessibility on interactive elements
- Pure black (#000) or white (#FFF) usage
- Brand color misuse (borders, decorative)
- Prop drilling past 2 levels in new code

### Important (Should Fix Before Merge)

- Missing focus states
- Incorrect button variant
- Wrong font family
- Animation timing off
- Component over 200 lines
- Missing `devProps` on feature component
- Duplicated pattern that has a shared component available

### Minor (Track for Future)

- Suboptimal class ordering
- Could use more semantic token
- Animation could be smoother
- Component between 150–200 lines
- Hardcoded string that should be in constants

---

## Integration with Existing Plugins

### With code-review

- <PROJECT> quality is a dimension of code-review
- Add <PROJECT> checklist to review output

### With feature-dev

- Quality gates at Build and Review phases
- Block phase transition on Critical issues

### With hookify

- Create hooks for automated <PROJECT> checks
- Warn on deviations, block on violations

### With verification-before-completion

- <PROJECT> compliance is verification criterion
- Must pass quality check before "complete"

---

## Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│  <PROJECT> CODE QUALITY QUICK CHECK                              │
├────────────────────────────────────────────────────────────┤
│  Colors:     bg-bg-*, text-fg-*, border-border-*          │
│  Borders:    border-border-secondary (containers)         │
│  Brand:      Accent for CTAs/active ONLY                  │
│  Components: React Aria for all interactive               │
│  Cards:      bg-bg-secondary, border-border-secondary     │
│  Focus:      ring-2 ring-brand                            │
│  Contrast:   18.5:1 Ink↔Paper (AAA)               │
├────────────────────────────────────────────────────────────┤
│  ❌ NEVER: #000, #FFF, bg-white, border-brand             │
│  ✅ ALWAYS: CSS vars, React Aria, focus states           │
└────────────────────────────────────────────────────────────┘
```

---

## Supporting Files

### Examples

- **[Review Walkthrough](review-walkthrough.md)** — Step-by-step example of conducting a code quality review on a FilterPanel PR, identifying issues and providing corrections

### References

- **[Design Token Mapping](design-token-mapping.md)** — Complete mapping of all <PROJECT> semantic tokens (backgrounds, text, borders, states) with usage patterns and migration guide

---

_Project-specific skill for design-system quality enforcement_
