import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0'}

urls = [
    ('State wise architects', 'https://www.coa.gov.in/index1.php?lang=1&level=1&sublinkid=376&lid=330'),
    ('Yearwise registration', 'https://www.coa.gov.in/index1.php?lang=1&level=1&sublinkid=37&lid=50'),
    ('Cities > 500', 'https://www.coa.gov.in/index1.php?lang=1&level=1&sublinkid=32&lid=45')
]

for name, url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"\n=== {name} ===")
            print(f"Status: {resp.status}, length: {len(content)}")
            tables = re.findall(r'<table\b[^>]*>(.*?)</table>', content, re.DOTALL | re.I)
            print(f"Tables count: {len(tables)}")
            for t in tables[:2]:
                rows = re.findall(r'<tr\b[^>]*>(.*?)</tr>', t, re.DOTALL | re.I)
                print(f"Table rows: {len(rows)}")
                for r in rows[:6]:
                    cols = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', r, re.DOTALL | re.I)]
                    print("  ", cols)
    except Exception as e:
        print(f"Error {name}: {e}")
