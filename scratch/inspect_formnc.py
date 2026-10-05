with open('scratch/search_arch2_cat1.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
pos = html.find('name="formNC"')
print("Surrounding 3000 chars of formNC:")
print(html[pos-200:pos+3000])
