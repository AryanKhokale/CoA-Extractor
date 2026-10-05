with open('scratch/search_arch2_cat1.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
idx = html.find('refreshCaptcha')
while idx != -1:
    print("Found refreshCaptcha at:", idx)
    print(html[max(0, idx-200):min(len(html), idx+300)])
    print("="*40)
    idx = html.find('refreshCaptcha', idx+1)
