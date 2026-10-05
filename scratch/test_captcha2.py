import urllib.request, http.cookiejar, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=ctx))
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
    ('Referer', 'https://www.coa.gov.in/search_arch2.php?lang=1&level=1&linkid=&lid=289&searCat=1')
]

# Fetch form
r1 = opener.open('https://www.coa.gov.in/search_arch2.php?lang=1&level=1&linkid=&lid=289&searCat=1')
html = r1.read().decode('utf-8', errors='ignore')

# Find img src for captcha
img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']*captcha[^"\']*)["\']', html, re.I)
print("Captcha img srcs in HTML:", img_srcs)

# Load php_captcha.php
r_img = opener.open('https://www.coa.gov.in/app/admin/captcha/php_captcha.php')
img_bytes = r_img.read()
print(f"Loaded php_captcha.php, bytes: {len(img_bytes)}")

# Now load ajax_captcha.php
r_ajax = opener.open('https://www.coa.gov.in/app/admin/captcha/ajax_captcha.php')
captcha_text = r_ajax.read().decode('utf-8').strip()
print("Captcha value after php_captcha:", repr(captcha_text))
