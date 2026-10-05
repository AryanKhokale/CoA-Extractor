import re

with open('scratch/search_arch.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find forms
forms = re.findall(r'<form\b[^>]*>(.*?)</form>', html, re.DOTALL | re.IGNORECASE)
print(f"Found {len(forms)} form(s)")

for i, form in enumerate(forms):
    print(f"\n--- Form {i+1} ---")
    action = re.search(r'action=["\']([^"\']*)["\']', form, re.I)
    method = re.search(r'method=["\']([^"\']*)["\']', form, re.I)
    name = re.search(r'name=["\']([^"\']*)["\']', form, re.I)
    id_ = re.search(r'id=["\']([^"\']*)["\']', form, re.I)
    print(f"Action: {action.group(1) if action else 'None'}")
    print(f"Method: {method.group(1) if method else 'None'}")
    print(f"Name/ID: {name.group(1) if name else 'None'} / {id_.group(1) if id_ else 'None'}")

    inputs = re.findall(r'<input\b[^>]*>', form, re.I)
    for inp in inputs:
        print(f"  Input: {inp}")

    selects = re.findall(r'<select\b[^>]*name=["\']([^"\']+)["\'][^>]*>(.*?)</select>', form, re.DOTALL | re.I)
    for sname, scontent in selects:
        options = re.findall(r'<option\b[^>]*value=["\']([^"\']*)["\'][^>]*>(.*?)</option>', scontent, re.I)
        print(f"  Select: {sname} ({len(options)} options, first few: {options[:5]})")

# Also print main content area
print("\n--- Main content text snippets ---")
clean_text = re.sub(r'<[^>]+>', ' ', html)
lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
for line in lines[40:100]:
    print(line)
