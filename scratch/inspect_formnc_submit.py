with open('scratch/search_arch2_cat1.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('name="formNC"')
print(html[pos+2500:pos+5000])
