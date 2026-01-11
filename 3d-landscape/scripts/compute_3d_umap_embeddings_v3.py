"""
Compute 3D UMAP embeddings for sentences with embeddedness/speculation scoring.
Searches for ALL keywords from keywords_precomputed.json
"""

import json
import re
import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import umap

# ============================================================================
# STEP 1: Load sentences and keywords
# ============================================================================
print("Loading sentences...")

# Get the parent directory of the scripts folder
script_dir = Path(__file__).parent
root_dir = script_dir.parent

with open(root_dir / "data" / "sentences_with_positions.json", "r", encoding="utf-8") as f:
    sentences_data = json.load(f)

print("Loading keywords...")
with open(root_dir / "3DUMAP" / "data" / "keywords_precomputed.json", "r", encoding="utf-8") as f:
    keywords_precomputed = json.load(f)

df = pd.DataFrame(sentences_data)
sentences = df["sentence"].tolist()

print(f"Loaded {len(sentences)} sentences")

# ============================================================================
# STEP 2: Extract ALL keywords and contextual scores
# ============================================================================
print("Extracting all keywords...")

# Collect all keywords from all sections
all_keywords_dict = {}  # keyword -> score

# Add contextual scores (these have explicit scores)
contextual_scores = keywords_precomputed.get("contextual_scores", {})
embedded_scores = contextual_scores.get("embeddedness_keywords", {})
speculative_scores = contextual_scores.get("speculative_keywords", {})

for keyword, score in embedded_scores.items():
    all_keywords_dict[keyword.lower()] = score

for keyword, score in speculative_scores.items():
    all_keywords_dict[keyword.lower()] = score

# Also extract keywords from the embedded_keywords, speculative_keywords, critique_keywords sections
# (the sections with lists of keyword variations)
for section_name in ["embedded_keywords", "speculative_keywords", "critique_keywords"]:
    section = keywords_precomputed.get(section_name, {})
    for key_name, keyword_list in section.items():
        if isinstance(keyword_list, list):
            for keyword_variant in keyword_list:
                kw_lower = keyword_variant.lower()
                # If not already in dict, assign score based on category
                if kw_lower not in all_keywords_dict:
                    if section_name == "embedded_keywords":
                        all_keywords_dict[kw_lower] = -0.5  # Default embedded score
                    elif section_name == "speculative_keywords":
                        all_keywords_dict[kw_lower] = 0.5   # Default speculative score
                    else:  # critique_keywords
                        all_keywords_dict[kw_lower] = 0.0   # Neutral for critique

print(f"Total keywords to search for: {len(all_keywords_dict)}")
print(f"Sample keywords: {list(all_keywords_dict.keys())[:10]}")

# ============================================================================
# STEP 3: Find keywords in sentences
# ============================================================================
print("Searching for keywords in sentences...")

def find_keywords_in_sentence(sentence):
    """
    Find all keywords in the sentence.
    Returns list of found keywords and their average score.
    """
    sentence_lower = sentence.lower()
    
    # Sort by length (longest first) to handle multi-word phrases better
    sorted_keywords = sorted(all_keywords_dict.keys(), key=len, reverse=True)
    
    found_keywords = []
    score_sum = 0.0
    matched_set = set()
    
    for keyword in sorted_keywords:
        if keyword in matched_set:
            continue
            
        try:
            if ' ' in keyword:  # Multi-word phrase
                if keyword in sentence_lower:
                    matched_set.add(keyword)
                    found_keywords.append(keyword)
                    score_sum += all_keywords_dict[keyword]
            else:  # Single word
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, sentence_lower):
                    matched_set.add(keyword)
                    found_keywords.append(keyword)
                    score_sum += all_keywords_dict[keyword]
        except Exception as e:
            pass
    
    # Calculate average score
    avg_score = score_sum / len(found_keywords) if found_keywords else 0.0
    
    return found_keywords, avg_score

# Apply keyword finding to all sentences
keywords_list = []
scores_list = []

for i, s in enumerate(sentences):
    if i % 1000 == 0:
        print(f"  Processed {i}/{len(sentences)} sentences")
    found_keywords, avg_score = find_keywords_in_sentence(s)
    keywords_list.append(found_keywords)
    scores_list.append(avg_score)

# Add to dataframe
df["keywords_found"] = keywords_list
df["embedded_speculative"] = scores_list

print(f"Keywords found in sentences")
print(f"  Mean: {df['embedded_speculative'].mean():.3f}")
print(f"  Min: {df['embedded_speculative'].min():.3f}")
print(f"  Max: {df['embedded_speculative'].max():.3f}")

# ============================================================================
# STEP 4: Embed sentences using sentence transformer
# ============================================================================
print("Computing embeddings (this may take a few minutes)...")
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(sentences, show_progress_bar=True)

print(f"Embeddings shape: {embeddings.shape}")

# ============================================================================
# STEP 5: Run 3D UMAP
# ============================================================================
print("Running 3D UMAP...")
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

print(f"UMAP complete")
print(f"  X range: [{df['x'].min():.2f}, {df['x'].max():.2f}]")
print(f"  Y range: [{df['y'].min():.2f}, {df['y'].max():.2f}]")
print(f"  Z range: [{df['z'].min():.2f}, {df['z'].max():.2f}]")

# ============================================================================
# STEP 6: Export for browser
# ============================================================================
print("Exporting data...")

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

print(f"Exported to {output_path}")
print(f"Done! {len(output_data)} points ready for Three.js")
