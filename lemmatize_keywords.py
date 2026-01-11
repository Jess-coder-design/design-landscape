import json

# Load keywords_precomputed to extract lemmatization groups
with open('2d-landscape/data/keywords_precomputed.json', 'r', encoding='utf-8') as f:
    keywords_data = json.load(f)

# Build lemmatization map from keywords_precomputed
# Map each variant to its BASE keyword (the key in the dict)
lemmatization_map = {}

for section_name in ['embedded_keywords', 'speculative_keywords', 'critique_keywords']:
    if section_name in keywords_data:
        for base_keyword, variants in keywords_data[section_name].items():
            # Map each variant to the base keyword
            if isinstance(variants, list):
                for variant in variants:
                    lemmatization_map[variant.lower()] = base_keyword

print(f"✓ Loaded {len(lemmatization_map)} lemmatization mappings")

# Load data
with open('3d-landscape/data/umap_3d_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
changes = {}

# Process each sentence
for point in data:
    if 'keyword' in point and isinstance(point['keyword'], list):
        new_keywords = []
        for kw in point['keyword']:
            kw_lower = kw.lower()
            # Check if keyword should be lemmatized
            if kw_lower in lemmatization_map:
                base_kw = lemmatization_map[kw_lower]
                new_keywords.append(base_kw)
                updated_count += 1
                # Track changes
                change_str = f"{kw} → {base_kw}"
                if change_str not in changes:
                    changes[change_str] = 0
                changes[change_str] += 1
            else:
                new_keywords.append(kw)
        point['keyword'] = new_keywords

# Save updated data
with open('3d-landscape/data/umap_3d_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✓ Lemmatization complete!")
print(f"  Updated {updated_count} keyword instances")
print(f"\nTop changes:")
for change, count in sorted(changes.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  {change}: {count} times")
