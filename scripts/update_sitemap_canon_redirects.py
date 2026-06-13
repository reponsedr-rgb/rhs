#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re
ROOT = Path('/workspaces/rhs')
EXCLUDE = {'assets','lib','.git','node_modules','scripts'}
html_files = [p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE for part in p.parts)]
base = 'https://rusumohighschool.org'

sitemap_entries = []
redirects = []
modified_files = []

for p in sorted(html_files):
    rel = p.relative_to(ROOT).as_posix()
    # Determine canonical URL: index.html -> /
    if rel == 'index.html':
        canonical = base + '/'
        redirect_froms = ['/']
    else:
        canonical = base + '/' + rel
        # clean path candidates: remove .html and possible duplicate dir-name
        # e.g., Contact/Contact.html -> /Contact and /Contact/
        no_ext = '/' + rel[:-5]
        redirects.append((no_ext, '/' + rel, '301'))
        if no_ext.endswith('/' + Path(no_ext).name):
            # also add without double
            redirects.append((no_ext + '/', '/' + rel, '301'))
    # Read file and ensure canonical link in head
    text = p.read_text(encoding='utf-8')
    orig = text
    # Replace existing canonical
    if '<link rel="canonical"' in text:
        text = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{canonical}">', text, flags=re.I)
    else:
        # insert before </head>
        if '</head>' in text:
            text = text.replace('</head>', f'    <link rel="canonical" href="{canonical}">\n</head>')
    if text != orig:
        p.write_text(text, encoding='utf-8')
        modified_files.append(str(p.relative_to(ROOT)))
    # sitemap entry
    lastmod = datetime.utcfromtimestamp(p.stat().st_mtime).date().isoformat()
    sitemap_entries.append({'loc': canonical, 'lastmod': lastmod, 'priority': '0.7'})

# Ensure index priority 1.0
for e in sitemap_entries:
    if e['loc'].endswith('/') and e['loc'] == base + '/':
        e['priority'] = '1.0'

# Write sitemap.xml
sitemap_path = ROOT / 'sitemap.xml'
lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for e in sitemap_entries:
    lines.append('  <url>')
    lines.append(f'    <loc>{e["loc"]}</loc>')
    lines.append(f'    <lastmod>{e["lastmod"]}</lastmod>')
    lines.append(f'    <changefreq>weekly</changefreq>')
    lines.append(f'    <priority>{e["priority"]}</priority>')
    lines.append('  </url>')
lines.append('</urlset>')
sitemap_path.write_text('\n'.join(lines), encoding='utf-8')

# Write Netlify _redirects
redirects_path = ROOT / '_redirects'
r_lines = []
# dedupe redirects
seen = set()
for src, dst, code in redirects:
    key = (src, dst)
    if key in seen:
        continue
    seen.add(key)
    r_lines.append(f'{src} {dst} {code}')
# Also redirect bare paths without extension for nested files: /Contact/Contact.html -> /Contact/Contact.html (no change) skipped
redirects_path.write_text('\n'.join(r_lines) + '\n', encoding='utf-8')

print('Canonical tags updated in files:')
for m in modified_files:
    print(m)
print('\nWrote sitemap.xml with %d entries' % len(sitemap_entries))
print('Wrote _redirects with %d rules' % len(r_lines))
