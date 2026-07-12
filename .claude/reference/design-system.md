# <PROJECT> Design System Reference

<!-- Last Changed: 2026-03-16 -->

> This reference provides design system context for all Claude Code plugins in your workspace.
> Import this context when building or reviewing UI components.

---

## Brand Philosophy

**"Steward, not advisor"** — Act as a team member who speaks FROM within the brand, not an external consultant.

- Use "we" and "our" when discussing brand decisions
- Don't preface responses with "according to guidelines"
- Make brand-aligned choices feel natural, not prescriptive

---

## Core Colors (<PROJECT>)

The system uses **warm neutrals** instead of harsh black/white for an inviting, approachable feel.

| Token        | Hex       | Role                                            |
| ------------ | --------- | ----------------------------------------------- |
| **Accent**   | `<COLOR_ACCENT>` | Primary accent — CTAs, links, badges, alerts    |
| **Ink** | `<COLOR_PRIMARY>` | Warm dark — Dark mode backgrounds, primary text |
| **Paper**  | `<COLOR_BACKGROUND>` | Warm light — Light mode backgrounds, light text |

### Color Usage Rules

- **Brand colors (Accent)**: Use sparingly for primary CTAs, active states, badges
- **NEVER** use brand colors for borders or harsh outlines
- **Semantic colors**: Success (emerald-500), Warning (amber-500), Error (red-500)

### Contrast Ratios

- Paper on Ink: **18.5:1** (AAA compliant)
- Ink on Paper: **18.5:1** (AAA compliant)

---

## Typography

| Category    | Font                          | Usage                                  |
| ----------- | ----------------------------- | -------------------------------------- |
| **Display** | <FONT_DISPLAY> | Headlines, titles, hero text           |
| **Body**    | <FONT_BODY>    | Body text, paragraphs, inputs, tabs    |
| **Small**   | <FONT_BODY>    | Labels, captions, hints, metadata      |
| **Accent**  | <FONT_MONO>                        | Digital/tech feel (max 2 per viewport) |

**Note**: We use <FONT_DISPLAY> consistently—no separate code or monospace fonts.

---

## Border & Interaction Philosophy

Borders should **support, not dominate** the visual hierarchy.

