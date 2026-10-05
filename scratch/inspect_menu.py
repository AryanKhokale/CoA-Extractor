import urllib.request, ssl, re
from html.parser import HTMLParser

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.coa.gov.in', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, context=ctx, timeout=15)
html = resp.read().decode('utf-8', errors='ignore')

# Search for navbar / menu items
menu_links = re.findall(r'<li[^>]*>.*?<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>.*?</li>', html, re.DOTALL | re.IGNORECASE)
print(f"Found {len(menu_links)} menu items:")
for href, text in menu_links[:50]:
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    if clean_text:
        print(f"  {clean_text} -> {href}")
