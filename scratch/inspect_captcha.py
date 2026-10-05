with open('scratch/search_arch2_cat1.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Find the form tag and surrounding html
form = re.search(r'(<form[^>]+name="frm".*?</form>)', html, re.DOTALL | re.I)
if form:
    print("Form HTML:")
    print(form.group(1))
else:
    # search for T3
    idx = html.find('name="T3"')
    print("Around T3:")
    print(html[idx-300:idx+400])

# Look for captcha scripts
scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL | re.I)
for s in scripts:
    if 'T3' in s or 'cap' in s or 'captcha' in s.lower():
        print("\n--- Captcha Script snippet ---")
        print(s[:500])
