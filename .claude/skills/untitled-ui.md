# Skill: Untitled UI React Component Library

Provides component-first frontend development using the Untitled UI Pro React library. All components, patterns, and icons are available in this project — reach for them before building anything from scratch.

**Auto-activates when:** building UI components, creating pages/forms/flows, adding buttons/inputs/modals/tables/tabs, or any frontend development task.

---

## The Rule: UUI First

When building any UI:

1. **Check `components/uui/`** — the component likely already exists, production-ready
2. **Use `npx untitledui@latest add <component>`** if you need a component not yet in the repo
3. **Reach for existing custom components** (`components/ui/`) only when UUI doesn't have what you need
4. **Build from scratch** as a last resort only

---

## Available Components

All installed at `components/uui/`:

### Base — `components/uui/base/`

| Component    | Path                                 | Notes                                                                         |
| ------------ | ------------------------------------ | ----------------------------------------------------------------------------- |
| Button       | `base/buttons/button.tsx`            | Sizes: sm/md/lg/xl/2xl; Variants: primary/secondary/tertiary/link/destructive |
| Button Group | `base/button-group/button-group.tsx` | Grouped button row                                                            |
| Input        | `base/input/input.tsx`               | With label, hint-text, input-group                                            |
| Textarea     | `base/textarea/textarea.tsx`         | Multi-line input                                                              |
| Select       | `base/select/select.tsx`             | Also: combobox, multi-select, native select                                   |
| Checkbox     | `base/checkbox/checkbox.tsx`         |                                                                               |
| Toggle       | `base/toggle/toggle.tsx`             | On/off switch                                                                 |
| Slider       | `base/slider/slider.tsx`             |                                                                               |
| Dropdown     | `base/dropdown/dropdown.tsx`         | Context menus, action menus                                                   |
| Avatar       | `base/avatar/avatar.tsx`             | With label-group, profile-photo variants                                      |
| Badge        | `base/badges/badges.tsx`             |                                                                               |
| Tags         | `base/tags/`                         | Tag input/display                                                             |
| Tooltip      | `base/tooltip/tooltip.tsx`           |                                                                               |

### Application — `components/uui/application/`

| Component   | Path                                      | Notes                                                                           |
| ----------- | ----------------------------------------- | ------------------------------------------------------------------------------- |
| Modal       | `application/modals/modal.tsx`            | DialogTrigger, ModalOverlay, Modal, Dialog exports                              |
| Tabs        | `application/tabs/tabs.tsx`               | Horizontal/vertical; types: underline, button-brand, button-gray, button-border |
| Table       | `application/table/table.tsx`             | Full data table with sorting, checkboxes, dropdowns                             |
| Pagination  | `application/pagination/pagination.tsx`   | Base, dot, line variants                                                        |
| Date Picker | `application/date-picker/date-picker.tsx` | Single date + date-range-picker                                                 |
| Empty State | `application/empty-state/empty-state.tsx` |                                                                                 |

### Foundations — `components/uui/foundations/`

| Component     | Path                                          | Notes                                |
| ------------- | --------------------------------------------- | ------------------------------------ |
| Featured Icon | `foundations/featured-icon/featured-icon.tsx` | Icon in a styled container           |
| Dot Icon      | `foundations/dot-icon.tsx`                    | Status dot                           |
| Payment Icons | `foundations/payment-icons/`                  | Visa, Mastercard, Amex, PayPal, etc. |

### Shared Assets — `components/uui/shared-assets/`

| Component           | Path                                 | Notes                              |
| ------------------- | ------------------------------------ | ---------------------------------- |
| Background Patterns | `shared-assets/background-patterns/` | Circle, grid, grid-check, square   |
| Illustrations       | `shared-assets/illustrations/`       | Box, cloud, credit-card, documents |

---

## Import Patterns

```tsx
// Base components
import { Button } from '@/components/uui/base/buttons/button';
import { Input } from '@/components/uui/base/input/input';
import { Select } from '@/components/uui/base/select/select';
import { Checkbox } from '@/components/uui/base/checkbox/checkbox';
import { Toggle } from '@/components/uui/base/toggle/toggle';
import { Textarea } from '@/components/uui/base/textarea/textarea';
import { Dropdown } from '@/components/uui/base/dropdown/dropdown';
import { Avatar } from '@/components/uui/base/avatar/avatar';
import { Badge } from '@/components/uui/base/badges/badges';
import { Tooltip, TooltipTrigger } from '@/components/uui/base/tooltip/tooltip';

// Application components
import {
  DialogTrigger,
  ModalOverlay,
  Modal,
  Dialog,
} from '@/components/uui/application/modals/modal';
import { Tabs, Tab, TabList, TabPanel } from '@/components/uui/application/tabs/tabs';
import { Table } from '@/components/uui/application/table/table';
import { Pagination } from '@/components/uui/application/pagination/pagination';
import { DatePicker } from '@/components/uui/application/date-picker/date-picker';
import { EmptyState } from '@/components/uui/application/empty-state/empty-state';

// Foundations
import { FeaturedIcon } from '@/components/uui/foundations/featured-icon/featured-icon';
```

---

## Adding New Components

If a component you need isn't in `components/uui/` yet:

```bash
npx untitledui@latest add <component-name> --path components/uui -y
```

Common names: `notification`, `toaster`, `breadcrumb`, `search-input`, `progress`, `step-indicator`, `color-picker`, `file-upload`, `radio`, `divider`, `card`

For full-page templates (dashboards, settings pages, marketing):

```bash
npx untitledui@latest example
```

---

## Icons

Icons are already wired up via `@untitledui-pro/icons/line` — use the `Icon` wrapper or direct imports:

```tsx
// Preferred: use Icon wrapper (maps Lucide names, handles FA icons)
import { Icon } from '@/components/ui/Icon';
<Icon name="Settings01" />;

// Direct import (when you know the exact UUI name)
import { Settings01, Bell01, ChevronDown } from '@untitledui-pro/icons/line';
```

**Hard rules:**

- Never import from `lucide-react`
- Never use the `Sparkles` icon
- Never put icons before section headers

---

## UUI + <PROJECT> Token Alignment

UUI components use the same CSS variable conventions as <PROJECT>. When customizing:

```tsx
// UUI uses cx() utility from @/utils/cx — already installed
import { cx } from '@/utils/cx';

// <PROJECT> semantic tokens work directly in UUI component className overrides
<Button className={cx('bg-bg-brand-solid text-fg-primary')} />;
```

UUI's `sortCx` and `cx` utilities are in `utils/cx.ts` — use these for conditional class merging in any component.

---

## devProps Requirement

UUI components are source files we own — if wrapping or re-exporting them as new named components, add `devProps`:

```tsx
import { devProps } from '@/lib/utils/dev-props';
// Add to the root DOM element of any NEW component you create wrapping UUI
```

Note: Do NOT add `devProps` inside the UUI source files themselves in `components/uui/` — only in components you write in `components/` at the feature level.

---

## When to Use UUI vs Custom Components

| Situation                                                 | Use                                           |
| --------------------------------------------------------- | --------------------------------------------- |
| New feature, new component                                | `components/uui/` first                       |
| Extending existing feature with existing custom component | Keep existing `components/ui/base/` component |
| Form elements (button, input, select, checkbox, toggle)   | Always UUI                                    |
| Modals, drawers, overlays                                 | Always UUI                                    |
| Tables, tabs, pagination                                  | Always UUI                                    |
| Complex app-specific UI with no UUI equivalent            | Build custom                                  |
| Wrapping UUI for feature-specific behavior                | OK — import UUI, wrap it                      |
