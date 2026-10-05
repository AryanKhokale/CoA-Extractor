import urllib.request, ssl, re
from html.parser import HTMLParser

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.coa.gov.in', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
except Exception as e:
    print("Fetch error:", e)
    exit(1)

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_tag = None
        self.current_href = ''
        self.current_text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.current_tag = 'a'
            attrs_dict = dict(attrs)
            self.current_href = attrs_dict.get('href', '')
            self.current_text = []

    def handle_endtag(self, tag):
        if tag == 'a':
            text = ' '.join(self.current_text).strip()
            if self.current_href:
                self.links.append((text, self.current_href))
            self.current_tag = None

    def handle_data(self, data):
        if self.current_tag == 'a':
            self.current_text.append(data.strip())

parser = LinkParser()
parser.feed(html)

seen = set()
for text, href in parser.links:
    if any(k in text.lower() or k in href.lower() for k in ['directory', 'register', 'search', 'verify', 'find', 'status', 'architects', 'member']):
        key = (text, href)
        if key not in seen:
            seen.add(key)
            print(f"TEXT: '{text}' -> HREF: '{href}'")
