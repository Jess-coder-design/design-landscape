"""
Add position data from landscape_data.json to nodes.json
"""
import json

print("Loading landscape_data.json...")
with open('data/landscape_data.json', 'r', encoding='utf-8') as f:
    landscape = json.load(f)

print("Loading nodes.json...")
with open('data/nodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

print(f"\nProcessing {len(nodes)} nodes...")

# Create URL to position mapping
url_to_position = {}
for pos in landscape['positions']:
    url_to_position[pos['url']] = {
        'x': pos['umap_x'],
        'y': pos['umap_y']
    }

# Update nodes with positions
positioned = 0
not_positioned = 0

for i, node in enumerate(nodes):
    url = node.get('url')
    
    if url and url in url_to_position:
        node['x'] = url_to_position[url]['x']
        node['y'] = url_to_position[url]['y']
        positioned += 1
    else:
        # Keep existing x, y if present, or set to None
        if 'x' not in node:
            node['x'] = None
        if 'y' not in node:
            node['y'] = None
        not_positioned += 1
    
    # Progress indicator
    if (i + 1) % 50 == 0:
        print(f"  Processed {i + 1}/{len(nodes)} nodes...")

# Save updated nodes
print("\nSaving updated nodes.json...")
with open('data/nodes.json', 'w', encoding='utf-8') as f:
    json.dump(nodes, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"✓ Position update complete!")
print(f"  Total nodes: {len(nodes)}")
print(f"  With positions: {positioned} ({positioned/len(nodes)*100:.1f}%)")
print(f"  Without positions: {not_positioned} ({not_positioned/len(nodes)*100:.1f}%)")
print(f"{'='*60}")

# Show some examples
print("\nSample nodes with positions:")
examples = [n for n in nodes if n.get('x') is not None][:3]
for i, node in enumerate(examples, 1):
    print(f"\n[{i}] {node.get('url', 'No URL')}")
    print(f"    Position: ({node['x']:.4f}, {node['y']:.4f})")
    print(f"    Keywords: {', '.join(node.get('keywords', [])[:5])}")
