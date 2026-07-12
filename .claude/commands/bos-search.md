# /bos-search - Search Codebase Context

Search the <PROJECT> context cache using semantic similarity.

## Usage

```
/bos-search "your natural language query"
```

## Arguments

| Argument        | Description                                   |
| --------------- | --------------------------------------------- |
| `query`         | Natural language search query                 |
| `--top-k N`     | Number of results to return (default: 5)      |
| `--threshold N` | Minimum similarity 0-1 (default: 0.5)         |
| `--stats`       | Show database statistics instead of searching |

## Examples

```bash
# Search for chat-related context
/bos-search "how does chat streaming work"

# Get more results with lower threshold
/bos-search "database services" --top-k 10 --threshold 0.3

# Check database status
/bos-search --stats
```

## Output

Returns ranked results with:

- **Title**: Section heading
- **URI**: `bos://context/...` identifier
- **Layer**: L0 (overview), L1 (section), or L2 (source)
- **Similarity**: Match percentage (higher is better)
- **Content**: Excerpt from the matching section

## Prerequisites

Before first use, initialize the search database:

```bash
# 1. Generate context files
bunx tsx .bos/scripts/generate-context.ts

# 2. Initialize SQLite database
bunx tsx .bos/scripts/init-db.ts

# 3. Set your Gemini API key in .env.local
echo "GOOGLE_GENERATIVE_AI_API_KEY=your-key-here" >> .env.local

# 4. Embed context (requires API key)
GOOGLE_GENERATIVE_AI_API_KEY=your-key npx tsx .bos/scripts/embed-context.ts
```

## Environment Variables

| Variable                       | Purpose                                     |
| ------------------------------ | ------------------------------------------- |
| `GOOGLE_GENERATIVE_AI_API_KEY` | Google AI API key for embeddings (required) |
| `GEMINI_API_KEY`               | Alternative API key name                    |

**Get an API key**: Visit https://aistudio.google.com/app/apikey to create a free Gemini API key.

## Implementation

```bash
# Direct CLI usage
bunx tsx .bos/lib/search-context.ts "your query"

# With options
bunx tsx .bos/lib/search-context.ts "query" --top-k 10 --threshold 0.3

# Check stats
bunx tsx .bos/lib/search-context.ts --stats
```

## How It Works

1. **Query Embedding**: Your query is embedded using Gemini's `text-embedding-004` model
2. **Vector Search**: SQLite with sqlite-vec performs cosine similarity search
3. **Ranking**: Results are ordered by similarity score
4. **Filtering**: Results below threshold are excluded

## When to Use

Use `/bos-search` when:

- Looking for specific functionality in the codebase
- Need to understand how a feature works
- Want relevant context before making changes
- Exploring unfamiliar parts of the codebase

## Related

- `/bos-refresh` - Regenerate context cache (run before embedding)
- `.claude/reference/context-layers.md` - L0/L1/L2 model documentation
- `.bos/scripts/` - Underlying scripts
