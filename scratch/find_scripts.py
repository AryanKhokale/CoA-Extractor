with open('scratch/search_arch2_cat1.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I)
for s in scripts:
    print(s)
