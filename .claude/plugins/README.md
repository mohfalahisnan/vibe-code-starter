# <PROJECT> Plugins

> Complete packages that bundle agents, commands, hooks, and skills together.

---

## What Are Plugins?

Plugins are comprehensive packages that:
- **Bundle multiple capabilities** — agents + commands + hooks + skills
- **Provide complete workflows** — everything needed for a use case
- **Can be complex** — multiple interconnected components
- **Are self-contained** — work independently

---

## Plugins Inventory

| Plugin | What It Does | Key Commands |
|--------|--------------|--------------|
| [agent-sdk-dev](./agent-sdk-dev/) | Build Agent SDK applications | `/new-sdk-app` |
| [hookify](./hookify/) | Create custom rules and guardrails | `/hookify`, `/hookify:list` |
| [plugin-dev](./plugin-dev/) | Build your own plugins with guided workflow | `/plugin-dev:create-plugin` |
| [pr-review-toolkit](./pr-review-toolkit/) | Specialized PR review with multiple agents | `/pr-review-toolkit:review-pr` |

---

## How Plugins Differ from Other Types

| Type | Purpose | Complexity |
|------|---------|------------|
| **Plugins** | Complete packages with multiple components | High |
| **Agents** | Autonomous workflows | Medium |
| **Commands** | Single-purpose operations | Low |
| **Skills** | Contextual knowledge (auto-activates) | Low |

---

## Plugin Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Plugin metadata
├── agents/              # AI agents
├── commands/            # Slash commands
├── skills/              # Contextual knowledge
├── hooks/               # Event handlers
├── core/                # Core logic (if needed)
└── README.md            # Documentation
```

---

## Featured Plugin: hookify

The most powerful plugin for creating custom rules:

```
/hookify                    # Interactive hook creation
/hookify:list              # See all active hooks
```

Use hookify to:
- Warn on hardcoded colors
- Block commits without tests
- Enforce <PROJECT> design patterns
- Create custom guardrails

---

## <PROJECT> Design System Integration

All plugins are adapted for <PROJECT>:
- **Accent** (<COLOR_ACCENT>) — Primary accent
- **Ink** (<COLOR_PRIMARY>) — Warm dark neutral
- **Paper** (<COLOR_BACKGROUND>) — Warm light neutral

See [<PROJECT>-DESIGN-SYSTEM.md](<PROJECT>-DESIGN-SYSTEM.md) for complete reference.

---

*Part of the <PROJECT> config system*
