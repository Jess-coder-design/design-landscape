import json
import numpy as np
from collections import defaultdict
from umap import UMAP

# Load the nodes with keywords data
with open('data/nodes_keywords.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

# Load keywords analysis to extract all actual keyword combinations
with open('landscape/keywords_analysis.json', 'r', encoding='utf-8') as f:
    keywords_data = json.load(f)

print(f"Total nodes: {len(nodes)}")

# Build a comprehensive keyword dictionary from all combinations found
keyword_combinations = defaultdict(int)

for result in keywords_data.get('results', []):
    analysis = result.get('analysis')
    if not analysis:
        continue
    
    # Count all design keywords found
    design_keywords = analysis.get('design_keywords_found', {})
    for category, words in design_keywords.items():
        for word in words:
            keyword_combinations[word] += 1
    
    # Count all critical keywords found
    critical_keywords = analysis.get('critical_keywords_found', {})
    for category, words in critical_keywords.items():
        for word in words:
            keyword_combinations[word] += 1

# Sort by frequency and create feature list
sorted_keywords = sorted(keyword_combinations.items(), key=lambda x: x[1], reverse=True)
feature_keywords = [kw for kw, count in sorted_keywords]

print(f"Total unique keywords found: {len(feature_keywords)}")
print(f"Top 20 keywords: {feature_keywords[:20]}")

# Create embeddings for each node based on keyword presence
embeddings = []
node_urls = []

for node in nodes:
    url = node['url']
    analysis_data = None
    
    # Find the corresponding analysis for this node
    for result in keywords_data.get('results', []):
        if result['url'] == url:
            analysis_data = result.get('analysis')
            break
    
    # Create embedding vector
    embedding = np.zeros(len(feature_keywords))
    
    if analysis_data:
        # Get all keywords for this node
        found_keywords = set()
        
        design_keywords = analysis_data.get('design_keywords_found', {})
        for category, words in design_keywords.items():
            for word in words:
                found_keywords.add(word)
        
        critical_keywords = analysis_data.get('critical_keywords_found', {})
        for category, words in critical_keywords.items():
            for word in words:
                found_keywords.add(word)
        
        # Set embedding dimensions for found keywords
        for i, keyword in enumerate(feature_keywords):
            if keyword in found_keywords:
                embedding[i] = 1.0
    
    embeddings.append(embedding)
    node_urls.append(url)

# Convert to numpy array
embeddings_array = np.array(embeddings)
print(f"Embedding shape: {embeddings_array.shape}")

# Generate UMAP coordinates
print("\nGenerating UMAP embeddings...")
umap_model = UMAP(n_components=2, random_state=42, n_neighbors=15, min_dist=0.1)
umap_coordinates = umap_model.fit_transform(embeddings_array)

print(f"UMAP coordinates shape: {umap_coordinates.shape}")

# Create output nodes with UMAP coordinates
output_nodes = []

for i, node in enumerate(nodes):
    new_node = {
        'url': node['url'],
        'sentence': node['sentence'],
        'design_keywords_found': node['design_keywords_found'],
        'critical_keywords_found': node['critical_keywords_found'],
        'direct_phrase_combinations': node['direct_phrase_combinations'],
        'conditions_met': node['conditions_met'],
        'weights': node['weights'],
        'designer': node['designer'],
        'designer_url': node['designer_url'],
        'umap_x': float(umap_coordinates[i][0]),
        'umap_y': float(umap_coordinates[i][1]),
        'embedding_keywords': feature_keywords
    }
    output_nodes.append(new_node)

# Save the result
with open('landscape/nodes_with_umap_keywords.json', 'w', encoding='utf-8') as f:
    json.dump(output_nodes, f, ensure_ascii=False, indent=2)

print(f"\n✓ Saved {len(output_nodes)} nodes with UMAP coordinates to nodes_with_umap_keywords.json")

# Print sample
print("\nFirst 3 nodes with UMAP coordinates:")
for i in range(min(3, len(output_nodes))):
    node = output_nodes[i]
    print(f"\n{i+1}. {node['url'][:60]}")
    print(f"   UMAP: ({node['umap_x']:.3f}, {node['umap_y']:.3f})")
    print(f"   Keywords: {len(node['design_keywords_found'])} design + {len(node['critical_keywords_found'])} critical")
