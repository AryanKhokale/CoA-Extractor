with open('scratch/search_result.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Look for table or records
tables = re.findall(r'<table\b[^>]*>(.*?)</table>', html, re.DOTALL | re.I)
print(f"Found {len(tables)} tables")

for idx, tbl in enumerate(tables):
    # Check headers
    ths = re.findall(r'<th\b[^>]*>(.*?)</th>', tbl, re.DOTALL | re.I)
    clean_ths = [re.sub(r'<[^>]+>', '', t).strip() for t in ths if re.sub(r'<[^>]+>', '', t).strip()]
    trs = re.findall(r'<tr\b[^>]*>(.*?)</tr>', tbl, re.DOTALL | re.I)
    print(f"Table {idx+1}: {len(trs)} rows, headers: {clean_ths}")
    if trs:
        print(" Sample Row 1:", trs[0][:300])
        if len(trs) > 1:
            print(" Sample Row 2:", trs[1][:300])

# Search for any messages or alerts
alerts = re.findall(r'class=["\'](?:alert|error|message|msg)[^"\']*["\'][^>]*>(.*?)<', html, re.I)
print(f"Alerts: {alerts}")

# Look for search architect result snippets
clean_text = re.sub(r'<[^>]+>', ' ', html)
lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
print("\nFirst 40 lines of text:")
for l in lines[40:80]:
    print(l)
