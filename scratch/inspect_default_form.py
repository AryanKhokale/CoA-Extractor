with open('scratch/default_arch.php.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
forms = re.findall(r'<form\b[^>]*>(.*?)</form>', html, re.DOTALL | re.I)
print(f"Forms in default_arch: {len(forms)}")
for i, f in enumerate(forms):
    inputs = re.findall(r'<input\b[^>]*>', f, re.I)
    selects = re.findall(r'<select\b[^>]*name=["\']([^"\']+)["\'][^>]*>', f, re.I)
    if len(inputs) > 2 or selects:
        print(f"Form {i+1} inputs: {inputs}")
        print(f"Form {i+1} selects: {selects}")

# Check any other links in cmscontent
idx = html.find('id="cmscontent"')
if idx != -1:
    print("\nInside cmscontent (first 1000 chars):")
    print(html[idx:idx+1000])
