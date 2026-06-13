#!/usr/bin/env python3
import re
from pathlib import Path
ROOT = Path('/workspaces/rhs')
EXCLUDE_DIRS = {'assets','lib','.git','node_modules'}
html_files = [p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE_DIRS for part in p.parts)]
modified = []

def clean_text(s):
    s = re.sub(r'\s+', ' ', s or '').strip()
    s = re.sub(r'[\n\r\t]+', ' ', s)
    return s

for path in html_files:
    text = path.read_text(encoding='utf-8')
    orig = text

    # --- Header hierarchy ---
    # Find all h1 tags
    h1s = list(re.finditer(r'<h1\b[^>]*>(.*?)</h1>', text, re.I | re.S))
    if len(h1s) > 1:
        # keep first, change others to h2
        for m in h1s[1:]:
            old = m.group(0)
            inner = m.group(1)
            new = f'<h2>{inner}</h2>'
            text = text.replace(old, new)
    # If no h1, insert a visually-hidden one after <body>
    if not h1s:
        text = re.sub(r'(<body[^>]*>)', r"\1\n    <h1 class='visually-hidden'>Rusumo High School</h1>", text, count=1, flags=re.I)

    # Ensure at least one H2 exists; if none, promote first h3 or insert generic H2 after first H1
    if not re.search(r'<h2\b', text, re.I):
        m_h3 = re.search(r'<h3\b[^>]*>(.*?)</h3>', text, re.I | re.S)
        if m_h3:
            # replace first h3 with h2
            text = text.replace(m_h3.group(0), f'<h2>{m_h3.group(1)}</h2>', 1)
        else:
            # insert generic H2 after first h1
            text = re.sub(r'(</h1>)', r'\1\n    <h2>Overview</h2>', text, count=1, flags=re.I)

    # --- Per-page title & meta description ---
    # Determine page_name from first h1 or filename
    m_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)
    if m_h1:
        page_name = clean_text(re.sub(r'<[^>]+>', '', m_h1.group(1)))
    else:
        page_name = path.stem.replace('-', ' ').replace('_', ' ').title()

    # Title
    title_re = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    desired_title = 'Rusumo High School (RHS) | Official Website' if path.name.lower() in ('index.html','home.html') else f"{page_name} | Rusumo High School (RHS)"
    if title_re:
        cur_title = clean_text(title_re.group(1))
        if cur_title.lower() in ('rusumo high school','home','welcome','') or not cur_title:
            text = re.sub(r'<title>.*?</title>', f'<title>{desired_title}</title>', text, flags=re.I | re.S)
        else:
            # if title doesn't contain RHS, append suffix for branding
            if 'rusumo' not in cur_title.lower() and 'rhs' not in cur_title.lower():
                text = re.sub(r'<title>.*?</title>', f'<title>{cur_title} | Rusumo High School (RHS)</title>', text, flags=re.I | re.S)
    else:
        text = re.sub(r'(<head[^>]*>)', f"\1\n    <title>{desired_title}</title>", text, count=1, flags=re.I)

    # Meta description
    desc_re = re.search(r'<meta[^>]+name=["\']description["\'][^>]*>', text, re.I)
    sample_desc = f'{page_name} — Rusumo High School (RHS) in Kirehe, Rwanda. Learn about programs, admissions, campus life, and contact details.'
    if desc_re:
        # check if content empty
        if re.search(r'content=["\']\s*["\']', desc_re.group(0)):
            text = text.replace(desc_re.group(0), f'<meta name="description" content="{sample_desc}">')
    else:
        # insert meta description in head
        text = re.sub(r'(<head[^>]*>)', f"\1\n    <meta name=\"description\" content=\"{sample_desc}\">", text, count=1, flags=re.I)

    # Ensure keywords meta includes location and programs
    kw_re = re.search(r'<meta[^>]+name=["\']keywords["\'][^>]*>', text, re.I)
    kw_value = f'Rusumo High School, RHS, Kirehe, Rwanda, {page_name}'
    if kw_re:
        # replace empty or generic
        if re.search(r'content=["\']\s*["\']', kw_re.group(0)):
            text = text.replace(kw_re.group(0), f'<meta name="keywords" content="{kw_value}">')
    else:
        text = re.sub(r'(<head[^>]*>)', f"\1\n    <meta name=\"keywords\" content=\"{kw_value}\">", text, count=1, flags=re.I)

    # --- Image optimizations ---
    # For each <img ...> tag, add alt if missing, add loading="lazy" and decoding="async"
    def img_repl(match):
        tag = match.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', tag)
        src = src_match.group(1) if src_match else ''
        # derive alt from filename
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', tag)
        if alt_match and alt_match.group(1).strip():
            alt = alt_match.group(1).strip()
        else:
            fname = src.split('/')[-1].split('?')[0]
            name = re.sub(r'[-_]+', ' ', re.sub(r'\.[a-zA-Z0-9]+$', '', fname))
            alt = name.title() if name else 'Rusumo High School image'
            if alt_match:
                tag2 = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{alt}"', tag)
                tag = tag2
            else:
                tag = tag[:-1] + f' alt="{alt}">'
        # add loading
        if 'loading=' not in tag:
            tag = tag.replace('>', ' loading="lazy">')
        # add decoding
        if 'decoding=' not in tag:
            tag = tag.replace('>', ' decoding="async">')
        # add srcset if missing (simple fallback)
        if 'srcset=' not in tag:
            tag = tag.replace('>', f' srcset="{src} 1x">')
        return tag

    text = re.sub(r'<img\b[^>]*>', img_repl, text, flags=re.I)

    # --- Write back if changed ---
    if text != orig:
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_text(orig, encoding='utf-8')
        path.write_text(text, encoding='utf-8')
        modified.append(str(path.relative_to(ROOT)))

# report
print('Modified files:')
for m in modified:
    print(m)
if not modified:
    print('No files modified.')