> **⚠️ CSS Variable Opacity Warning**
>
> Tailwind's opacity modifier (`/30`, `/50`, etc.) does NOT work with CSS variables.
> `bg-[var(--bg-secondary)]/30` will silently fail—the opacity is ignored.
>
> **Use mapped semantic classes instead:** `bg-bg-secondary/30` works correctly.
>
> See the [Opacity Pattern Guide](#opacity-pattern-guide) section for complete guidance.

### Border States

```css
/* Default: Subtle (use secondary token, not opacity on primary) */
border border-border-secondary

/* Hover: More visible */
hover:border-border-primary

/* Focus: Clear but not harsh */
focus:border-border-primary
```

### Card Pattern

```jsx
className = 'bg-bg-secondary border border-border-secondary hover:bg-bg-secondary-hover';
```

---

## Component Patterns

### Buttons

- Built on React Aria for full WCAG compliance
- Primary: Accent background, warm hover state
- Secondary: Transparent with subtle border
- Tertiary: Text-only with hover underline

### Form Inputs

- Subtle border at rest
- Brand accent on focus (but not harsh)
- Clear label hierarchy
- Helpful hint text below
- Input font ≥16px (prevents iOS auto-zoom)
- Show errors adjacent to fields, focus first error on submit
- Don't pre-disable submit—let users discover issues

> **Deep dive**: See `frontend-design` skill §5 "Form Design" for validation patterns, autofill compatibility, and mobile considerations.

### Cards & Containers

- Use `bg-bg-secondary` for elevated surfaces (opacity modifiers don't work with CSS vars)
- Rounded corners: `rounded-lg` (8px) or `rounded-xl` (12px for brand)
- Shadows use Ink (25,25,25) not pure black
- Nested radii: child ≤ parent (e.g., outer 16px with 8px padding → inner 8px)
- Layered shadows: ≥2 layers (ambient + direct light)

---

## Interaction Patterns

### Hit Targets

| Context | Minimum |
| ------- | ------- |
| Desktop | 24×24px |
| Mobile  | 44×44px |

### Loading States

- Show delay: 150–300ms (prevent flash)
- Minimum visible: 300–500ms (avoid jarring)
- Keep original label visible during load

### State Persistence

Persist UI state in URL for share/refresh/Back/Forward:

- Filters, pagination, selected tabs
- Use [nuqs](https://nuqs.47ng.com/) for type-safe URL state

### Destructive Actions

- Confirmation dialog for permanent deletes
- Undo with timeout for soft actions
- Type-to-confirm for critical operations

> **Deep dive**: See `frontend-design` skill §3 "Interaction Patterns" for optimistic updates, focus management, and touch interactions.

---

## Animation & Motion

<PROJECT> uses a **two-system architecture** for animations. Both systems share the same easing curves and duration tiers, defined as CSS custom properties in `app/theme.css` with the canonical source in `lib/motion.tsx`.

### Two-System Rule

| System | When to Use | Examples |
| --- | --- | --- |
| **CSS Motion Tokens** (Tailwind classes) | React Aria overlay components, micro-interactions (hover, focus, state changes) | UUI modals, dropdowns, tooltips, selects, buttons, inputs, toggles |
| **Framer Motion** (`lib/motion.tsx`) | Page transitions, stagger animations, gesture-driven interactions, layout animations | `PageTransition`, `MotionItem`, `HoverScale`, `AnimatePresence` wrappers |

**Why two systems?** React Aria controls overlay mount/unmount lifecycle via CSS animation completion detection. Framer Motion's `AnimatePresence` would conflict with this lifecycle. CSS tokens handle overlays; Framer Motion handles everything else.

### Easing Curves

| Token | CSS Value | Framer Motion | Tailwind Class | Use For |
| --- | --- | --- | --- | --- |
| `--ease-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | `easings.easeOut` | `ease-motion-out` | Entrances, appearing elements |
| `--ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | `easings.easeIn` | `ease-motion-in` | Exits, disappearing elements |
| `--ease-in-out` | `cubic-bezier(0.4, 0, 0.6, 1)` | `easings.easeInOut` | `ease-motion-in-out` | Symmetric transitions (toggles) |
| Spring | N/A | `easings.spring` (stiffness: 400, damping: 30) | N/A | Interactive drag, layout shifts |

### Duration Tiers

| Token | Value | Tailwind Class | Use For |
| --- | --- | --- | --- |
| `--duration-micro` | 100ms | `duration-micro` | Hover/focus state changes, button presses |
| `--duration-quick` | 150ms | `duration-quick` | Tooltips, toggles, small popovers |
| `--duration-standard` | 200ms | `duration-standard` | Overlay exits, content swaps |
| `--duration-moderate` | 300ms | `duration-moderate` | Modal/overlay entrances, drawers |
| `--duration-page` | 350ms | `duration-page` | Route transitions, page-level animations |

### UUI Component Convention

All UUI components use <PROJECT> motion tokens. **Never use generic `ease-linear`, `ease-in`, `ease-out`** in UUI components.

```tsx
// Micro-interactions (buttons, inputs, badges, tabs)
"transition duration-micro ease-motion-out"

// Overlay enter (modals, dropdowns, tooltips, selects)
"duration-moderate ease-motion-out animate-in fade-in"

// Overlay exit
"duration-standard ease-motion-in animate-out fade-out"

// Inline styles (toggle knob)
transition: "transform var(--duration-quick) var(--ease-in-out)"
```

### Framer Motion Library (`lib/motion.tsx`)

Pre-built variants for consistent animations:

- `fadeInUp`, `fadeIn`, `scaleIn` — Content appearance
- `slideFromLeft`, `slideFromRight` — Drawers, panels
- `dropdownUp`, `staggerContainer` — Menus, lists
- `PageTransition`, `MotionItem` — Page-level wrappers
- `cssEasings`, `durations` — CSS-compatible exports for bridging

### Decision Tree

1. **Is it a UUI overlay** (modal, popover, tooltip, select)? Use CSS motion tokens via Tailwind classes.
2. **Is it a UUI micro-interaction** (hover, focus, toggle)? Use `transition duration-micro ease-motion-out`.
3. **Is it a page/route transition?** Use `PageTransition` + `MotionItem` from `lib/motion.tsx`.
4. **Does it need stagger, spring, or gesture?** Use Framer Motion variants from `lib/motion.tsx`.
5. **Is it a custom component with enter/exit?** Use `AnimatePresence` + Framer Motion variants.

### Accessibility: Reduced Motion

CSS motion tokens automatically zero all durations via `@media (prefers-reduced-motion: reduce)` in `theme.css`. Framer Motion respects `prefers-reduced-motion` natively.

### Performance

- **Prefer**: `transform`, `opacity`, `filter` (GPU-accelerated)
- **Avoid animating**: `width`, `height`, `margin`, `padding` (layout-triggering)
- **Never**: `transition: all`

> **Deep dive**: See `frontend-design` skill §4 "Motion & Animation" for variant selection guide.

---

## Accessibility (A11y) First

- All components use **React Aria Components**
- Focus states are always visible (`:focus-visible` over `:focus`)
- Color contrast meets AAA standards (prefer APCA over WCAG 2)
- Screen reader support built-in
- Never rely on color alone—always include text/icons
- Interactive states must have **more** contrast than rest state

> **Deep dive**: See `frontend-design` skill §7 "Accessibility" for APCA guidance, color independence patterns, and motion accessibility.

---

## Voice & Tone

| Quality                      | Description                            |
| ---------------------------- | -------------------------------------- |
| **Smart but not smug**       | Expert knowledge without condescension |
| **Technical but accessible** | Explain concepts clearly               |
| **Confident but humble**     | State opinions, remain open            |
| **Warm but professional**    | Friendly without being casual          |

**Formula**: Expert + Humble + Accessible + Community-focused = **<COMPANY_NAME>**

---

## Token Selection Guide

Use this guide to pick the right token for each context. All classes use **Style 2 syntax** (mapped classes like `bg-bg-primary`).

### Backgrounds

| Context                          | Token                  | Class                   |
| -------------------------------- | ---------------------- | ----------------------- |
| Page background                  | `--bg-primary`         | `bg-bg-primary`         |
| Cards, panels, elevated surfaces | `--bg-secondary`       | `bg-bg-secondary`       |
| Card hover state                 | `--bg-secondary_hover` | `bg-bg-secondary-hover` |
| Inputs, form fields              | `--bg-tertiary`        | `bg-bg-tertiary`        |
| Modal/drawer overlays            | `--bg-overlay`         | `bg-bg-overlay`         |
| Active/selected items            | `--bg-active`          | `bg-bg-active`          |

### Text/Foreground

| Context                       | Token              | Class                 |
| ----------------------------- | ------------------ | --------------------- |
| Headings, primary text        | `--fg-primary`     | `text-fg-primary`     |
| Body paragraphs               | `--fg-primary`     | `text-fg-primary`     |
| Descriptions, supporting text | `--fg-secondary`   | `text-fg-secondary`   |
| Metadata (timestamps, counts) | `--fg-tertiary`    | `text-fg-tertiary`    |
| Helper text, hints            | `--fg-quaternary`  | `text-fg-quaternary`  |
| Disabled text                 | `--fg-disabled`    | `text-fg-disabled`    |
| Placeholders                  | `--fg-placeholder` | `text-fg-placeholder` |

### Borders

| Context                                | Token                | Class                     |
| -------------------------------------- | -------------------- | ------------------------- |
| Interactive elements (inputs, buttons) | `--border-primary`   | `border-border-primary`   |
| Containers (cards, panels, sections)   | `--border-secondary` | `border-border-secondary` |
| Subtle internal dividers               | `--border-tertiary`  | `border-border-tertiary`  |
| Focus rings                            | Use `ring-brand`     | `ring-brand`              |

### Brand Colors (Use Sparingly)

| Context                   | Token                      | Class                   |
| ------------------------- | -------------------------- | ----------------------- |
| Primary CTA buttons       | `--bg-brand-solid`         | `bg-brand-solid`        |
| Links                     | `--fg-brand-primary`       | `text-fg-brand-primary` |
| Active indicators, badges | `--fg-brand-primary`       | `text-fg-brand-primary` |
| **NEVER**                 | Borders, large backgrounds | —                       |

### Naming Convention

CSS variables use underscores for states, Tailwind classes use hyphens:

```
CSS Variable:      --bg-primary_alt       --fg-secondary_hover
Tailwind Class:    bg-bg-primary-alt      text-fg-secondary-hover
```

---

## Icon System

<PROJECT> uses **Untitled UI (UUI) icons** as the primary icon library, with **Font Awesome brand icons** for company/tool logos.

### Quick Reference

| Use Case               | Library                         | Import Pattern                                               |
| ---------------------- | ------------------------------- | ------------------------------------------------------------ |
| UI icons (all)         | `@untitledui-pro/icons/line`    | `import { XClose, Cpu01 } from '@untitledui-pro/icons/line'` |
| Brand/company logos    | Font Awesome (via Icon wrapper) | `<Icon name="fa-github" />`                                  |
| Dynamic icon rendering | `<Icon>` component              | `<Icon name="Globe" />` or `<Icon name="fa-slack" />`        |

### Package: @untitledui-pro/icons (Pro — the only icon package)

We are on the **Pro tier exclusively**. Import from the `/line` style:

```tsx
import { XClose, Check, Plus, ChevronDown, SearchLg } from '@untitledui-pro/icons/line';
import { Cpu01, Magic01, ColorSwatch01 } from '@untitledui-pro/icons/line';
```

Available icon styles (all from `@untitledui-pro/icons/<style>`):

- `line` — **Default, use this** (4694 icons)
- `solid` — Filled variant
- `duotone` — Two-tone variant
- `duocolor` — Alternative two-color variant

Common icon names:

- `Cpu01` — AI/brain/processing concepts
- `Magic01` — wand/magic/AI-generate
- `ColorSwatch01` — palette/color

### UUI Naming Convention

UUI uses **numbered variants** for visual flexibility. Each icon concept has 2–6 visual styles:

- `Send01`, `Send02`, `Send03` (not `Send`)
- `Home01`, `Home02`, `Home03`
- `Settings01`, `Settings02`

**Rule:** Prefer `01` variants unless a specific visual style is needed. Consult the dev comparison page at `/dev/icons` for visual reference.

### Common Lucide → UUI Name Reference

All icons are from `@untitledui-pro/icons/line`:

| Old (Lucide)                | New (UUI)        |
| --------------------------- | ---------------- |
| `X`                         | `XClose`         |
| `Check`                     | `Check`          |
| `Plus`                      | `Plus`           |
| `ChevronDown/Up/Left/Right` | Same name        |
| `Search`                    | `SearchLg`       |
| `Loader2`                   | `Loading01`      |
| `Settings`                  | `Settings01`     |
| `Trash2`                    | `Trash01`        |
| `ExternalLink`              | `LinkExternal01` |
| `Copy`                      | `Copy01`         |
| `Download`                  | `Download01`     |
| `Upload`                    | `Upload01`       |
| `Globe`                     | `Globe01`        |
| `ArrowLeft/Right`           | Same name        |
| `MoreHorizontal`            | `DotsHorizontal` |
| `MoreVertical`              | `DotsVertical`   |
| `RefreshCw`                 | `RefreshCw01`    |
| `Brain`                     | `Cpu01`          |
| `Wand2`                     | `Magic01`        |
| `Palette`                   | `ColorSwatch01`  |

Full mapping: `lib/icon-map.ts`

### Brand Icons (Font Awesome)

Company and tool logos use Font Awesome brand icons via the `<Icon>` wrapper:

```tsx
import { Icon } from '@/components/ui/Icon';

<Icon name="fa-github" className="w-5 h-5" />
<Icon name="fa-slack" className="w-5 h-5" />
<Icon name="fa-anthropic" className="w-5 h-5" />
```

Available brand icons are listed in `lib/icons.ts` → `FA_BRAND_ICONS`. Do NOT import from `@fortawesome/free-brands-svg-icons` directly in components — use the `<Icon>` wrapper.

### Dynamic Icon Rendering (Icon Wrapper)

For cases where the icon name comes from data (e.g., stored in database):

```tsx
import { Icon } from '@/components/ui/Icon';

// UUI icon by Lucide-compat name
<Icon name="Globe" className="w-5 h-5" />

// FA brand icon
<Icon name="fa-notion" className="w-5 h-5" />
```

The `<Icon>` component handles both UUI and FA routing automatically.

### Sizing

Use Tailwind size utilities:

```tsx
className = 'w-4 h-4'; // 16px — small, inline with text
className = 'w-5 h-5'; // 20px — standard
className = 'w-6 h-6'; // 24px — prominent
className = 'w-8 h-8'; // 32px — large
```

### Hard Rules

- **NEVER import from `lucide-react`** — fully replaced by `@untitledui-pro/icons/line`
- **NEVER use the `Sparkles` icon** — hard brand ban (no UUI equivalent added, none will be added)
- **No star imports** — `import * from '@untitledui-pro/icons/line'` defeats tree-shaking; always use named imports
- **No icons before section headers** — brand rule, UI cleanliness
- **FA brand icons only via `<Icon>` wrapper** — never import `@fortawesome/free-brands-svg-icons` directly in components
- **Pro only** — `@untitledui/icons` (free tier) is NOT installed and must NOT be added

### Dev Reference Pages

Visual catalogs of all icons are available at:

- `/dev/icons` — Side-by-side comparison of Lucide→UUI mappings, FA brands, and full UUI catalog
- `/dev/icon-audit` — Persistent audit dashboard with migration stats, gap analysis, and flagged items

Use these pages to verify icon visual matches before committing.

---

## Untitled UI React Components

<PROJECT> uses the **Untitled UI Pro React component library** as the primary source for all UI components. Components are owned source files in `components/uui/` — not a runtime npm dependency.

### Component Priority Rule

**Always check `components/uui/` before building any UI.** If the component isn't installed yet, add it:

```bash
npx untitledui@latest add <component> --path components/uui -y
```

For full-page templates (dashboards, settings, marketing pages):

```bash
npx untitledui@latest example
```

### Directory Structure

```
components/uui/
  base/           # Core UI: button, input, select, checkbox, toggle, avatar, badge, dropdown, tooltip, textarea, slider, tags
  application/    # Complex UI: modal, tabs, table, pagination, date-picker, empty-state
  foundations/    # Primitives: featured-icon, dot-icon, payment-icons
  shared-assets/  # Decorative: background-patterns, illustrations
```

### Token Alignment

UUI's design tokens align directly with <PROJECT> semantic tokens — both use CSS variables with the same naming philosophy. Override UUI component styles using <PROJECT> mapped classes:

```tsx
import { cx } from '@/utils/cx'; // UUI's cx utility, installed at utils/cx.ts

// UUI components accept className — override with <PROJECT> tokens
<Button className={cx('bg-bg-brand-solid')} />;
```

### devProps on UUI Wrapper Components

UUI components in `components/uui/` do NOT need `devProps` — they're library code. Add `devProps` only when you create feature-level wrapper components:

```tsx
// ✅ Add devProps to YOUR wrapper, not to the UUI source file
export function SettingsForm() {
  return (
    <form {...devProps('SettingsForm')}>
      <Input ... />  {/* UUI Input — no devProps needed here */}
    </form>
  );
}
```

---

## Opacity Pattern Guide

Tailwind's opacity modifier (`/30`, `/50`) does NOT work with CSS variables in bracket notation. This is a silent failure that produces full-opacity backgrounds instead of the intended transparency.

### The Problem

| Pattern                       | Works? | Result                  |
| ----------------------------- | ------ | ----------------------- |
| `bg-[var(--bg-secondary)]/30` | NO     | Full opacity (bug!)     |
| `bg-bg-secondary/30`          | YES    | 30% opacity as intended |
| `bg-black/50`                 | YES    | Literal colors work     |

Why? Tailwind's opacity modifier expects a color value it can decompose into RGB channels. CSS variables are opaque strings that Tailwind can't parse, so the opacity is silently ignored.

### Three Correct Patterns

Use these patterns instead:

#### 1. Theme-Aware Transparency (Most Common)

Use semantic mapped classes with opacity modifiers:

```tsx
// Cards with subtle backgrounds
className = 'bg-bg-secondary/30 border border-border-secondary';

// Hover states
className = 'hover:bg-bg-tertiary/50';

// Brand accents at low opacity
className = 'bg-brand-solid/10 text-fg-brand-primary';
```

#### 2. Element-Level Fade (Visibility Control)

Use Tailwind's `opacity-*` utilities for element-level visibility:

```tsx
// Hover-revealed actions
className = 'opacity-0 group-hover:opacity-100 transition-opacity';

// Disabled state
className = 'opacity-50 pointer-events-none';

// Loading state
className = 'opacity-70';
```

#### 3. Modal/Overlay Backgrounds

Use literal colors for overlays (not theme-dependent):

```tsx
// Modal backdrop
className = 'bg-black/50 backdrop-blur-sm';

// Image overlay for text legibility
className = 'bg-black/40';

// Light overlay
className = 'bg-white/80';
```

### Decision Matrix

| Use Case          | Recommended Pattern                 |
| ----------------- | ----------------------------------- |
| Card backgrounds  | `bg-bg-secondary/30`                |
| Hover states      | `bg-bg-tertiary/50`                 |
| Active selections | `bg-bg-active/80`                   |
| Modal backdrops   | `bg-black/50`                       |
| Brand hints       | `bg-brand-solid/10`                 |
| Fade out elements | `opacity-50`                        |
| Hover reveal      | `opacity-0 group-hover:opacity-100` |

### Common Opacity Values

| Value | Visual Effect  | Use For                          |
| ----- | -------------- | -------------------------------- |
| `/10` | Barely visible | Brand hints, subtle badges       |
| `/20` | Very subtle    | Hover backgrounds                |
| `/30` | Light          | Card backgrounds, soft overlays  |
| `/50` | Half           | Modal backdrops, disabled states |
| `/80` | Near solid     | Emphasized surfaces              |

### ESLint Enforcement

The `bos-local/no-broken-opacity-pattern` rule automatically detects and fixes broken patterns:

```tsx
// ESLint error: bg-[var(--bg-secondary)]/30
// Auto-fixed to: bg-bg-secondary/30
```

Run `npm run lint -- --fix` to automatically fix any broken patterns in your code.

---

## For Plugin Developers

When creating or reviewing code, always:

1. **Check design token usage** — Use mapped Tailwind classes (`bg-bg-primary`), not hardcoded colors
2. **Verify accessibility** — Focus states, contrast, screen readers
3. **Apply warm neutrals** — Avoid pure black/white
4. **Use subtle borders** — Use `border-secondary` for containers, never brand color for borders
5. **Match brand voice** — Steward, not advisor
6. **Never use opacity on CSS vars** — `bg-[var(--bg-primary)]/50` silently fails; use dedicated tokens

---

_This reference is synced with <PROJECT>_
