import urllib.request, http.cookiejar, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=ctx))
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'),
    ('Referer', 'https://www.coa.gov.in/search_arch2.php?lang=1&level=1&linkid=&lid=289&searCat=1')
]

# 1. Fetch form
r1 = opener.open('https://www.coa.gov.in/search_arch2.php?lang=1&level=1&linkid=&lid=289&searCat=1')
print("Loaded form, status:", r1.status)
for c in cj:
    print(f"Cookie: {c.name}={c.value}")

# 2. Fetch captcha
r2 = opener.open('https://www.coa.gov.in/app/admin/captcha/ajax_captcha.php')
captcha_text = r2.read().decode('utf-8').strip()
print("Captcha value returned by ajax_captcha.php:", repr(captcha_text))
