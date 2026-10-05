with open('scratch/search_result.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
# Print lines with meaningful content
for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['result', 'sharma', 'search', 'record', 'not found', 'error', 'limit', 'subscribe', 'captcha']):
        print(f"L{i}: {l.strip()[:150]}")
