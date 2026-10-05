with open('scratch/get_search_result.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for l in lines[1035:1150]:
    print(l, end='')
