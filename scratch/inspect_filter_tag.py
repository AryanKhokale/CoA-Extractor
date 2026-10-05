with open('scratch/default_arch.php.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
forms = re.findall(r'<form\b[^>]*>', html, re.I)
for f in forms:
    if 'search_by' in html[html.find(f):html.find(f)+500]:
        print("Filter form tag:", f)
