import json

# Load and verify
data = json.load(open('3DUMAP/data/umap_3d_data.json', encoding='utf-8'))

sample = data[0]
print('Sample sentence with color:')
print(f"  Keywords: {sample.get('keyword')}")
print(f"  Color (RGB): {sample.get('color')}")

print(f"\nTotal sentences: {len(data)}")
print(f"Sentences with color: {sum(1 for x in data if 'color' in x)}")

# Show some examples
print("\nFirst 3 examples:")
for i in range(3):
    item = data[i]
    keywords = item.get('keyword', [])
    color = item.get('color')
    print(f"  {i+1}. Color: {color}, Most freq keyword: {keywords[0] if keywords else 'N/A'}")
