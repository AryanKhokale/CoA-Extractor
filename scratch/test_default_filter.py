import urllib.request, urllib.parse, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Test POST or GET filter
post_data = urllib.parse.urlencode({
    'search_by_fname': '',
    'search_by_lname': '',
    'search_by_city': 'Mumbai',
    'search_by_reg_no': '',
    'submit': 'Submit'
}).encode('utf-8')

url = 'https://www.coa.gov.in/default_arch.php'
req = urllib.request.Request(url, data=post_data, headers={**headers, 'Content-Type': 'application/x-www-form-urlencoded'})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

trs = re.findall(r'<tr\b[^>]*>(.*?)</tr>', html, re.DOTALL | re.I)
print(f"Filtered rows count: {len(trs)}")
for i in range(1, min(6, len(trs))):
    tds = re.findall(r'<td\b[^>]*>(.*?)</td>', trs[i], re.DOTALL | re.I)
    print(f"Row {i}:", [re.sub(r'<[^>]+>', '', x).strip() for x in tds])
