import urllib.request, http.cookiejar, urllib.parse, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def test_cat(searCat, field_data):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=ctx))
    
    cat_url = f'https://www.coa.gov.in/search_arch2.php?lang=1&level=1&linkid=&lid=289&searCat={searCat}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': cat_url
    }
    
    # 1. GET search_arch2
    r1 = opener.open(urllib.request.Request(cat_url, headers=headers))
    html1 = r1.read().decode('utf-8', errors='ignore')
    
    # Check if there is an IP search limit message already on page
    if "three searches" in html1.lower():
        print(f"Cat {searCat}: 'three searches' notice present")
    
    # 2. Get captcha
    opener.open(urllib.request.Request('https://www.coa.gov.in/app/admin/captcha/php_captcha.php', headers=headers))
    r_cap = opener.open(urllib.request.Request('https://www.coa.gov.in/app/admin/captcha/ajax_captcha.php', headers=headers))
    captcha = r_cap.read().decode('utf-8').strip()
    print(f"Cat {searCat}: Got captcha: {captcha}")
    
    # 3. POST search_architectResult.php
    post_payload = {
        'val_sub': '1',
        'searCat': str(searCat),
        'cap_code': captcha,
        'T3': captcha,
        'submit': 'Search',
        **field_data
    }
    data = urllib.parse.urlencode(post_payload).encode('utf-8')
    action_url = 'https://www.coa.gov.in/search_architectResult.php?lang=1&level=1&linkid=&lid=289'
    req = urllib.request.Request(action_url, data=data, headers={**headers, 'Content-Type': 'application/x-www-form-urlencoded'})
    
    r_res = opener.open(req)
    res_html = r_res.read().decode('utf-8', errors='ignore')
    print(f"Cat {searCat}: Response length: {len(res_html)}")
    
    with open(f'scratch/cat_{searCat}_res.html', 'w', encoding='utf-8') as f:
        f.write(res_html)
        
    if '<script>window.location=' in res_html:
        print(f"Cat {searCat}: Redirected via JS")
    else:
        print(f"Cat {searCat}: SUCCESS! HTML returned without redirect!")

if __name__ == '__main__':
    print("Testing Cat 3 (Registration No): CA/2000/12345...")
    test_cat(3, {'arc_reg': 'CA/2000/12345'})
    print("\nTesting Cat 4 (State: 28 = Andhra Pradesh)...")
    test_cat(4, {'state_id': '28'})
