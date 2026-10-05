import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://www.coa.gov.in/index1.php?lang=1&level=1&sublinkid=1161&lid=297'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print("Additional Fine Waived List status:", resp.status, "length:", len(content))
        tables = re.findall(r'<table\b[^>]*>(.*?)</table>', content, re.DOTALL | re.I)
        print("Tables:", len(tables))
        if tables:
            trs = re.findall(r'<tr\b[^>]*>(.*?)</tr>', tables[0], re.DOTALL | re.I)
            print("Rows:", len(trs))
            for r in trs[:5]:
                print("  ", [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', r, re.DOTALL | re.I)])
except Exception as e:
    print("Error:", e)
