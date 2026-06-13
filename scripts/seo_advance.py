#!/usr/bin/env python3
import re
from pathlib import Path
ROOT = Path('/workspaces/rhs')
EXCLUDE_DIRS = {'assets','lib','.git','node_modules'}
html_files = [p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE_DIRS for part in p.parts)]

BASE_URL = 'https://rusumohighschool.org'
modified = []

GA4_SNIPPET = '''<!-- Google Analytics (GA4) - replace G-PNQVXH2VSV with your ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PNQVXH2VSV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);} 
  gtag('js', new Date());
  gtag('config', 'G-PNQVXH2VSV');
</script>
<!-- End GA4 -->\n'''

SECURITY_HEADERS_NETLIFY = '''/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Feature-Policy: vibrate 'none'; geolocation 'none'
  Content-Security-Policy: default-src 'self' https:; img-src 'self' data: https:; script-src 'self' https://www.googletagmanager.com https://www.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; frame-ancestors 'none'
  Cache-Control: public, max-age=31536000, immutable
'''

# Collect images for image sitemap
images = []
for img in (ROOT / 'assets' / 'img').glob('*'):
    if img.is_file():
        images.append(img)

# Process HTML files
for path in html_files:
    text = path.read_text(encoding='utf-8')
    orig = text

    # Add preload for main CSS if not present
    if 'rel="preload" href="assets/css/style.css"' not in text:
        text = re.sub(r'(<head[^>]*>)', r"\1\n    <link rel=\"preload\" href=\"assets/css/style.css\" as=\"style\" onload=\"this.rel='stylesheet'\">\n    <noscript><link rel=\"stylesheet\" href=\"assets/css/style.css\"></noscript>", text, count=1, flags=re.I)

    # Preload hero image on index and our-school pages
    if path.name.lower() in ('index.html','our-school.html') and 'rel="preload" href="assets/img/hero.jpg"' not in text:
        text = re.sub(r'(<head[^>]*>)', r"\1\n    <link rel=\"preload\" href=\"assets/img/hero.jpg\" as=\"image\">", text, count=1, flags=re.I)

    # Defer non-critical scripts (main.js, animations.js)
    text = re.sub(r'<script([^>]*?)src=("|\')(assets/js/main.js)("|\')([^>]*)>', r'<script\1src="assets/js/main.js" defer>', text, flags=re.I)
    text = re.sub(r'<script([^>]*?)src=("|\')(assets/js/animations.js)("|\')([^>]*)>', r'<script\1src="assets/js/animations.js" defer>', text, flags=re.I)

    # Add rel=preconnect for Google fonts if missing
    if 'rel="preconnect" href="https://fonts.gstatic.com"' not in text:
        text = re.sub(r'(<head[^>]*>)', r"\1\n    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>", text, count=1, flags=re.I)

    # Insert GA4 snippet if not present
    if 'gtag(' not in text:
        text = re.sub(r'(<head[^>]*>)', r"\1\n    %s" % GA4_SNIPPET, text, count=1, flags=re.I)

    # Insert BreadcrumbList JSON-LD if not present
    if 'BreadcrumbList' not in text:
        # create breadcrumbs from path
        parts = list(path.relative_to(ROOT).parts)
        crumbs = []
        url = BASE_URL
        position = 1
        crumbs.append({"name": "Home", "item": BASE_URL + '/'})
        for p in parts[:-1]:
            if p.lower().endswith('.html'):
                continue
            url = url + '/' + p if not url.endswith('/') else url + p
            crumbs.append({"name": p.replace('-', ' ').title(), "item": url + '/'})
        # prepare json
        items = []
        pos = 1
        for c in crumbs:
            items.append({'@type':'ListItem','position':pos,'name':c['name'],'item':c['item']})
            pos += 1
        ld = '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[' + ','.join([str(i).replace("'","\"") for i in items]) + ']}'
        text = re.sub(r'(<head[^>]*>)', r"\1\n    <script type=\"application/ld+json\">%s</script>" % ld, text, count=1, flags=re.I)

    # Add FAQ structured data to FAQ page
    if path.name.lower() == 'faq.html' and 'FAQPage' not in text:
        faq_ld = {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': [
                {'@type': 'Question', 'name': 'How do I apply?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Visit the Admissions page and follow application instructions.'}},
                {'@type': 'Question', 'name': 'Where is RHS located?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Rusumo High School is located in Kigina Sector, Kirehe District, Rwanda.'}}
            ]
        }
        import json
        text = re.sub(r'(<head[^>]*>)', r"\1\n    <script type=\"application/ld+json\">%s</script>" % json.dumps(faq_ld), text, count=1, flags=re.I)

    if text != orig:
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_text(orig, encoding='utf-8')
        path.write_text(text, encoding='utf-8')
        modified.append(str(path.relative_to(ROOT)))

# Generate image sitemap
img_sitemap = ROOT / 'image-sitemap.xml'
with img_sitemap.open('w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n')
    for img in images:
        loc = BASE_URL + '/assets/img/' + img.name
        f.write('  <url>\n')
        f.write(f'    <loc>{BASE_URL}/</loc>\n')
        f.write('    <image:image>\n')
        f.write(f'      <image:loc>{loc}</image:loc>\n')
        f.write('    </image:image>\n')
        f.write('  </url>\n')
    f.write('</urlset>\n')

# Write security headers file for Netlify/Nginx
(ROOT / '_headers').write_text(SECURITY_HEADERS_NETLIFY, encoding='utf-8')

# Update sitemap.xml to include image-sitemap
smap = ROOT / 'sitemap.xml'
if smap.exists():
    s = smap.read_text(encoding='utf-8')
    if 'image-sitemap.xml' not in s:
        # append comment with instruction
        s = s.replace('</urlset>', '</urlset>\n<!-- Image sitemap: image-sitemap.xml -->')
        smap.write_text(s, encoding='utf-8')

# Output
print('Modified HTML files:')
for m in modified:
    print(m)
print('Image sitemap generated:', img_sitemap.name)
print('Security headers file created: _headers')
