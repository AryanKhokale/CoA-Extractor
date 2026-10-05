with open('scratch/member_list.php.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
tables = re.findall(r'<table\b[^>]*>(.*?)</table>', html, re.DOTALL | re.I)
print(f"Tables in member_list: {len(tables)}")
for i, t in enumerate(tables):
    trs = re.findall(r'<tr\b[^>]*>(.*?)</tr>', t, re.DOTALL | re.I)
    print(f"Table {i+1} rows: {len(trs)}")
    if trs:
        for r in trs[:5]:
            tds = [re.sub(r'<[^>]+>', '', d).strip() for d in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', r, re.DOTALL | re.I)]
            print("  ", tds)
