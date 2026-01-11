# Critical Design UMAP - 3D Visualization

This implements a 3D UMAP visualization of critical design sentences, following the PAIR/Fashion-UMAP pattern.

## PART 1: Compute Embeddings & 3D UMAP

### Step 1: Install dependencies (if not already installed)
```bash
pip install sentence-transformers umap-learn pandas scikit-learn
```

### Step 2: Run the computation script
```bash
python scripts/compute_3d_umap.py
```

This will:
1. Load 10,000+ sentences from `data/sentences_with_positions.json`
2. Embed them using SentenceTransformer (384D semantic vectors)
3. Compute embeddedness ↔ speculation scores for each sentence
4. Run 3D UMAP to create layout
5. Export to `3DUMAP/data/umap_3d_data.json`

**Output**: `umap_3d_data.json` with columns:
- `sentence` - The text
- `url` - Source URL
- `keyword` - Associated keyword
- `embedded_speculative` - Score (0.0 = embedded, 1.0 = speculative)
- `x`, `y`, `z` - 3D coordinates from UMAP

## PART 2: Interactive 3D Visualization

### Open in browser
```
3d-landscape/index.html
```

### Features

**Visual Design:**
- Color gradient: Blue (embedded) ↔ Red (speculative)
- 3D points represent semantic structure
- Distance = semantic similarity

**Interaction:**
- **Left-click + drag**: Rotate the view
- **Scroll**: Zoom in/out
- **Right-click + drag**: Pan camera
- **Hover**: Show sentence text and metadata

**Controls:**
- Toggle labels (placeholder for future enhancement)
- Adjust point size

**Panels:**
- **Info Panel** (top-left): Explanation
- **Legend** (top-right): Color scale
- **Options** (bottom-right): UI controls
- **Sentence Display** (bottom-left): Hovers to show text

## Architecture

```
Sentences (10K+)
    ↓
[SentenceTransformer] → Embeddings (384D)
    ↓
[Score Function] → embeddedness ↔ speculation (0.0-1.0)
    ↓
[UMAP] → 3D coordinates (x, y, z)
    ↓
[Three.js] → Interactive 3D visualization
    ↓
Colors = embeddedness spectrum
```

### Key Design Decisions

1. **ONE UMAP only** - No stacking or projection tricks
2. **Semantic embeddings** - Not spatial embeddings (unlike 2D UMAP)
3. **x, y, z have no individual meaning** - Only distances and clusters matter
4. **Color as visual attribute** - Embeddedness/speculation mapped to HSL hue
5. **Interactive, not prescriptive** - Viewers can explore and form own interpretations

## Data Format

`umap_3d_data.json`:
```json
[
  {
    "sentence": "Critical design challenges dominant narratives...",
    "url": "https://example.com",
    "keyword": "critical",
    "embedded_speculative": 0.25,
    "x": 12.45,
    "y": -8.92,
    "z": 3.21
  },
  ...
]
```

## Customization

### Adjust embedding model
Edit `scripts/compute_3d_umap.py`:
```python
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")  # Larger, slower
# or
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")   # Smaller, faster
```

### Adjust UMAP parameters
```python
umap_3d = umap.UMAP(
    n_components=3,
    n_neighbors=15,      # More = global structure
    min_dist=0.1,        # Less = tighter clusters
    metric="cosine",
    random_state=42
)
```

### Adjust color scale
In `index.html`:
```javascript
const hue = (1 - d.embedded_speculative) * 0.6;  // 0.6 = blue, 0 = red
c.setHSL(hue, saturation, lightness);
```

## Bonus: Future Enhancements

As suggested in the brief:
- [ ] Toggle "color by embeddedness" vs "color by keyword family"
- [ ] Live re-weighting of keywords
- [ ] Show sentence text on hover (✓ implemented)
- [ ] Allow users to misclassify/annotate points
- [ ] Export annotations back to JSON

---

**Pattern**: Fashion-UMAP (PAIR) adapted for critical design discourse
