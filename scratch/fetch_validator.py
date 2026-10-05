import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://www.coa.gov.in/app/admin/scripts/clientChk/jsValidatorv4.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        with open('scratch/jsValidatorv4.js', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Saved jsValidatorv4.js, length:", len(content))
except Exception as e:
    print("Error:", e)
