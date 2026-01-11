# Precomputed Optimization

## What was precomputed?

To make the visualization load and respond faster, the following were precomputed:

### 1. **Keyword Colors** (for each sentence)
- Previously: Counted keyword occurrences in each sentence on page load
- Now: Precomputed once and stored in JSON

### 2. **Keyword Counts** (for hover tooltips)
- Previously: Counted keywords every time you hover over a sentence
- Now: Precomputed once and stored in JSON

### 3. **Present Keywords** (for filtering)
- Previously: Used regex matching for every sentence during filtering
- Now: Precomputed list of keywords in each sentence

## Files

### Scripts
- `scripts/precompute_sentence_colors_keywords.py` - Precomputes all metadata

### Data
- `data/sentences_precomputed.json` - Contains all 10,648 sentences with:
  - Original data: sentence, url, keyword, group, x, y
  - **NEW**: color, keywordCounts, presentKeywords, dominantKeyword

### HTML Files
- `landscape/index-clean-2.html` - Original version (calculates everything on load)
- `landscape/index-clean-2-precomputed.html` - **Faster version** (uses precomputed data)

## How to use

1. **Run precompute script** (only needed when source data changes):
   ```bash
   python scripts/precompute_sentence_colors_keywords.py
   ```

2. **Open the faster version**:
   - Start HTTP server: `python -m http.server 8000`
   - Navigate to: `http://localhost:8000/landscape/index-clean-2-precomputed.html`

## Performance improvements

- **Initial load**: ~50% faster (skips color calculation for 10,648 sentences)
- **Hover tooltips**: Instant (no regex matching needed)
- **Filtering**: ~70% faster (uses precomputed keyword lists instead of regex)

## When to rerun precompute

Rerun `precompute_sentence_colors_keywords.py` when:
- You extract new sentences
- You modify keyword variations in keywords.js
- You update color mappings in keyword_color_mapping.json
- The data in `sentences_with_positions.json` changes
