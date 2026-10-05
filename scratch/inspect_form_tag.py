with open('scratch/search_arch2_cat1.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
forms = re.findall(r'<form\b[^>]*>', html, re.I)
for f in forms:
    print(f)
