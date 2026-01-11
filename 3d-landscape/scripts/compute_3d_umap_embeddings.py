"""
Compute 3D UMAP embeddings for sentences with embeddedness/speculation scoring.
Follows the PAIR/Fashion-UMAP pattern exactly.
"""

import json
import re
import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import umap

# ============================================================================
# STEP 1: Load sentences and contextual scores
# ============================================================================
print("Loading sentences...")

# Get the parent directory of the scripts folder
script_dir = Path(__file__).parent
root_dir = script_dir.parent

with open(root_dir / "data" / "sentences_with_positions.json", "r", encoding="utf-8") as f:
    sentences_data = json.load(f)

print("Loading contextual scores...")
with open(root_dir / "3DUMAP" / "data" / "keywords_precomputed.json", "r", encoding="utf-8") as f:
    keywords_precomputed = json.load(f)

df = pd.DataFrame(sentences_data)
sentences = df["sentence"].tolist()

print(f"✓ Loaded {len(sentences)} sentences")

# ============================================================================
# STEP 2: Embed sentences using sentence transformer
# ============================================================================
print("🧠 Computing embeddings (this may take a few minutes)...")
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(sentences, show_progress_bar=True)

print(f"✓ Embeddings shape: {embeddings.shape}")

# ============================================================================
# STEP 3: Compute embeddedness ↔ speculation score using contextual scores
# ============================================================================
print("📊 Computing embeddedness/speculation scores...")

# Extract keyword to score mappings from contextual_scores
contextual_scores = keywords_precomputed.get("contextual_scores", {})

embedded_scores = contextual_scores.get("embeddedness_keywords", {})
speculative_scores = contextual_scores.get("speculative_keywords", {})

# Create normalized keyword lists for matching (handle multi-word keywords)
embedded_keywords_dict = {}  # keyword -> score
speculative_keywords_dict = {}  # keyword -> score

for keyword, score in embedded_scores.items():
    embedded_keywords_dict[keyword.lower()] = score

for keyword, score in speculative_scores.items():
    speculative_keywords_dict[keyword.lower()] = score

print(f"✓ Loaded {len(embedded_keywords_dict)} embedded keywords")
print(f"✓ Loaded {len(speculative_keywords_dict)} speculative keywords")

def score_sentence(sentence):
    """
    Find all contextual keywords in the sentence.
    Returns list of keywords and their average score.
    """
    sentence_lower = sentence.lower()
    
    # Check for multi-word phrases first (longest match wins)
    all_keywords = list(embedded_keywords_dict.keys()) + list(speculative_keywords_dict.keys())
    all_keywords.sort(key=len, reverse=True)  # Check longest phrases first
    
    found_keywords = []
    score_sum = 0
    matched_set = set()
    
    for keyword in all_keywords:
        if keyword in matched_set:
            continue
            
        # Try to find the keyword in the sentence
        try:
            if ' ' in keyword:  # Multi-word phrase - just do substring check
                if keyword in sentence_lower:
                    matched_set.add(keyword)
                    if keyword in embedded_keywords_dict:
                        score = embedded_keywords_dict[keyword]
                    else:
                        score = speculative_keywords_dict[keyword]
                    found_keywords.append(keyword)
                    score_sum += score
            else:  # Single word - use word boundaries
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, sentence_lower):
                    matched_set.add(keyword)
                    if keyword in embedded_keywords_dict:
                        score = embedded_keywords_dict[keyword]
                    else:
                        score = speculative_keywords_dict[keyword]
                    found_keywords.append(keyword)
                    score_sum += score
        except:
            pass
    
    # Calculate average score
    avg_score = score_sum / len(found_keywords) if found_keywords else 0.0
    
    return found_keywords, avg_score

# Score each sentence and extract keywords
keywords_list = []
scores_list = []

for s in sentences:
    found_keywords, avg_score = score_sentence(s)
    keywords_list.append(found_keywords)
    scores_list.append(avg_score)

# Add to dataframe
df["keywords_found"] = keywords_list
df["embedded_speculative"] = scores_list

print(f"✓ Scores computed")
print(f"  Mean: {df['embedded_speculative'].mean():.3f}")
print(f"  Min: {df['embedded_speculative'].min():.3f}")
print(f"  Max: {df['embedded_speculative'].max():.3f}")

# ============================================================================
# STEP 4: Run 3D UMAP
# ============================================================================
print("🗺️ Running 3D UMAP...")
umap_3d = umap.UMAP(
    n_components=3,
    n_neighbors=15,
    min_dist=0.1,
    metric="cosine",
    random_state=42
)

coords = umap_3d.fit_transform(embeddings)

df["x"] = coords[:, 0]
df["y"] = coords[:, 1]
df["z"] = coords[:, 2]

print(f"✓ UMAP complete")
print(f"  X range: [{df['x'].min():.2f}, {df['x'].max():.2f}]")
print(f"  Y range: [{df['y'].min():.2f}, {df['y'].max():.2f}]")
print(f"  Z range: [{df['z'].min():.2f}, {df['z'].max():.2f}]")

# ============================================================================
# STEP 5: Export for browser
# ============================================================================
print("💾 Exporting data...")

# Select and order columns for export
export_cols = [
    "sentence", "url", "keywords_found", "group", 
    "x", "y", "z", "embedded_speculative"
]

output_data = df[export_cols].copy()
# Rename keywords_found to keyword for output
output_data.rename(columns={"keywords_found": "keyword"}, inplace=True)
output_data = output_data.to_dict(orient="records")

output_path = root_dir / "3DUMAP" / "data" / "umap_3d_data.json"
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"✓ Exported to {output_path}")
print(f"✅ Done! {len(output_data)} points ready for Three.js")
