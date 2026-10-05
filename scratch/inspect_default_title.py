with open('scratch/default_arch.php.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
titles = re.findall(r'<h[1-4]\b[^>]*>(.*?)</h[1-4]>', html, re.DOTALL | re.I)
for t in titles:
    print("Heading:", re.sub(r'<[^>]+>', '', t).strip())

bcs = re.findall(r'class=["\']breadcrumb["\'][^>]*>(.*?)</ol>', html, re.DOTALL | re.I)
for b in bcs:
    print("Breadcrumb:", re.sub(r'<[^>]+>', '', b).strip())
