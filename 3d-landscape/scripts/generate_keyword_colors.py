import json
from collections import Counter
import itertools

# Load the data
with open('3DUMAP/data/umap_3d_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all keywords
all_keywords = list(itertools.chain.from_iterable(
    x.get('keyword', []) if isinstance(x.get('keyword'), list) else [] 
    for x in data
))

# Get unique keywords and count
keyword_counts = Counter(all_keywords)
unique_keywords = sorted(keyword_counts.keys())

# Generate colors and output
print("KEYWORD AND COLOR MAPPING")
print("=" * 80)
print(f"{'Keyword':<45} {'Count':<8} {'Color (HSL)':<25}")
print("-" * 80)

keyword_color_map = {}

for keyword in unique_keywords:
    # Create hash similar to JavaScript
    hash_val = 0
    for char in keyword:
        hash_val = ((hash_val << 5) - hash_val) + ord(char)
        hash_val = hash_val & 0xFFFFFFFF
    
    # Generate HSL color (hue based on hash)
    hue = (hash_val % 360)
    saturation = 70 + (hash_val % 30)
    lightness = 50 + (hash_val % 20)
    
    hsl_str = f"hsl({hue}, {saturation}%, {lightness}%)"
    count = keyword_counts[keyword]
    
    keyword_color_map[keyword] = {
        'hsl': hsl_str,
        'hue': hue,
        'saturation': saturation,
        'lightness': lightness,
        'count': count
    }
    
    print(f"{keyword:<45} {count:<8} {hsl_str:<25}")

print("-" * 80)
print(f"Total unique keywords: {len(unique_keywords)}")
print(f"Total keyword occurrences: {len(all_keywords)}")

# Save to JSON
with open('3DUMAP/data/keyword_color_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(keyword_color_map, f, indent=2, ensure_ascii=False)

print("\nSaved to 3DUMAP/data/keyword_color_mapping.json")
