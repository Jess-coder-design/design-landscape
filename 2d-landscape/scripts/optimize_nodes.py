"""
Strip unused fields from nodes.json to reduce file size
Keeps only the fields needed for rendering
"""
import json

# Load nodes
with open('data/nodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

# Check original size
import os
original_size = os.path.getsize('data/nodes.json') / 1024 / 1024  # MB

# Keep only essential fields for rendering
optimized_nodes = []
for node in nodes:
    optimized = {
        'url': node['url'],
        'sentence': node.get('sentence'),
        'highlighted_sentence': node.get('highlighted_sentence', []),
        'x': node['x'],
        'y': node['y'],
        'color': node['color']
    }
    optimized_nodes.append(optimized)

# Save optimized nodes
with open('data/nodes.json', 'w', encoding='utf-8') as f:
    json.dump(optimized_nodes, f, indent=2)

# Check new size
new_size = os.path.getsize('data/nodes.json') / 1024 / 1024  # MB
reduction = ((original_size - new_size) / original_size) * 100

print(f'✅ Optimized nodes.json')
print(f'  Original size: {original_size:.2f} MB')
print(f'  New size: {new_size:.2f} MB')
print(f'  Reduction: {reduction:.1f}%')
print(f'  Removed fields: design_keywords_found, critical_keywords_found, umap_x, umap_y, weights, designer, etc.')
