import re

with open('scratch/default_arch.php.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find rows in the table
trs = re.findall(r'<tr\b[^>]*>(.*?)</tr>', html, re.DOTALL | re.I)
print(f"Total rows: {len(trs)}")

for i in range(1, min(6, len(trs))):
    print(f"\n--- Row {i} raw HTML ---")
    print(trs[i])
