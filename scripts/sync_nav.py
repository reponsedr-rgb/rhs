#!/usr/bin/env python3
from pathlib import Path
import re
ROOT = Path('/workspaces/rhs')
index = ROOT / 'index.html'
if not index.exists():
    raise SystemExit('index.html not found')
text = index.read_text(encoding='utf-8')
# Extract the <nav ...>...</nav> block (greedy)
m = re.search(r'<!-- Navbar Start -->(.*?)<!-- Navbar End -->', text, re.S)
if not m:
    raise SystemExit('Navbar markers not found in index.html')
nav_block = m.group(0)  # include markers

# Find all HTML files to update
EXCLUDE = {'assets','lib','scripts','.git','node_modules'}
files = [p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE for part in p.parts) and p != index]
modified = []
for path in files:
    content = path.read_text(encoding='utf-8')
    # If file already has Navbar markers, replace whole marker section
    if '<!-- Navbar Start -->' in content and '<!-- Navbar End -->' in content:
        new = re.sub(r'<!-- Navbar Start -->(.*?)<!-- Navbar End -->', nav_block, content, flags=re.S)
    else:
        # Fallback: replace first <nav ...>...</nav> occurrence
        if '<nav' in content and '</nav>' in content:
            new = re.sub(r'<nav\b.*?</nav>', nav_block, content, flags=re.S)
        else:
            # No nav found, try to insert after <body>
            if '<body' in content:
                new = re.sub(r'(<body[^>]*>)', r"\1\n" + nav_block, content, count=1, flags=re.S)
            else:
                new = content
    if new != content:
        path.write_text(new, encoding='utf-8')
        modified.append(str(path.relative_to(ROOT)))

print('Replaced nav in files:')
for m in modified:
    print(m)
if not modified:
    print('No changes made')
