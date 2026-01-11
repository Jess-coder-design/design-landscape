import json

# Load keywords_precomputed.json
with open('3DUMAP/data/keywords_precomputed.json', 'r', encoding='utf-8') as f:
    kp = json.load(f)

# Function to convert HSL to RGB
def hsl_to_rgb(h, s, l):
    """Convert HSL to RGB"""
    s = s / 100
    l = l / 100
    
    if s == 0:
        r = g = b = int(l * 255)
        return (r, g, b)
    
    def hue_to_rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1/6:
            return p + (q - p) * 6 * t
        if t < 1/2:
            return q
        if t < 2/3:
            return p + (q - p) * (2/3 - t) * 6
        return p
    
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    
    r = int(hue_to_rgb(p, q, h/360 + 1/3) * 255)
    g = int(hue_to_rgb(p, q, h/360) * 255)
    b = int(hue_to_rgb(p, q, h/360 - 1/3) * 255)
    
    return (r, g, b)

# Function to generate color hash
def generate_color(keyword):
    """Generate HSL color from keyword hash"""
    hash_val = 0
    for char in keyword:
        hash_val = ((hash_val << 5) - hash_val) + ord(char)
        hash_val = hash_val & 0xFFFFFFFF
    
    hue = (hash_val % 360)
    saturation = 70 + (hash_val % 30)
    lightness = 50 + (hash_val % 20)
    
    return hsl_to_rgb(hue, saturation, lightness)

# Collect all keywords from keywords_precomputed.json
all_keywords = set()

# From contextual_scores
contextual = kp.get('contextual_scores', {})
for section in contextual.values():
    all_keywords.update(section.keys())

# From embedded_keywords
for kw_list in kp.get('embedded_keywords', {}).values():
    if isinstance(kw_list, list):
        all_keywords.update(kw_list)

# From speculative_keywords
for kw_list in kp.get('speculative_keywords', {}).values():
    if isinstance(kw_list, list):
        all_keywords.update(kw_list)

# From critique_keywords
for kw_list in kp.get('critique_keywords', {}).values():
    if isinstance(kw_list, list):
        all_keywords.update(kw_list)

# Create RGB-only mapping for all keywords
rgb_only = {}
for keyword in sorted(all_keywords):
    r, g, b = generate_color(keyword)
    rgb_only[keyword] = [r, g, b]

# Save to colorsnew.json
with open('3DUMAP/data/colorsnew.json', 'w', encoding='utf-8') as f:
    json.dump(rgb_only, f, indent=2, ensure_ascii=False)

print(f"✓ Saved RGB colors for all {len(rgb_only)} keywords to 3DUMAP/data/colorsnew.json")
