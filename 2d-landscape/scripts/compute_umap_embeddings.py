"""
Compute UMAP embeddings for design landscape nodes based on keywords
"""
import json
import numpy as np
import umap
from sklearn.preprocessing import StandardScaler
from pathlib import Path

# Load nodes data
with open('data/nodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

# All 35 keywords (17 design + 18 critical)
ALL_KEYWORDS = {
    # Design keywords
    "design", "method", "making", "applied art", "intention", "plan", 
    "research", "tool", "inquiry", "practice", "work", "concept", 
    "craft", "exploration", "engineering", "shape", "project",
    # Critical keywords
    "critical", "conceptual", "analytical", "deconstructive", "collaborative",
    "interdisciplinary", "contextual", "iterative", "reflective", "theoretical",
    "evaluative", "investigative", "explorative", "dialectical", "discursive",
    "reflexive", "narrative", "speculative", "systemic"
}

# Create keyword occurrence vectors
weight_vectors = []

for node in nodes:
    # Count occurrences of each keyword in design and critical keywords found
    vector = []
    design_kw = node.get('design_keywords_found', {})
    critical_kw = node.get('critical_keywords_found', {})
    
    for keyword in sorted(ALL_KEYWORDS):
        # Count occurrences in design keywords
        if keyword in design_kw:
            count = len(design_kw[keyword])
        elif keyword in critical_kw:
            count = len(critical_kw[keyword])
        else:
            count = 0
        vector.append(count)
    
    weight_vectors.append(vector)

# Convert to numpy array and normalize using StandardScaler
X = np.array(weight_vectors, dtype=float)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Computing UMAP embeddings for {len(nodes)} nodes with {X_scaled.shape[1]} features...")

# Compute UMAP with parameters that work well for design landscapes
# n_neighbors: how many local neighbors to consider (lower = more local structure)
# min_dist: minimum distance between points (lower = more clumped)
# metric: distance metric (correlation works well for normalized weights)
reducer = umap.UMAP(
    n_components=2,
    n_neighbors=15,
    min_dist=0.1,
    metric='cosine',
    random_state=42,
    verbose=1
)

embeddings = reducer.fit_transform(X_scaled)

# Normalize embeddings to [0, 1] range for consistent positioning
embeddings_min = embeddings.min(axis=0)
embeddings_max = embeddings.max(axis=0)
embeddings_normalized = (embeddings - embeddings_min) / (embeddings_max - embeddings_min)

# Add embeddings to nodes
for i, node in enumerate(nodes):
    node['umap_x'] = float(embeddings_normalized[i, 0])
    node['umap_y'] = float(embeddings_normalized[i, 1])

# Save updated nodes with UMAP coordinates
output_path = 'data/nodes.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(nodes, f, indent=2)

print(f"✓ Saved embeddings to {output_path}")
print(f"  X range: [{embeddings_normalized[:, 0].min():.3f}, {embeddings_normalized[:, 0].max():.3f}]")
print(f"  Y range: [{embeddings_normalized[:, 1].min():.3f}, {embeddings_normalized[:, 1].max():.3f}]")
