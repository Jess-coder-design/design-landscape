import json
from collections import Counter

# Load keywords_precomputed.json to map variants to main keywords
with open('3DUMAP/data/keywords_precomputed.json', 'r', encoding='utf-8') as f:
    kp = json.load(f)

# Load colorsnew.json for the color mapping
with open('3DUMAP/data/colorsnew.json', 'r', encoding='utf-8') as f:
    color_map = json.load(f)

# Build reverse mapping: variant -> main keyword
variant_to_main = {}

# From embedded_keywords
for main_kw, variants in kp.get('embedded_keywords', {}).items():
    if isinstance(variants, list):
        for variant in variants:
            variant_to_main[variant.lower()] = main_kw

# From speculative_keywords
for main_kw, variants in kp.get('speculative_keywords', {}).items():
    if isinstance(variants, list):
        for variant in variants:
            variant_to_main[variant.lower()] = main_kw

# From critique_keywords
for main_kw, variants in kp.get('critique_keywords', {}).items():
    if isinstance(variants, list):
        for variant in variants:
            variant_to_main[variant.lower()] = main_kw

# Also add contextual_scores keys as main keywords
contextual = kp.get('contextual_scores', {})
for section in contextual.values():
    for main_kw in section.keys():
        variant_to_main[main_kw.lower()] = main_kw

print(f"Built mapping for {len(variant_to_main)} variants to main keywords")

# Function to get most frequent keyword
def get_most_frequent_keyword(keyword_array):
    if not keyword_array:
        return None
    counts = Counter(keyword_array)
    most_common = counts.most_common(1)
    if most_common:
        return most_common[0][0]
    return keyword_array[0]

# Load umap_3d_data.json
with open('3DUMAP/data/umap_3d_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} sentences from umap_3d_data.json")

# Add color to each sentence
color_count = {
    'found': 0,
    'not_found': 0,
    'colors_used': set()
}

for i, item in enumerate(data):
    if i % 500 == 0:
        print(f"Processing {i}/{len(data)}...")
    
    # Get keywords for this sentence
    keywords = item.get('keyword', [])
    if not keywords:
        continue
    
    # Get the most frequent keyword
    most_freq = get_most_frequent_keyword(keywords)
    if not most_freq:
        continue
    
    # Map to main keyword
    main_keyword = variant_to_main.get(most_freq.lower())
    if not main_keyword:
        color_count['not_found'] += 1
        continue
    
    # Get color for main keyword
    if main_keyword in color_map:
        item['color'] = color_map[main_keyword]
        color_count['found'] += 1
        color_count['colors_used'].add(main_keyword)
    else:
        color_count['not_found'] += 1

# Save updated data
with open('3DUMAP/data/umap_3d_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✓ Updated umap_3d_data.json with colors")
print(f"  - Color added: {color_count['found']}")
print(f"  - Not found: {color_count['not_found']}")
print(f"  - Unique colors used: {len(color_count['colors_used'])}")
print(f"\nColors used:")
for color in sorted(color_count['colors_used']):
    print(f"  {color}")
