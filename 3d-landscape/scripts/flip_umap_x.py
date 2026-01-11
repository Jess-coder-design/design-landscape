import json

# Load the existing UMAP data
with open('landscape/nodes_with_umap_keywords.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

# Flip X coordinates
for node in nodes:
    if 'umap_x' in node:
        node['umap_x'] = -node['umap_x']

# Save back
with open('landscape/nodes_with_umap_keywords.json', 'w', encoding='utf-8') as f:
    json.dump(nodes, f, indent=2)

print(f"✓ Flipped X-axis for {len(nodes)} nodes")
print("✓ FUTURE is now on the right, PAST is now on the left")
