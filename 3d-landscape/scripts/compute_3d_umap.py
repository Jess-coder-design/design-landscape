#!/usr/bin/env python3
"""
Compute 3D UMAP layout for critical design sentences.
Lightweight version using TF-IDF instead of neural embeddings.
Follows PAIR/Fashion-UMAP pattern.
"""

import json
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import umap

# ============================================================================
# STEP 1: Load data
# ============================================================================

print("=" * 70)
print("COMPUTING 3D UMAP LAYOUT")
print("=" * 70)

sentences_path = Path("data/sentences_with_positions.json")
keywords_path = Path("data/keywords.json")

with open(sentences_path, "r", encoding="utf-8") as f:
    sentences_data = json.load(f)

with open(keywords_path, "r", encoding="utf-8") as f:
    keywords_data = json.load(f)

print(f"\n✓ Loaded {len(sentences_data)} sentences")

# ============================================================================
# STEP 2: Create embeddings using TF-IDF
# ============================================================================

print("\nComputing TF-IDF embeddings...")

sentences_list = [d["sentence"] for d in sentences_data]

vectorizer = TfidfVectorizer(
    max_features=384,
    min_df=2,
    max_df=0.8,
    ngram_range=(1, 2)
)

embeddings = vectorizer.fit_transform(sentences_list).toarray()
print(f"✓ Embeddings shape: {embeddings.shape}")

# ============================================================================
# STEP 3: Compute embeddedness ↔ speculation scores
# ============================================================================

# ============================================================================
# STEP 3: Compute embeddedness ↔ speculation scores
# ============================================================================

print("\nScoring embeddedness vs speculation...")

embedded_keywords = []
speculative_keywords = []

# Extract keywords from JSON
# EMBEDDED: Context-based, grounded keywords
for group_name, keywords_list in keywords_data.get("context_keywords_found", {}).items():
    if isinstance(keywords_list, list):
        embedded_keywords.extend(keywords_list)

# SPECULATIVE: Design/futures-oriented keywords
for group_name, keywords_list in keywords_data.get("design_keywords_found", {}).items():
    if isinstance(keywords_list, list):
        speculative_keywords.extend(keywords_list)

# NOTE: Critique keywords are kept separate and NOT used in embedded_speculative scoring
# They are tracked separately as a third dimension

embedded_keywords = list(set([kw.lower() for kw in embedded_keywords]))
speculative_keywords = list(set([kw.lower() for kw in speculative_keywords]))

print(f"✓ Embedded keywords (context-based): {len(embedded_keywords)}")
print(f"✓ Speculative keywords (design/futures): {len(speculative_keywords)}")

# Create regex patterns for word boundary matching
def count_keyword_occurrences(sentence, keywords):
    """Count keyword occurrences using word boundaries"""
    sentence_lower = sentence.lower()
    count = 0
    for kw in keywords:
        # Use word boundaries to match whole words
        pattern = r'\b' + re.escape(kw) + r'\b'
        matches = re.findall(pattern, sentence_lower)
        count += len(matches)
    return count

embedded_speculative_scores = []
for d in sentences_data:
    sentence = d["sentence"]
    
    # Count keyword occurrences with proper word boundaries
    embedded_count = count_keyword_occurrences(sentence, embedded_keywords)
    speculative_count = count_keyword_occurrences(sentence, speculative_keywords)
    
    total = embedded_count + speculative_count
    if total == 0:
        score = 0.5
    else:
        score = speculative_count / total
    
    embedded_speculative_scores.append(score)

print(f"✓ Scored {len(embedded_speculative_scores)} sentences")

# ============================================================================
# STEP 4: Run 3D UMAP
# ============================================================================

print("\nRunning 3D UMAP reduction...")
umap_3d = umap.UMAP(
    n_components=3,
    n_neighbors=15,
    min_dist=0.1,
    metric="cosine",
    random_state=42,
    verbose=True
)

coordinates_3d = umap_3d.fit_transform(embeddings)
print(f"✓ 3D coordinates computed: {coordinates_3d.shape}")

# ============================================================================
# STEP 5: Export to JSON
# ============================================================================

print("\nExporting to JSON...")

output_data = []
for i, d in enumerate(sentences_data):
    output_data.append({
        "sentence": d["sentence"],
        "url": d["url"],
        "keyword": d["keyword"],
        "embedded_speculative": float(embedded_speculative_scores[i]),
        "x": float(coordinates_3d[i, 0]),
        "y": float(coordinates_3d[i, 1]),
        "z": float(coordinates_3d[i, 2])
    })

output_path = Path("3DUMAP/data/umap_3d_data.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f)

file_size_mb = output_path.stat().st_size / 1024 / 1024
print(f"✓ Exported {len(output_data)} points to {output_path}")
print(f"✓ File size: {file_size_mb:.2f} MB")

print("\n" + "=" * 70)
print("✓ DONE! Ready to visualize in browser.")
print("  Open: 3d-landscape/index.html")
print("=" * 70)
