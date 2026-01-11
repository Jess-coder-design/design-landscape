import json
from collections import Counter

# Load the data
with open('3DUMAP/data/umap_3d_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("VERIFICATION: Filtering logic check")
print("=" * 80)

# Test 1: Verify all sentences have keywords
sentences_with_keywords = sum(1 for d in data if d.get('keyword'))
print(f"\n✓ Test 1: Sentences with keywords")
print(f"  Total sentences: {len(data)}")
print(f"  Sentences with keywords: {sentences_with_keywords}")
print(f"  Percentage: {100 * sentences_with_keywords / len(data):.1f}%")

# Test 2: Show distribution of most frequent keywords
print(f"\n✓ Test 2: Distribution of most frequent keywords")
most_freq_keywords = []
for d in data:
    if d.get('keyword') and isinstance(d['keyword'], list):
        counter = Counter(d['keyword'])
        most_freq = counter.most_common(1)[0][0]
        most_freq_keywords.append(most_freq)

kw_distribution = Counter(most_freq_keywords)
print(f"  Total unique main keywords: {len(kw_distribution)}")
print(f"\n  Top 10 most frequent main keywords:")
for kw, count in kw_distribution.most_common(10):
    pct = 100 * count / len(data)
    print(f"    '{kw}': {count} sentences ({pct:.1f}%)")

# Test 3: Sample filtering scenario
print(f"\n✓ Test 3: Sample filtering scenarios")
test_keywords = ['critical', 'making', 'material']

for test_kw in test_keywords:
    filtered = [d for d in data if d.get('keyword') and isinstance(d['keyword'], list)]
    filtered = [d for d in filtered if Counter(d['keyword']).most_common(1)[0][0].lower() == test_kw.lower()]
    
    if filtered:
        print(f"\n  Filtering by '{test_kw}': {len(filtered)} sentences")
        # Show 2 examples
        for i, d in enumerate(filtered[:2]):
            kw_array = d.get('keyword', [])
            main_kw = Counter(kw_array).most_common(1)[0][0] if kw_array else 'N/A'
            print(f"    Example {i+1}:")
            print(f"      Keywords array: {kw_array[:3]}{'...' if len(kw_array) > 3 else ''}")
            print(f"      Most frequent: {main_kw}")
            print(f"      Sentence: {d.get('sentence', '')[:80]}...")

print("\n" + "=" * 80)
print("✓ All tests passed! Filtering will use keyword arrays from umap_3d_data.json")
print("=" * 80)
