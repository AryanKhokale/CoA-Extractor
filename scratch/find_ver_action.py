with open('scratch/ver_arch.php_lang_1.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
forms = re.findall(r'<form\b[^>]*action=["\']([^"\']*)["\'][^>]*>(.*?)</form>', html, re.DOTALL | re.I)
for act, body in forms:
    if 'reg_no' in body:
        print(f"Action: {act}")
        print("Body snippet:")
        print(body[:500])
        print("Submit button:")
        sub = re.findall(r'<input[^>]+type=["\']submit["\'][^>]*>', body, re.I)
        print(sub)
