import json

nodes = json.load(open('data/nodes.json', encoding='utf-8'))
with_kw = [n for n in nodes if n.get('keywords')]

print(f"✓ {len(with_kw)} nodes with keywords extracted\n")
print("="*80)

for i, node in enumerate(with_kw[:5]):
    print(f"\n[{i+1}] {node['url']}")
    print(f"Keywords found: {', '.join(node['keywords'])}")
    if node.get('sample_sentence'):
        sentence = node['sample_sentence']
        if len(sentence) > 200:
            sentence = sentence[:200] + "..."
        print(f"Sample: {sentence}")
    print("-"*80)
