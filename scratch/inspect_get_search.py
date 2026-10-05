with open('scratch/get_search_result.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Find tables or content in cmscontent or maincont
clean_text = re.sub(r'<[^>]+>', ' ', html)
lines = [l.strip() for l in clean_text.splitlines() if l.strip()]

# Find all occurrences of Sharma or results
print("Matching lines containing Sharma:")
for i, l in enumerate(lines):
    if 'sharma' in l.lower():
        print(f"L{i}: {l}")

print("\n--- Any tables ---")
tables = re.findall(r'<table\b[^>]*>(.*?)</table>', html, re.DOTALL | re.I)
print(f"Found {len(tables)} tables")
for t in tables:
    ths = re.findall(r'<th\b[^>]*>(.*?)</th>', t, re.DOTALL | re.I)
    print("Table headers:", [re.sub(r'<[^>]+>', '', x).strip() for x in ths])
    trs = re.findall(r'<tr\b[^>]*>(.*?)</tr>', t, re.DOTALL | re.I)
    print(f"Total rows: {len(trs)}")
    for r in trs[:5]:
        tds = re.findall(r'<td\b[^>]*>(.*?)</td>', r, re.DOTALL | re.I)
        print("  Row:", [re.sub(r'<[^>]+>', '', d).strip() for d in tds])
