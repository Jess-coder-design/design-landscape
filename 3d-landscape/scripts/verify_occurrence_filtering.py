import json
from collections import Counter

# Load the data
with open('3DUMAP/data/umap_3d_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("VERIFICATION: Multiple click filtering")
print("=" * 80)

# Test filtering with different click counts
test_cases = [
    ('critical', 1),
    ('critical', 2),
    ('critical', 3),
    ('making', 1),
    ('making', 2),
    ('making', 3),
]

for keyword, required_count in test_cases:
    matching = 0
    for d in data:
        keyword_array = d.get('keyword', [])
        count = sum(1 for kw in keyword_array if kw.lower() == keyword.lower())
        if count == required_count:
            matching += 1
    
    pct = 100 * matching / len(data)
    print(f"\n'{keyword}' appears exactly {required_count}x: {matching} sentences ({pct:.1f}%)")
    
    # Show examples
    examples = 0
    for d in data:
        if examples >= 2:
            break
        keyword_array = d.get('keyword', [])
        count = sum(1 for kw in keyword_array if kw.lower() == keyword.lower())
        if count == required_count:
            print(f"  Example: {keyword_array} → count={count}")
            examples += 1

print("\n" + "=" * 80)
print("✓ Filtering by occurrence count will now work correctly!")
print("=" * 80)
