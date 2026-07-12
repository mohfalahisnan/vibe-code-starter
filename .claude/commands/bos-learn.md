# /bos-learn - Add Manual Memory

Add a memory manually to the <PROJECT> self-evolving memory system.

## Usage

```
/bos-learn <category> "title" "content"
```

## Arguments

| Argument   | Description                               |
| ---------- | ----------------------------------------- |
| `category` | Memory category (see below)               |
| `title`    | Short descriptive title (max 50 chars)    |
| `content`  | The memory to add (can be multi-sentence) |

## Categories

| Category      | Use For                                  |
| ------------- | ---------------------------------------- |
| `entities`    | People, services, APIs, external systems |
| `patterns`    | Recurring solutions and best practices   |
| `preferences` | User choices and project conventions     |
| `events`      | Significant milestones or decisions      |
| `cases`       | Bug fixes, edge cases, anti-patterns     |
| `profile`     | Meta-learnings about the user/project    |

## Examples

```
/bos-learn patterns "Debug Supabase RLS via JWT" "When debugging Supabase RLS, always check JWT claims first"
/bos-learn preferences "Explicit error messages" "User prefers explicit error messages over generic ones"
/bos-learn cases "useFormStatus requires form" "React 19 useFormStatus must be called inside a form component"
/bos-learn entities "Vercel MCP server" "Vercel MCP server handles deployments and logs"
```

## Behavior

1. Parse the category, title, and content from the command
2. Check for similar existing memories (deduplication threshold: 0.85)
3. If unique, add to the appropriate memory category
4. Update the category index.md file
5. Report success or explain why it was skipped

## Implementation

Execute this command to add the memory:

```bash
bunx tsx .bos/lib/memory-manager.ts add <category> "<title>" "<content>"
```

The memory-manager CLI will:

- Generate embeddings for deduplication
- Check for similar memories
- Add to SQLite database
- Update the markdown index file

## Example Output

**Success:**

```
✅ Memory added to patterns:
   Title: "Debug Supabase RLS via JWT claims"
   ID: patterns/debug-supabase-rls-via-jwt-claims
```

**Duplicate detected:**

```
⚠️ Similar memory exists (92% similar):
   "Check JWT claims for RLS debugging"
   Skipping to avoid duplication.
```

## When to Use

Use `/bos-learn` to manually capture:

- Insights from debugging sessions
- Project-specific conventions
- Integration details with external services
- Anti-patterns to avoid
- User preferences observed during work

Memories are automatically extracted from:

- Session transcripts (via SessionEnd hook)
- Git commits (via post-commit hook)

Use manual capture for insights that won't appear in commits or transcripts.

## Related

- `/bos-search` - Search memories and context
- `/bos-refresh` - Regenerate context cache
- `.bos/memory/` - Memory storage location
- `.bos/lib/memory-manager.ts` - Memory management implementation
