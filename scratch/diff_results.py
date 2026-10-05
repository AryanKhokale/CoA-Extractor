with open('scratch/get_search_result.html', 'r', encoding='utf-8') as f:
    h1 = f.read()

with open('scratch/search_result.html', 'r', encoding='utf-8') as f:
    h2 = f.read()

import difflib

# Let's inspect differences
diff = list(difflib.unified_diff(h2.splitlines(), h1.splitlines(), lineterm=''))
print(f"Diff lines count: {len(diff)}")
for line in diff[:80]:
    print(line)
