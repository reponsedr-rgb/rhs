#!/usr/bin/env python3
from pathlib import Path
import re
ROOT = Path('/workspaces/rhs')
EXCLUDE = {'assets','lib','.git','node_modules'}
files = [p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE for part in p.parts)]
modified = []
for path in files:
    text = path.read_text(encoding='utf-8')
    orig = text
    # Add phone click event
    # tel links
    def add_onclick_tel(match):
        tag = match.group(0)
        if "gtag('event'" in tag or 'onclick=' in tag:
            return tag
        # extract phone
        m = re.search(r'href=["\']tel:([^"\']+)["\']', tag)
        phone = m.group(1) if m else ''
        onclick = f" onclick=\"gtag('event','phone_click',{{'phone':'{phone}'}})\""
        # insert before closing > (but after any existing attributes)
        tag = tag[:-1] + onclick + '>'
        return tag
    text = re.sub(r'<a\b[^>]*href=["\']tel:[^"\']+["\'][^>]*>', add_onclick_tel, text, flags=re.I)

    # WhatsApp links (wa.me)
    def add_onclick_wa(match):
        tag = match.group(0)
        if "gtag('event'" in tag or 'onclick=' in tag:
            return tag
        m = re.search(r'href=["\'](https?:)?//wa\.me/([^"\']+)["\']', tag)
        phone = m.group(2) if m else ''
        onclick = f" onclick=\"gtag('event','whatsapp_click',{{'phone':'{phone}'}})\""
        tag = tag[:-1] + onclick + '>'
        return tag
    text = re.sub(r'<a\b[^>]*href=["\'](?:https?:)?//wa\.me/[^"\']+["\'][^>]*>', add_onclick_wa, text, flags=re.I)

    # Forms: add onsubmit if missing (only for forms likely contact/reg)
    def add_onsubmit_form(match):
        tag = match.group(0)
        if 'onsubmit=' in tag:
            return tag
        # add generic event
        onsubmit = " onsubmit=\"gtag('event','contact_form_submit',{'form_name':'contact_form'});\""
        tag = tag[:-1] + onsubmit + '>'
        return tag
    text = re.sub(r'<form\b(?![^>]*onsubmit)[^>]*>', add_onsubmit_form, text, flags=re.I)

    if text != orig:
        path.write_text(text, encoding='utf-8')
        modified.append(str(path.relative_to(ROOT)))

print('Modified files:')
for m in modified:
    print(m)
if not modified:
    print('No changes made')
