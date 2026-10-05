import urllib.request, ssl, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.coa.gov.in', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, context=ctx, timeout=15)
html = resp.read().decode('utf-8', errors='ignore')

# Search for "Verify"
matches = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?verify.*?)</a>', html, re.I | re.DOTALL)
print("Verify links count:", len(matches))
for h, t in matches[:10]:
    clean_t = re.sub(r'<[^>]+>', '', t).strip()
    print(f"  {clean_t} -> {h}")

phps = set(re.findall(r'[\w\-]+\.php(?:\?[^\s"\'<>]*)?', html, re.I))
print(f"Total PHP endpoints found: {len(phps)}")
for p in sorted(phps):
    if any(k in p.lower() for k in ['arch', 'verif', 'search', 'direct', 'reg', 'member', 'list']):
        print("  *", p)
