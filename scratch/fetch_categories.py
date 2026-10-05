import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

for cat in [1, 2, 3, 4, 5, 6]:
    url = f'https://www.coa.gov.in/search_arch2.php?lang=1&level=1&linkid=&lid=289&searCat={cat}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            filename = f'scratch/search_arch2_cat{cat}.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cat {cat}: HTTP {resp.status}, length {len(content)}, saved to {filename}")
    except Exception as e:
        print(f"Cat {cat} error: {e}")
