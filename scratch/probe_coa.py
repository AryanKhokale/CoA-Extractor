import urllib.request
import ssl
import re
from urllib.parse import urljoin

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def probe(url):
    print(f"Fetching {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f"Status: {resp.status}, Content-Length: {len(html)}")
            links = re.findall(r'href=["\']([^"\']+)["\']', html, re.I)
            candidates = set()
            for l in links:
                full = urljoin(url, l)
                if any(w in l.lower() for w in ['architect', 'directory', 'register', 'search', 'verify', 'member']):
                    candidates.add(full)
            print(f"Found {len(candidates)} candidate links:")
            for c in sorted(list(candidates))[:25]:
                print(f"  * {c}")
            return html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

if __name__ == '__main__':
    probe('https://www.coa.gov.in')
