import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url = 'https://www.coa.gov.in/default_arch.php?page=2&lang=1&level=&linkid=&lid='
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

trs = re.findall(r'<tr\b[^>]*>(.*?)</tr>', html, re.DOTALL | re.I)
print(f"Page 2 rows: {len(trs)}")
for i in range(1, min(6, len(trs))):
    tds = re.findall(r'<td\b[^>]*>(.*?)</td>', trs[i], re.DOTALL | re.I)
    print(f"Row {i}:", [re.sub(r'<[^>]+>', '', x).strip() for x in tds])
