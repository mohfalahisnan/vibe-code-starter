---
name: brand-guidelines
description: Applies <COMPANY_NAME>'s brand colors, typography, and voice to any artifact that benefits from an on-brand look-and-feel. Use when brand colors, style guidelines, visual formatting, or company design standards apply. NOTE - this skill is a template; run setup.md (Phase 4) to configure it for your brand.
---

# <COMPANY_NAME> Brand Styling

> ⚠️ **This skill is not configured yet.** It ships as a template with `<PLACEHOLDER>`
> fields. Run **[`setup.md`](../../../setup.md) Phase 4** — the agent interviews you and
> rewrites this file (and `.claude/brand/`) with your brand's real values, then sets
> `brand.configured = true` in [`.claude/setup.config.json`](../../setup.config.json).
> Until then, do **not** apply the placeholder values literally.

## Overview

Use this skill to apply <COMPANY_NAME>'s official brand identity to generated artifacts.
<COMPANY_NAME> — <TAGLINE>.

**Keywords**: branding, corporate identity, visual identity, styling, brand colors,
typography, visual formatting, visual design, design systems.

## Brand Guidelines

### Colors

Fill these from `setup.config.json → brand.identity.colors`.

**Primary Palette:**

- **Background** — `<COLOR_BACKGROUND>` — primary surface. ~45–50% of composition.
- **Primary** — `<COLOR_PRIMARY>` — primary text / foreground and secondary surfaces. ~45–50% of composition.
- **Accent** — `<COLOR_ACCENT>` — CTAs, highlights, interactive elements. **MAXIMUM 10%** of composition.

> **Ratio rule (keep this regardless of brand):** background + primary ≈ 45–50% each;
> accent capped at 10%. This ratio is what makes the palette read as intentional.

**Grayscale system:** define a neutral ramp (e.g. `<GRAY_90>` … `<GRAY_10>`) for
borders, disabled states, and subtle text. Derive from your primary/background neutrals.

### Typography

Fill from `setup.config.json → brand.identity.typography`.

- **Display font**: `<FONT_DISPLAY>` — large headings, hero text (H1–H2, display sizes).
- **Body font**: `<FONT_BODY>` — body copy, captions, labels, buttons.
- **Mono / accent font**: `<FONT_MONO>` — code, technical content, personality accents.
  - **Rule**: use the accent font sparingly (max ~2 instances per viewport).

**Fallback stacks** (keep robust fallbacks so artifacts render everywhere):
- Display / Body: `<FONT_...>, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif`
- Mono: `<FONT_MONO>, ui-monospace, SFMono-Regular, Menlo, Consolas, "Courier New", monospace`

### Logo & assets

- **Logo location**: `<LOGO_PATH>`
- **Fonts location**: `<FONTS_PATH>`
- **Icon set**: `<ICON_SET>`
- **Image style**: `<IMAGE_STYLE>`

### Brand personality

Fill from `setup.config.json → brand.identity.tone`.

- **Mission**: `<MISSION>`
- **Tone**: `<TONE>`
- **Core traits**: `<TRAIT_1>`, `<TRAIT_2>`, `<TRAIT_3>` — and when each applies.

## Application rules (transferable — keep these)

These rules are brand-agnostic best practices. Keep them; only the color/font *names*
change per brand.

### Color usage

- **Backgrounds**: only the two primary neutrals (`<COLOR_BACKGROUND>` / `<COLOR_PRIMARY>` surface). Alternate them for rhythm. Never use the accent as a primary background.
- **Text**: maximum contrast pairing — primary text on background, background on primary surface.
- **Accent (`<COLOR_ACCENT>`)**: ≤10% of composition; best for CTAs, highlights, interactive elements; never for body copy or large headlines.
- **Ratio**: maintain ~45–50% background, ~45–50% primary, ≤10% accent.

### Accessibility

- Primary/background pairing should meet **WCAG AA at minimum, AAA where possible**.
- Verify accent-on-background and accent-on-surface contrast before using accent for text.
- Interactive elements: minimum 44×44px touch targets.

### Typography hierarchy

- Display / H1–H2: `<FONT_DISPLAY>` (bold) for hero and page/section titles.
- H3–H4: `<FONT_DISPLAY>` (medium) for subsections.
- H5–H6: `<FONT_MONO>` (accent) — personality subheadings, used sparingly.
- Body / buttons / captions: `<FONT_BODY>`.
- Keep ≥2 size steps between hierarchy levels; use weight (not just size) for emphasis.
- Line height ≈ 1.2 for headings, ≈ 1.5 for body.

## Design tokens (fill in during setup)

```css
/* Colors — from brand.identity.colors */
--color-brand-background: <COLOR_BACKGROUND>;
--color-brand-primary:    <COLOR_PRIMARY>;
--color-brand-accent:     <COLOR_ACCENT>;

/* Typography — from brand.identity.typography */
--font-display: "<FONT_DISPLAY>", system-ui, sans-serif;
--font-text:    "<FONT_BODY>", system-ui, sans-serif;
--font-mono:    "<FONT_MONO>", ui-monospace, monospace;
```

## When to apply this skill

Use when creating presentations, documents, marketing materials, educational content,
or any branded artifact for <COMPANY_NAME> — but only **after** setup has replaced the
placeholders above with real values.
