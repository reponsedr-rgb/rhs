import re
import pathlib
import requests

root = pathlib.Path(__file__).resolve().parents[1]
html_files = list(root.glob('**/*.html'))
asset_re = re.compile(r'(?:href|src)=["\']([^"\']+)["\']')

bad = []
for f in html_files:
    if str(f).endswith('.bak'):
        continue
    text = f.read_text(encoding='utf-8')
    for m in asset_re.findall(text):
        url = m
        if url.startswith(('http://','https://','/assets')):
            # make absolute path for local server
            if url.startswith('/assets'):
                full = f'http://127.0.0.1:8000{url}'
            elif url.startswith('http'):
                full = url
            else:
                continue
            try:
                r = requests.head(full, timeout=5)
                if r.status_code >= 400:
                    bad.append((f.relative_to(root), url, r.status_code))
            except Exception as e:
                bad.append((f.relative_to(root), url, str(e)))

print('Checked assets. Problems:')
for b in bad:
    print(b)
if not bad:
    print('No problems found')
