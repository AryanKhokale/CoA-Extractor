with open('scratch/search_arch.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Find iframe or forms or ajax calls or tables
iframes = re.findall(r'<iframe\b[^>]*>', html, re.I)
print(f"iframes: {iframes}")

scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL | re.I)
print(f"Script tags count: {len(scripts)}")
for i, s in enumerate(scripts):
    if any(k in s for k in ['search', 'arch', 'load', 'post', 'ajax', 'table']):
        print(f"\n--- Script {i} snippet ---")
        print(s[:500])

# Look for div id="maincontent" or similar container
main = re.search(r'(<div[^>]+id=["\'](?:maincontent|content|container|mid_content)[^>]*>.*?)(?:<div[^>]+id=["\']footer|\Z)', html, re.DOTALL | re.I)
if main:
    print("\n--- Main Content Section (first 1500 chars) ---")
    print(main.group(1)[:1500])
else:
    print("Main content container not matched directly.")
