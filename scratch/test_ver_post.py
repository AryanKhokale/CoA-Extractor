import urllib.request, http.cookiejar, urllib.parse, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=ctx))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.coa.gov.in/ver_arch.php?lang=1'
}

# 1. GET ver_arch.php
r1 = opener.open(urllib.request.Request('https://www.coa.gov.in/ver_arch.php?lang=1', headers=headers))
print("Loaded ver_arch.php:", r1.status)

# 2. Trigger captcha
opener.open(urllib.request.Request('https://www.coa.gov.in/app/admin/captcha/php_captcha_search.php', headers=headers))
r_ajax = opener.open(urllib.request.Request('https://www.coa.gov.in/app/admin/captcha/ajax_captcha_search.php', headers=headers))
code = r_ajax.read().decode('utf-8').strip()
print(f"Retrieved verification captcha: '{code}'")

# 3. POST form
post_data = {
    'reg_no': 'CA/1975/00005',
    'cap_code2': code,
    'T33': code,
    'Search': 'Search'
}
encoded = urllib.parse.urlencode(post_data).encode('utf-8')
req = urllib.request.Request('https://www.coa.gov.in/ver_arch.php?lang=1', data=encoded, headers={**headers, 'Content-Type': 'application/x-www-form-urlencoded'})

r_res = opener.open(req)
res_html = r_res.read().decode('utf-8', errors='ignore')
print(f"POST response status: {r_res.status}, length: {len(res_html)}")

with open('scratch/ver_res.html', 'w', encoding='utf-8') as f:
    f.write(res_html)

import re
# Look for verification details in the response
tables = re.findall(r'<table\b[^>]*>(.*?)</table>', res_html, re.DOTALL | re.I)
print(f"Found {len(tables)} tables")
for t in tables:
    print(t[:1000])
