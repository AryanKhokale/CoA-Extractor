import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for endpoint in ['ver_arch.php?lang=1', 'default_arch.php']:
    url = f'https://www.coa.gov.in/{endpoint}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            safe_name = endpoint.replace('?', '_').replace('&', '_').replace('=', '_')
            with open(f'scratch/{safe_name}.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Endpoint: {endpoint} -> Status: {resp.status}, Length: {len(content)}")
    except Exception as e:
        print(f"Endpoint: {endpoint} -> Error: {e}")
