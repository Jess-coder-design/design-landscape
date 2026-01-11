import json

with open('3DUMAP/data/umap_3d_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Sample entries showing scores and Z axis mapping:\n")
samples = [0, 100, 500, 1000, 2000]

for idx in samples:
    if idx < len(data):
        item = data[idx]
        print(f"Entry {idx}:")
        print(f"  Keywords: {item['keyword']}")
        print(f"  embedded_speculative score: {item['embedded_speculative']:.3f}")
        print(f"  Z coordinate: {item['z']:.3f}")
        print()

print("\nSummary statistics:")
scores = [item['embedded_speculative'] for item in data]
z_coords = [item['z'] for item in data]

print(f"embedded_speculative scores: min={min(scores):.3f}, max={max(scores):.3f}, mean={sum(scores)/len(scores):.3f}")
print(f"Z coordinates: min={min(z_coords):.3f}, max={max(z_coords):.3f}")
print(f"\nNote: Z axis now represents embeddedness (-5.0) to speculation (+4.25)")
