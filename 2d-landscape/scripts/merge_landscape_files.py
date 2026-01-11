"""
Merge landscape metadata and positions into a single lightweight file
Avoids multiple fetches for the same logical data
"""
import json

# Load metadata
with open('data/landscape_metadata.json', 'r', encoding='utf-8') as f:
    metadata = json.load(f)

# Load positions
with open('data/positions.json', 'r', encoding='utf-8') as f:
    positions = json.load(f)

# Merge into single file
merged = {
    'metadata': metadata,
    'positions': positions
}

with open('data/landscape_data.json', 'w', encoding='utf-8') as f:
    json.dump(merged, f, indent=2)

import os
size = os.path.getsize('data/landscape_data.json') / 1024  # KB

print(f'✅ Merged landscape metadata and positions')
print(f'  File: data/landscape_data.json')
print(f'  Size: {size:.1f} KB')
print(f'  Contains: bounds, SVG dimensions, counts, all positions')
