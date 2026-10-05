import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for url in [
    'https://www.coa.gov.in/search_architectResult.php',
    'https://www.coa.gov.in/search_architectResult.php?searCat=1&arc_name=Sharma',
    'https://www.coa.gov.in/searchresult.php?key=Sharma',
    'https://www.coa.gov.in/member_list.php?lang=1&level=1&sublinkid=919&lid=253',
    'https://www.coa.gov.in/architectural_institutions.php?lang=1&level=1&sublinkid=924&lid=793'
]:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"URL: {url} -> Status: {resp.status}, Length: {len(content)}, Title: {[l for l in content.splitlines() if '<title>' in l]}")
            if "searchresult.php" in url or "member_list.php" in url:
                with open(f"scratch/{url.split('/')[-1].split('?')[0]}.html", "w", encoding="utf-8") as f:
                    f.write(content)
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
