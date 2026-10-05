import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://www.coa.gov.in/sitemap.php?lang=1&level=0&linkid=30&lid=31'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL | re.I)
print(f"Total sitemap links: {len(links)}")
with open('scratch/sitemap_links.txt', 'w', encoding='utf-8') as f:
    for href, text in links:
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        f.write(f"{clean_text} -> {href}\n")
        if any(k in clean_text.lower() or k in href.lower() for k in ['architect', 'register', 'directory', 'list', 'member']):
            print(f"  {clean_text} -> {href}")
