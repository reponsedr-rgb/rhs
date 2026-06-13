#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path('/workspaces/rhs')
EXCLUDE_DIRS = {'assets','lib','.git','node_modules'}
BASE_URL = 'https://rusumohighschool.org'

html_files = [p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE_DIRS for part in p.parts)]
modified = []

def has_tag(text, pattern):
    return re.search(pattern, text, re.I | re.S) is not None

for path in html_files:
    text = path.read_text(encoding='utf-8')
    original = text

    # Ensure single H1 exists: if no <h1> add visually-hidden after <body>
    if not has_tag(text, r'<h1\b'):
        text = re.sub(r'(<body[^>]*>)', r"\1\n    <h1 class=\"visually-hidden\">Rusumo High School</h1>", text, count=1, flags=re.I)

    # Extract friendly page title from first H1 or filename
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)
    if m:
        page_name = re.sub('<[^<]+?>', '', m.group(1)).strip()
    else:
        page_name = path.stem.replace('-', ' ').replace('_', ' ').title()

    # Build title string
    if path.name.lower() in ('index.html', 'home.html'):
        title_text = 'Rusumo High School (RHS) | Official Website'
    else:
        title_text = f"{page_name} | Rusumo High School (RHS)"

    # Default description for this page (used if none exists)
    description = f'{page_name} — Rusumo High School (RHS). Learn about our programs, admissions, campus life, and contact information.'

    # Ensure <head> exists
    head_match = re.search(r'<head[^>]*>(.*?)</head>', text, re.I | re.S)
    if head_match:
        head = head_match.group(1)
        new_head = head

        # Title
        if has_tag(head, r'<title>'):
            new_head = re.sub(r'<title>.*?</title>', f'<title>{title_text}</title>', new_head, flags=re.I | re.S)
        else:
            new_head = f'<title>{title_text}</title>\n' + new_head

        # Meta description
        if not has_tag(head, r'<meta[^>]+name=["\']description["\']'):
            description = f'{page_name} — Rusumo High School (RHS). Learn about our programs, admissions, campus life, and contact information.'
            new_head = f'<meta name="description" content="{description}">\n' + new_head
        else:
            # if empty description, replace
            new_head = re.sub(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']\s*["\'][^>]*>', '', new_head, flags=re.I)
            if not has_tag(new_head, r'<meta[^>]+name=["\']description["\']'):
                description = f'{page_name} — Rusumo High School (RHS). Learn about our programs, admissions, campus life, and contact information.'
                new_head = f'<meta name="description" content="{description}">\n' + new_head

        # Canonical
        rel_path = '/' + str(path.relative_to(ROOT)).replace('\\','/').lstrip('/')
        canonical_url = BASE_URL + rel_path if not rel_path.endswith('/index.html') else BASE_URL + '/'
        if not has_tag(head, r'<link[^>]+rel=["\']canonical["\']'):
            new_head = f'<link rel="canonical" href="{canonical_url}">\n' + new_head

        # Open Graph & Twitter (minimal)
        if not has_tag(head, r'property=["\']og:title["\']'):
            og = (
                f'<meta property="og:type" content="website">\n'
                f'<meta property="og:title" content="{title_text}">\n'
                f'<meta property="og:description" content="{description}">\n'
                f'<meta property="og:url" content="{canonical_url}">\n'
                f'<meta property="og:image" content="{BASE_URL}/assets/img/hero.jpg">\n'
            )
            new_head = og + new_head
        if not has_tag(head, r'name=["\']twitter:card["\']'):
            tw = (
                '<meta name="twitter:card" content="summary_large_image">\n'
                f'<meta name="twitter:title" content="{title_text}">\n'
                f'<meta name="twitter:description" content="{description}">\n'
                f'<meta name="twitter:image" content="{BASE_URL}/assets/img/hero.jpg">\n'
            )
            new_head = tw + new_head

        # JSON-LD organization (only add once per file)
        if not has_tag(head, r'application/ld\+json'):
            jsonld = (
                '<script type="application/ld+json">\n'
                '{\n'
                '  "@context": "https://schema.org",\n'
                '  "@type": "EducationalOrganization",\n'
                '  "name": "Rusumo High School",\n'
                f'  "url": "{BASE_URL}/",\n'
                f'  "logo": "{BASE_URL}/assets/img/RHS Logo edited.jpg",\n'
                '  "contactPoint": [{\n'
                '    "@type": "ContactPoint",\n'
                '    "telephone": "+250788871560",\n'
                '    "contactType": "Admissions",\n'
                '    "email": "info@rusumohighschool.rw"\n'
                '  }],\n'
                '  "address": {\n'
                '    "@type": "PostalAddress",\n'
                '    "addressLocality": "Kirehe",\n'
                '    "addressCountry": "RW"\n'
                '  }\n'
                '}\n'
                '</script>\n'
            )
            new_head = jsonld + new_head

        # Replace head
        new_text = text[:head_match.start(1)] + new_head + text[head_match.end(1):]
        text = new_text

    # If changed, backup and write
    if text != original:
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_text(original, encoding='utf-8')
        path.write_text(text, encoding='utf-8')
        modified.append(str(path.relative_to(ROOT)))

# Print results
print('Modified files:')
for m in modified:
    print(m)
if not modified:
    print('No files modified.')
