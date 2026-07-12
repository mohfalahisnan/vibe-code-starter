# /bos-sync-karimo - Sync KARIMO Artifacts

Sync KARIMO learnings and PRD artifacts to the <PROJECT> context and memory systems.

## Usage

```
/bos-sync-karimo [--all] [--learnings] [--prds]
```

## Arguments

| Argument      | Description                            |
| ------------- | -------------------------------------- |
| `--all`       | Sync both learnings and PRDs (default) |
| `--learnings` | Sync only KARIMO learnings to memories |
| `--prds`      | Sync only PRD documents to context     |

## What Gets Synced

### Learnings → Memories

KARIMO learnings are synced to <PROJECT> memories with the following category mapping:

| KARIMO Category   | <PROJECT> Category  |
| ----------------- | ------------- |
| `patterns`        | `patterns`    |
| `anti-patterns`   | `cases`       |
| `project-notes`   | `preferences` |
| `execution-rules` | `patterns`    |

### PRDs → Context Embeddings

PRD documents are embedded as L1 context entries:

- `PRD_*.md` → `bos://karimo/prd/{slug}`
- `findings.md` → `bos://karimo/prd/{slug}/findings`

## Behavior

1. Parse the sync target from arguments
2. For learnings:
   - Read all category index files from `.karimo/learnings/`
   - Check for duplicates in memory system (0.9 similarity threshold)
   - Add new learnings with `source: 'karimo'`
3. For PRDs:
   - Scan all PRD directories in `.karimo/prds/`
   - Compare content hashes to detect changes
   - Embed and store new/updated PRDs

## Implementation

Execute this command to sync:

```bash
# Sync all
bunx tsx .bos/scripts/sync-karimo.ts --all

# Sync only learnings
bunx tsx .bos/scripts/sync-karimo.ts --learnings

# Sync only PRDs
bunx tsx .bos/scripts/sync-karimo.ts --prds
```

## Example Output

```
🔄 <PROJECT> KARIMO Sync

📖 Syncing KARIMO learnings...

   ✅ New pattern added

Learnings:
   Total: 19
   Added: 1
   Updated: 0
   Skipped: 18

📄 Syncing KARIMO PRDs...

   ✅ Added: 005_new-feature
   🔄 Updated: 001_brand-color-studio

PRDs:
   Total: 5
   Added: 1
   Updated: 1
   Skipped: 3

✅ Sync complete
```

## When to Use

Run `/bos-sync-karimo` when:

- After completing a KARIMO execution (PRD learnings are generated)
- After adding new learnings to `.karimo/learnings/`
- After creating or modifying PRD documents
- Periodically to keep <PROJECT> in sync with KARIMO state

## First-Time Migration

For initial migration of existing learnings, use:

```bash
bunx tsx .bos/scripts/migrate-learnings.ts
```

This performs a one-time import of all existing KARIMO learnings.

## Related

- `/bos-search` - Search synced content
- `/bos-learn` - Add manual memories
- `.karimo/learnings/` - KARIMO learnings source
- `.karimo/prds/` - KARIMO PRD source
