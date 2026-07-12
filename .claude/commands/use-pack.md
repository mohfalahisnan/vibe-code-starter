---
description: Activate an agency pack for specialized capabilities
allowed-tools: Read, Glob
---

# /use-pack - Agency Pack Activation

Activate a third-party agent pack for specialized capabilities.

## Usage

```
/use-pack <pack-name>
```

## Available Packs

| Pack | Description |
|------|-------------|
| `a11y` | WCAG 2.2 AA compliance, screen reader testing, React Aria validation |
| `perf` | Core Web Vitals, Lighthouse automation, bundle analysis |
| `security` | Threat modeling, secure code review, OWASP Top 10 |
| `database` | Supabase/PostgreSQL query analysis, index optimization |
| `ux` | User research frameworks, usability testing, persona development |

## Instructions

When a user runs `/use-pack <pack-name>`:

1. **Validate the pack name** from the list above
2. **Read the agent file** from `.claude/agency-packs/<pack>/<agent>.md`
3. **Load the agent's full context** including <PROJECT>-specific rules
4. **Confirm activation** with a brief summary of capabilities
5. **Apply the agent's expertise** to subsequent tasks in this session

## Pack Locations

```
.claude/agency-packs/
├── a11y/accessibility-auditor.md
├── perf/performance-benchmarker.md
├── security/security-engineer.md
├── database/database-optimizer.md
└── ux/ux-researcher.md
```

## Activation Response Template

When a pack is activated, respond with:

```
**{Pack Name} Activated**

I'll now apply {agent name} expertise to your tasks:
- {Capability 1}
- {Capability 2}
- {Capability 3}

<PROJECT> context loaded: {relevant <PROJECT> integrations}

What would you like me to help with?
```

## Example

User: `/use-pack a11y`

Response:
```
**Accessibility Pack Activated**

I'll now apply accessibility auditor expertise to your tasks:
- WCAG 2.2 AA compliance auditing
- Screen reader testing (VoiceOver, NVDA)
- React Aria component validation
- Keyboard navigation verification

<PROJECT> context loaded: React Aria Components, UUI semantic tokens, devProps standards

What would you like me to audit for accessibility?
```

## Error Handling

If pack name is invalid:

```
Unknown pack: {name}

Available packs:
- a11y: Accessibility auditing
- perf: Performance benchmarking
- security: Security engineering
- database: Database optimization
- ux: UX research

Usage: /use-pack <pack-name>
```
