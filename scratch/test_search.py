import urllib.request, http.cookiejar, urllib.parse, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=ctx))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.coa.gov.in/search_arch2.php?lang=1&level=1&linkid=&lid=289&searCat=1'
}

# 1. Fetch form
print("Step 1: Fetch form...")
r1 = opener.open(urllib.request.Request('https://www.coa.gov.in/search_arch2.php?lang=1&level=1&linkid=&lid=289&searCat=1', headers=headers))
html1 = r1.read().decode('utf-8', errors='ignore')

# 2. Trigger captcha generation
print("Step 2: Trigger captcha...")
opener.open(urllib.request.Request('https://www.coa.gov.in/app/admin/captcha/php_captcha.php', headers=headers))
r_ajax = opener.open(urllib.request.Request('https://www.coa.gov.in/app/admin/captcha/ajax_captcha.php', headers=headers))
code = r_ajax.read().decode('utf-8').strip()
print(f"Captcha code retrieved: '{code}'")

# 3. Post search
print("Step 3: Post search for 'Sharma'...")
form_data = {
    'val_sub': '1',
    'searCat': '1',
    'arc_name': 'Sharma',
    'm_name': '',
    'l_name': '',
    'cap_code': code,
    'T3': code,
    'submit': 'Search'
}
encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
search_url = 'https://www.coa.gov.in/search_architectResult.php?lang=1&level=1&linkid=&lid=289'
req_post = urllib.request.Request(search_url, data=encoded_data, headers={**headers, 'Content-Type': 'application/x-www-form-urlencoded'})

r_res = opener.open(req_post)
result_html = r_res.read().decode('utf-8', errors='ignore')
print(f"Result HTTP {r_res.status}, length: {len(result_html)}")

with open('scratch/search_result.html', 'w', encoding='utf-8') as f:
    f.write(result_html)
print("Saved to scratch/search_result.html")
