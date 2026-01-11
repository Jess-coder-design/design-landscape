# Folder Structure

## Root Level
- **chrome-extension/** - Chrome extension source code (content.js, manifest.json, styles, etc.)
- **landscape/** - D3.js landscape visualization website (HTML/CSS/JS)
- **scripts/** - Python utility scripts for data processing
- **data/** - JSON and CSV data files used by the application
- **reference/** - Reference documentation and color mapping files
- **highlight_keywords/** - (legacy/utility folder)
- **.venv/** - Python virtual environment

---

## Detailed Breakdown

### /chrome-extension
The Chrome extension that highlights keywords on webpages and enables navigation to the landscape.
- `manifest.json` - Extension configuration
- `content.js` - Main script that runs on webpages (keyword highlighting, ADD button)
- `popup.js`, `popup.html` - Extension popup UI
- `styles.css` - Styling for highlights
- `csv2.csv` - List of keywords (duplicated from data/)
- `designers.json` - Designer name database (duplicated from data/)

### /landscape
The D3.js visualization of design methodologies.
- `index.html` - Main visualization page
- `about.html` - About page
- `test_filter.html` - Testing/debugging page
- `csv2.csv` - Keywords reference (duplicated from data/)

### /scripts
Python utility scripts for data processing and validation:
- `add_url_to_landscape.py` - Add new URLs to the landscape database
- `check_keywords_on_pages.py` - Validate keyword presence on pages
- `check_capitalization.py` - Check text capitalization consistency
- `compute_umap_embeddings.py` - Compute UMAP coordinates for nodes
- `compute_umap_from_keywords.py` - Generate UMAP from keyword data
- `extract_sentences.py` - Extract sentences from documents
- `flip_umap_x.py` - Mirror UMAP X coordinates
- `generate_keyword_combinations.py` - Create keyword combinations
- `merge_analysis_to_umap.py` - Merge keyword analysis with UMAP
- `rebuild_keywords.py` - Rebuild keyword data structures
- `rebuild_nodes_from_keywords.py` - Regenerate nodes from keywords
- `debug_filter.py` - Debug filtering logic

### /data
All JSON and CSV data files:
- `nodes.json` - ⭐ **MAIN FILE** - Complete node data with UMAP coordinates and keywords (used by landscape visualization and scripts)
- `nodes_keywords.json` - Keywords-only version (intermediate processing file)
- `keywords_analysis.json` - ⭐ Keyword frequency and sentence data (used by landscape visualization)
- `designers.json` - Designer names and URLs
- `csv2.csv` - List of keywords

### /reference
Reference and documentation:
- `keyword_color_legend.html` - Visual legend showing all keywords and their colors
- `keyword_color_mapping.json` - Master mapping of keywords to hex colors
- `keywords.js` - JavaScript keyword definitions (legacy/reference)

---

## Which Files Are Used Where?

### Chrome Extension uses:
- `/data/designers.json` (copied to `/chrome-extension/designers.json`)
- `/data/csv2.csv` (copied to `/chrome-extension/csv2.csv`)

### Landscape uses:
- `/data/nodes_*.json` (nodes data)
- `/data/designers.json`
- `/data/csv2.csv`

### Scripts use:
- All files in `/data/` for processing and validation

---

## Notes

- **Actively Used Files** (marked with ⭐):
  - `nodes_with_umap_keywords.json` - Loaded by landscape visualization
  - `keywords_analysis.json` - Provides sentence data for landscape
- **Intermediate Processing Files**: Used by Python scripts when adding new URLs or regenerating data
- **CSV files** are duplicated in chrome-extension/ folder (required for web_accessible_resources)
- **designers.json** is also duplicated in chrome-extension/ folder
- Python scripts in `/scripts/` are utility functions for adding new content or validation
