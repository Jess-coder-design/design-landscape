"""
Scale positions in nodes.json to proper visualization coordinates
"""
import json

print("Loading landscape_data.json for metadata...")
with open('data/landscape_data.json', 'r', encoding='utf-8') as f:
    landscape = json.load(f)

print("Loading nodes.json...")
with open('data/nodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

# Get SVG dimensions from metadata
svg_width = landscape['metadata']['svg']['width']
svg_height = landscape['metadata']['svg']['height']
margin_x = landscape['metadata']['svg']['marginX']
margin_y = landscape['metadata']['svg']['marginY']

print(f"SVG dimensions: {svg_width}x{svg_height}")
print(f"Margins: x={margin_x}, y={margin_y}")
print(f"\nScaling {len(nodes)} nodes...")

# Scale positions from normalized (0-1) to SVG coordinates
for i, node in enumerate(nodes):
    if node.get('x') is not None and node.get('y') is not None:
        # Scale from 0-1 range to SVG coordinates with margins
        node['x'] = margin_x + (node['x'] * (svg_width - 2 * margin_x))
        node['y'] = margin_y + (node['y'] * (svg_height - 2 * margin_y))
    
    # Progress indicator
    if (i + 1) % 100 == 0:
        print(f"  Scaled {i + 1}/{len(nodes)} nodes...")

# Save updated nodes
print("\nSaving updated nodes.json...")
with open('data/nodes.json', 'w', encoding='utf-8') as f:
    json.dump(nodes, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"✓ Scaling complete!")
print(f"  Total nodes: {len(nodes)}")
print(f"  Coordinate range: x=[{margin_x}, {svg_width-margin_x}], y=[{margin_y}, {svg_height-margin_y}]")
print(f"{'='*60}")

# Show some examples
print("\nSample nodes with scaled positions:")
examples = [n for n in nodes if n.get('x') is not None][:3]
for i, node in enumerate(examples, 1):
    print(f"\n[{i}] {node.get('url', 'No URL')[:60]}...")
    print(f"    Position: ({node['x']:.1f}, {node['y']:.1f})")
    print(f"    Keywords: {', '.join(node.get('keywords', [])[:5])}")
