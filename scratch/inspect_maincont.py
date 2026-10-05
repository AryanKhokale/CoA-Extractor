with open('scratch/search_arch.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
idx = html.find('id="maincont"')
if idx != -1:
    print(html[idx:idx+4000])
else:
    print("Not found")
