with open('scratch/search_result.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="maincont"')
if idx != -1:
    print(html[idx:idx+4000])
else:
    print("No maincont found")
