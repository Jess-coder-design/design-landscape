"""
Compute 3D UMAP embeddings for sentences containing keywords from keywords_precomputed.json
Only includes sentences that have at least one keyword.
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

print(f"Loaded {len(sentences_data)} sentences")

# ============================================================================
# STEP 2: Extract ALL keywords and contextual scores
# ============================================================================
print("Extracting all keywords...")

# Collect all keywords from all sections with proper scoring
all_keywords_dict = {}  # keyword -> score

# First, add contextual scores (these have explicit scores and are most important)
contextual_scores = keywords_precomputed.get("contextual_scores", {})
embedded_scores = contextual_scores.get("embeddedness_keywords", {})
speculative_scores = contextual_scores.get("speculative_keywords", {})

for keyword, score in embedded_scores.items():
    all_keywords_dict[keyword.lower()] = score

for keyword, score in speculative_scores.items():
    all_keywords_dict[keyword.lower()] = score

# Also extract keywords from the embedded_keywords, speculative_keywords, critique_keywords sections
# and map them to contextual scores
for section_name in ["embedded_keywords", "speculative_keywords", "critique_keywords"]:
    section = keywords_precomputed.get(section_name, {})
    for key_name, keyword_list in section.items():
        if isinstance(keyword_list, list):
            for keyword_variant in keyword_list:
                kw_lower = keyword_variant.lower()
                # If not already in dict from contextual_scores, try to map it
                if kw_lower not in all_keywords_dict:
                    # Try to find matching contextual score keyword
                    found_score = None
                    
                    # Check if key_name exists in contextual scores
                    if key_name.lower() in embedded_scores:
                        found_score = embedded_scores[key_name.lower()]
                    elif key_name.lower() in speculative_scores:
                        found_score = speculative_scores[key_name.lower()]
                    
                    # If not found, assign default based on section
                    if found_score is None:
                        if section_name == "embedded_keywords":
                            found_score = -0.5  # Default embedded
                        elif section_name == "speculative_keywords":
                            found_score = 0.5   # Default speculative
                        else:  # critique_keywords
                            found_score = 0.0   # Neutral
                    
                    all_keywords_dict[kw_lower] = found_score

print(f"Total keywords to search for: {len(all_keywords_dict)}")

# ============================================================================
# STEP 3: Find keywords in sentences and filter
# ============================================================================
print("Searching for keywords in sentences...")

def find_keywords_in_sentence(sentence):
    """
    Find all keywords in the sentence, counting occurrences.
    Returns list of found keywords (with duplicates if word appears multiple times) 
    and their average score.
    """
    sentence_lower = sentence.lower()
    
    # Sort by length (longest first) to handle multi-word phrases better
    sorted_keywords = sorted(all_keywords_dict.keys(), key=len, reverse=True)
    
    found_keywords = []
    score_sum = 0.0
    already_processed = set()  # Track which keywords we've already counted
    
    for keyword in sorted_keywords:
        if keyword in already_processed:
            continue
            
        try:
            if ' ' in keyword:  # Multi-word phrase
                # Count occurrences
                count = sentence_lower.count(keyword)
                if count > 0:
                    already_processed.add(keyword)
                    # Add keyword once for each occurrence
                    for _ in range(count):
                        found_keywords.append(keyword)
                        score_sum += all_keywords_dict[keyword]
            else:  # Single word
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = re.findall(pattern, sentence_lower)
                if matches:
                    already_processed.add(keyword)
                    # Add keyword once for each match
                    for _ in matches:
                        found_keywords.append(keyword)
                        score_sum += all_keywords_dict[keyword]
        except Exception as e:
            pass
    
    # Calculate average score
    avg_score = score_sum / len(found_keywords) if found_keywords else 0.0
    
    return found_keywords, avg_score

# Find keywords in all sentences and filter
filtered_sentences = []
keywords_list = []
scores_list = []

for i, sentence_data in enumerate(sentences_data):
    if i % 1000 == 0:
        print(f"  Processed {i}/{len(sentences_data)} sentences")
    
    sentence = sentence_data.get("sentence", "")
    found_keywords, avg_score = find_keywords_in_sentence(sentence)
    
    # ONLY include sentences with at least one keyword
    if found_keywords:
        filtered_sentences.append(sentence_data)
        keywords_list.append(found_keywords)
        scores_list.append(avg_score)

print(f"\nFiltered results:")
print(f"  Original sentences: {len(sentences_data)}")
print(f"  Sentences with keywords: {len(filtered_sentences)}")
print(f"  Percentage: {100*len(filtered_sentences)/len(sentences_data):.1f}%")

if len(filtered_sentences) == 0:
    print("ERROR: No sentences with keywords found!")
    exit(1)

# Create dataframe from filtered sentences
df = pd.DataFrame(filtered_sentences)
df["keywords_found"] = keywords_list
df["embedded_speculative"] = scores_list

print(f"\nKeyword score statistics:")
print(f"  Mean: {df['embedded_speculative'].mean():.3f}")
print(f"  Min: {df['embedded_speculative'].min():.3f}")
print(f"  Max: {df['embedded_speculative'].max():.3f}")

sentences = df["sentence"].tolist()

# ============================================================================
# STEP 4: Embed sentences using sentence transformer
# ============================================================================
print("\nComputing embeddings (this may take a few minutes)...")
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
# Map Z axis to the embedded_speculative scores (normalize to reasonable range)
# Scores range from -1.0 (embedded) to +1.0 (speculative)
df["z"] = df["embedded_speculative"] * 5  # Scale for visibility

print(f"UMAP complete")
print(f"  X range: [{df['x'].min():.2f}, {df['x'].max():.2f}]")
print(f"  Y range: [{df['y'].min():.2f}, {df['y'].max():.2f}]")
print(f"  Z range (embeddedness->speculation): [{df['z'].min():.2f}, {df['z'].max():.2f}]")

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
print(f"Done! {len(output_data)} points with keywords ready for Three.js")
