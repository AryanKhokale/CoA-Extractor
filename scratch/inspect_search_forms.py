import re

for cat in [1, 2, 3, 4]:
    fname = f'scratch/search_arch2_cat{cat}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    print(f"\n=================== CAT {cat} ===================")
    forms = re.findall(r'<form\b[^>]*>(.*?)</form>', html, re.DOTALL | re.I)
    for form in forms:
        action = re.search(r'action=["\']([^"\']*)["\']', form, re.I)
        method = re.search(r'method=["\']([^"\']*)["\']', form, re.I)
        name = re.search(r'name=["\']([^"\']*)["\']', form, re.I)
        id_ = re.search(r'id=["\']([^"\']*)["\']', form, re.I)
        
        inputs = re.findall(r'<input\b[^>]*>', form, re.I)
        selects = re.findall(r'<select\b[^>]*name=["\']([^"\']+)["\'][^>]*>(.*?)</select>', form, re.DOTALL | re.I)
        
        # Only show search forms (ignore contrast/search_button header)
        if len(inputs) > 2 or selects:
            print(f"Action: {action.group(1) if action else 'None'} | Method: {method.group(1) if method else 'GET'}")
            print("Inputs:")
            for inp in inputs:
                print(" ", inp)
            for sname, sopt in selects:
                opts = re.findall(r'<option\b[^>]*value=["\']([^"\']*)["\'][^>]*>(.*?)</option>', sopt, re.I)
                print(f" Select: {sname} -> {len(opts)} options, sample: {opts[:5]}")
