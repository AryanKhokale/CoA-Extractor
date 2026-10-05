with open('scratch/default_arch.php.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL | re.I)
for s in scripts:
    if 'frm1' in s or 'search_by' in s or 'submitButton' in s:
        print("Found script:")
        print(s)
