"""
Sierra Puebla Nahuatl Filter
Extracts entries specifically from Western Sierra Puebla dialect variants
ISO 639-3 code: nhi (Zacatlán-Ahuacatlán-Tepetzintla)
"""

import elotl.corpus
from collections import defaultdict
from typing import DefaultDict
import json

print("=" * 70)
print("Sierra Puebla Nahuatl Extraction Tool")
print("=" * 70)

# Load full Axolotl corpus
axolotl = elotl.corpus.load('axolotl')

if axolotl == 0:
    print("❌ Error: Corpus not found")
    exit(1)

print(f"✅ Loaded {len(axolotl)} total parallel sentences\n")

# Step 1: Filter for Sierra Puebla variants
print("Filtering for Sierra Puebla Nahuatl variants...")
print("Target regions: Zacatlán, Ahuacatlán, Tepetzintla")
print("Target ISO code: nhi (Western Sierra Puebla)")
print("-" * 70)

sierra_puebla_entries = []

dialect_counts: DefaultDict[str, int] = defaultdict(int)

# Keywords that indicate Sierra Puebla origin
sierra_keywords = [
    'Sierra Puebla',
    'Sierra Norte',
    'Zacatlán',
    'Ahuacatlán',
    'Tepetzintla',
    'San Miguel Tenango',
    'Ixquihuacan',
    'Omitlán'
]

for entry in axolotl:
    spanish_text = entry[0]
    nahuatl_text = entry[1]
    dialect = entry[2]
    document = entry[3]
    iso_code = entry[4] if len(entry) > 4 else ""

    # Skip empty entries
    if not spanish_text.strip() or not nahuatl_text.strip():
        continue

    # Filter by ISO code (nhi = Western Sierra Puebla)
    is_sierra_puebla = False

    # Method 1: Check ISO code
    if iso_code == 'nhi':
        is_sierra_puebla = True

    # Method 2: Check dialect field for Sierra keywords
    for keyword in sierra_keywords:
        if keyword.lower() in dialect.lower():
            is_sierra_puebla = True
            break

    # Method 3: Check document source for Sierra keywords
    for keyword in sierra_keywords:
        if keyword.lower() in document.lower():
            is_sierra_puebla = True
            break

    if is_sierra_puebla:
        sierra_puebla_entries.append(entry)
        dialect_counts[dialect] += 1

# Step 2: Display results
print(f"\n🎯 Found {len(sierra_puebla_entries)} Sierra Puebla Nahuatl entries")
print(f"📊 Percentage of corpus: {len(sierra_puebla_entries)/len(axolotl)*100:.1f}%\n")

print("=" * 70)
print("Dialect Distribution in Sierra Puebla Entries:")
print("=" * 70)
for dialect, count in sorted(dialect_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {dialect:50s} ({count} sentences)")

# Step 3: Display sample entries
print("\n" + "=" * 70)
print("Sample Sierra Puebla Nahuatl Entries (First 15)")
print("=" * 70)

for i, entry in enumerate(sierra_puebla_entries[:15], 1):
    spanish_text = entry[0]
    nahuatl_text = entry[1]
    dialect = entry[2]
    document = entry[3]
    iso_code = entry[4] if len(entry) > 4 else "N/A"

    print(f"\n{i:2d}. 📍 Document: {document}")
    spanish_snip = spanish_text[:80] + ("..." if len(spanish_text) > 80 else "")
    nahuatl_snip = nahuatl_text[:80] + ("..." if len(nahuatl_text) > 80 else "")
    print(f"    🇪🇸 Spanish:  {spanish_snip}")
    print(f"    🇲🇽 Nahuatl:  {nahuatl_snip}")
    print(f"    🏷️  Dialect:  {dialect}")
    print(f"    🔖 ISO Code: {iso_code}")

# Step 4: Linguistic features analysis
print("\n" + "=" * 70)
print("Sierra Puebla Nahuatl Linguistic Features")
print("=" * 70)

# Check for characteristic features
features = {
    'absolutive -i/-e': 0,  # Modern Sierra evolution from -li
    'vowel length': 0,      # Presence of long vowels (doubled vowels)
    '/tl/ cluster': 0,      # Common in Nahuatl
    '/kw/ sound': 0         # Written as 'cu' or 'qu'
}

for entry in sierra_puebla_entries[:100]:  # Sample first 100
    nahuatl_text = entry[1].lower()

    # Check for absolutive -i or -e endings (not -li)
    words = nahuatl_text.split()
    for word in words:
        if word.endswith('i') or word.endswith('e'):
            if not word.endswith('li'):
                features['absolutive -i/-e'] += 1
                break

    # Check for vowel length markers (doubled vowels)
    if any(vowel*2 in nahuatl_text for vowel in 'aeiou'):
        features['vowel length'] += 1

    # Check for /tl/ cluster
    if 'tl' in nahuatl_text:
        features['/tl/ cluster'] += 1

    # Check for /kw/ sound
    if 'cu' in nahuatl_text or 'qu' in nahuatl_text:
        features['/kw/ sound'] += 1

print("\nPhonological/Morphological Features (in 100 samples):")
for feature, count in features.items():
    print(f"  {feature:20s}: {count}/100 sentences ({count}%)")

# Step 5: Export to JSON

output_data = {
    'corpus_stats': {
        'total_corpus_size': len(axolotl),
        'sierra_puebla_count': len(sierra_puebla_entries),
        'percentage': f"{len(sierra_puebla_entries)/len(axolotl)*100:.2f}%",
        'target_iso_code': 'nhi',
        'target_regions': sierra_keywords
    },
    'dialect_distribution': dict(dialect_counts),
    'sample_entries': [
        # Export 30 samples
        {
            'spanish': entry[0],
            'nahuatl': entry[1],
            'dialect': entry[2],
            'document': entry[3],
            'iso_code': entry[4] if len(entry) > 4 else 'N/A'
        }
        for entry in sierra_puebla_entries[:30]
    ]
}

with open('sierra_puebla_nahuatl.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

exported_count = len(sierra_puebla_entries[:30])
msg = f"\n✅ Exported {exported_count} entries"
msg += " to sierra_puebla_nahuatl.json"
print(msg)

# Step 6: Recommendations
print("\n" + "=" * 70)
print("💡 Recommendations for RAG System Development")
print("=" * 70)

if len(sierra_puebla_entries) >= 50:
    print("✅ Sufficient data for demo RAG system (50+ entries)")
    print("   → Use these entries as your core dataset")
    print("   → Highlight regional specificity in documentation")
else:
    print("⚠️  Limited Sierra Puebla data in corpus")
    print(f"   → Found: {len(sierra_puebla_entries)} entries")
    print("   → Consider supplementing with:")
    print("     • Universal Dependencies Sierra Puebla treebank")
    print("     • Community-sourced texts from target regions")

print("\n🔍 Next Steps:")
print("1. Review sierra_puebla_nahuatl.json for data quality")
print("2. Verify dialect tags with native speakers if possible")
print("3. Use ISO code 'nhi' to filter during embedding phase")
print("4. Document regional specificity in DESIGN.md")
