import re

print("=== DEFAULT_ARCH.PHP ANALYSIS ===")
with open('scratch/default_arch.php.html', 'r', encoding='utf-8') as f:
    d_html = f.read()

tables = re.findall(r'<table\b[^>]*>(.*?)</table>', d_html, re.DOTALL | re.I)
print(f"Found {len(tables)} tables in default_arch.php")
for i, t in enumerate(tables):
    ths = re.findall(r'<th\b[^>]*>(.*?)</th>', t, re.DOTALL | re.I)
    print(f"Table {i+1} headers: {[re.sub(r'<[^>]+>', '', x).strip() for x in ths]}")
    trs = re.findall(r'<tr\b[^>]*>(.*?)</tr>', t, re.DOTALL | re.I)
    print(f"Table {i+1} rows count: {len(trs)}")
    if len(trs) > 1:
        tds = re.findall(r'<td\b[^>]*>(.*?)</td>', trs[1], re.DOTALL | re.I)
        print("Sample row 1:", [re.sub(r'<[^>]+>', '', x).strip() for x in tds])
    if len(trs) > 2:
        tds = re.findall(r'<td\b[^>]*>(.*?)</td>', trs[2], re.DOTALL | re.I)
        print("Sample row 2:", [re.sub(r'<[^>]+>', '', x).strip() for x in tds])

# Pagination links
pagination = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(?:Next|Previous|Last|First|\d+)</a>', d_html, re.I)
print("Pagination in default_arch.php:", pagination[:10])

print("\n=== VER_ARCH.PHP ANALYSIS ===")
with open('scratch/ver_arch.php_lang_1.html', 'r', encoding='utf-8') as f:
    v_html = f.read()

forms = re.findall(r'<form\b[^>]*>(.*?)</form>', v_html, re.DOTALL | re.I)
print(f"Found {len(forms)} forms in ver_arch.php")
for f in forms:
    action = re.search(r'action=["\']([^"\']*)["\']', f, re.I)
    method = re.search(r'method=["\']([^"\']*)["\']', f, re.I)
    inputs = re.findall(r'<input\b[^>]*>', f, re.I)
    if len(inputs) > 2:
        print(f"Form action: {action.group(1) if action else 'None'}, method: {method.group(1) if method else 'GET'}")
        for inp in inputs:
            print(" ", inp)
