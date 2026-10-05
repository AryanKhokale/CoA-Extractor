with open('scratch/ver_res.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
idx = html.find('CA/1975/00005')
if idx != -1:
    print("Found registration number in HTML:")
    print(html[idx-100:idx+500])
else:
    print("Not found in response.")
    # check for error message or alert
    alerts = re.findall(r'<div[^>]+class=["\'](?:[^"\']*alert|[^"\']*error|[^"\']*message)[^"\']*["\'][^>]*>(.*?)</div>', html, re.DOTALL | re.I)
    print("Alerts:", alerts)
    scripts = re.findall(r'alert\((.*?)\)', html)
    print("JS alerts:", scripts)
