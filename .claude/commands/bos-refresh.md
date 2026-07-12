# /bos-refresh - Regenerate <PROJECT> Context Cache

Regenerate the L0/L1 context summaries in `.bos/context/`.

## Usage

```
/bos-refresh [--all] [--section <name>]
```

## Arguments

| Argument           | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| `--all`            | Regenerate all sections (default)                                |
| `--section <name>` | Regenerate specific section: `architecture`, `components`, `lib` |

## Behavior

1. Run the context generator script:

   ```bash
   bunx tsx .bos/scripts/generate-context.ts
   ```

2. Report what was regenerated:
   - Number of L1 sections updated
   - Total files analyzed
   - Git commit hash

3. Show cache freshness from `manifest.json`

## Output Files

The command regenerates:

```
.bos/context/
├── index.md                 # L0: Project overview (~500 tokens)
├── architecture/
│   ├── index.md             # L1: Architecture overview
│   ├── app-router.md        # L1: Next.js routing patterns
│   └── data-flow.md         # L1: Data flow patterns
├── components/
│   ├── index.md             # L1: Component library overview
│   ├── ui.md                # L1: Design system primitives
│   └── chat.md              # L1: Chat components
├── lib/
│   ├── index.md             # L1: Core libraries overview
│   ├── ai.md                # L1: AI provider system
│   └── supabase.md          # L1: Database services
└── manifest.json            # Cache metadata
```

## When to Use

Run `/bos-refresh` when:

- Starting a new feature that touches multiple areas
- After significant codebase changes
- When context feels stale or inaccurate
- Periodically during development sessions

## Implementation

```bash
# Run the generator
bunx tsx .bos/scripts/generate-context.ts

# Check freshness
cat .bos/context/manifest.json | jq '.generatedAt, .gitCommit'
```

## Related

- `.claude/reference/context-layers.md` - L0/L1/L2 model explanation
- `.bos/scripts/generate-context.ts` - Generator implementation
- `/bos-search` - Search context with vector similarity (Phase B2)
