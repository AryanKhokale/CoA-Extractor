import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://www.coa.gov.in/search_arch.php?lang=1&level=1&sublinkid=925&lid=289'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Status: {resp.status}, Length: {len(html)}")
        with open('scratch/search_arch.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Saved to scratch/search_arch.html")
except Exception as e:
    print("Error:", e)
