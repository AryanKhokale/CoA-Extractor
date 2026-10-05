with open('scratch/ver_arch.php_lang_1.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
idx = html.find('name="ca_reg_no"')
if idx != -1:
    print(html[idx-500:idx+1500])
else:
    print("ca_reg_no not found")
