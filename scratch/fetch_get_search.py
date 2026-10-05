import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://www.coa.gov.in/search_architectResult.php?searCat=1&arc_name=Sharma'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

with open('scratch/get_search_result.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved scratch/get_search_result.html, length:", len(html))
