import json

# Load the UMAP data
with open('3d-landscape/data/umap_3d_data.json', 'r', encoding='utf-8') as f:
    sentences = json.load(f)

# Keywords that should be neutral (score 0)
making_keywords = ['make', 'making', 'made', 'maker', 'makers']
material_keywords = ['material', 'materials', 'materiality']

# Track changes
updated_count = 0
making_count = 0
material_count = 0

# Update sentences
for sentence in sentences:
    keywords = sentence.get('keyword', [])
    
    # Check if sentence contains any "making" or "material" keywords
    has_making = any(kw in keywords for kw in making_keywords)
    has_material = any(kw in keywords for kw in material_keywords)
    
    if has_making or has_material:
        old_score = sentence.get('embedded_speculative', 0)
        sentence['embedded_speculative'] = 0.0
        updated_count += 1
        
        if has_making:
            making_count += 1
        if has_material:
            material_count += 1

# Save the updated data
with open('3d-landscape/data/umap_3d_data.json', 'w', encoding='utf-8') as f:
    json.dump(sentences, f, ensure_ascii=False, indent=2)

print(f"Updated {updated_count} sentences")
print(f"  - {making_count} with 'making' keywords")
print(f"  - {material_count} with 'material' keywords")
print("File saved to 3d-landscape/data/umap_3d_data.json")
