"""
Pre-compute final x,y positions for nodes to avoid client-side calculations
Calculates: x = xScale(umapX) + horizontalOffset
            y = yScale(umapY) + verticalOffset
"""
import json
import random
from pathlib import Path

# Load nodes with UMAP coordinates
with open('data/nodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

# Find UMAP bounds
umap_x_values = [n.get('umap_x', 0.5) for n in nodes]
umap_y_values = [n.get('umap_y', 0.5) for n in nodes]

minX = min(umap_x_values)
maxX = max(umap_x_values)
minY = min(umap_y_values)
maxY = max(umap_y_values)

xMid = (minX + maxX) / 2
yMid = (minY + maxY) / 2

# SVG canvas dimensions (from landscape HTML)
BASE_WIDTH = 1920
BASE_HEIGHT = 1080
WIDTH_SCALE = 1.67
HEIGHT_SCALE = 4.5
SVG_WIDTH = BASE_WIDTH * WIDTH_SCALE
SVG_HEIGHT = BASE_HEIGHT * HEIGHT_SCALE
MARGIN_X = int(80 * WIDTH_SCALE)
MARGIN_Y = int(60 * HEIGHT_SCALE)

# Create scale functions (same logic as D3.js scaleLinear)
def xScale(val):
    """Map UMAP x to SVG coordinates"""
    return MARGIN_X + ((val - minX) / (maxX - minX)) * (SVG_WIDTH - 2 * MARGIN_X) if maxX != minX else SVG_WIDTH / 2

def yScale(val):
    """Map UMAP y to SVG coordinates"""
    return MARGIN_Y + ((val - minY) / (maxY - minY)) * (SVG_HEIGHT - 2 * MARGIN_Y) if maxY != minY else SVG_HEIGHT / 2

# Pre-compute positions for each node
for node in nodes:
    umapX = node.get('umap_x', 0.5)
    umapY = node.get('umap_y', 0.5)
    
    # Generate random offsets (same as landscape)
    verticalOffset = (random.random() - 0.5) * 2500
    horizontalOffset = (random.random() - 0.5) * 2500
    
    # Calculate final positions
    node['x'] = xScale(umapX) + horizontalOffset
    node['y'] = yScale(umapY) + verticalOffset

# Save updated nodes
with open('data/nodes.json', 'w', encoding='utf-8') as f:
    json.dump(nodes, f, indent=2)

print(f'✅ Pre-computed x,y positions for {len(nodes)} nodes')
print(f'  UMAP bounds: X [{minX:.3f}, {maxX:.3f}], Y [{minY:.3f}, {maxY:.3f}]')
print(f'  SVG mapping: {int(SVG_WIDTH)}x{int(SVG_HEIGHT)} with X margin {MARGIN_X}, Y margin {MARGIN_Y}')
