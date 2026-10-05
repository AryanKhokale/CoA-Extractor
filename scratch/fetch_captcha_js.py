import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.coa.gov.in/app/admin/captcha/captcha.js', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print("Captcha JS content:")
        print(content)
except Exception as e:
    print("Error:", e)
