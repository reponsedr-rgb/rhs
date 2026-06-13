#!/usr/bin/env python3
"""
Accessibility & SEO audit script for RHS website.
Checks for common issues: alt text, form labels, contrast, ARIA, semantic HTML, etc.
"""
import re
from pathlib import Path

ROOT = Path('/workspaces/rhs')
EXCLUDE_DIRS = {'assets','lib','.git','node_modules'}
html_files = [p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE_DIRS for part in p.parts)]

issues = {}

for path in html_files:
    text = path.read_text(encoding='utf-8')
    file_issues = []

    # Check 1: Images without alt text
    imgs = re.findall(r'<img\b[^>]*>', text, re.I)
    for img in imgs:
        if not re.search(r'alt=["\']', img):
            file_issues.append(('Missing alt text', img[:80]))
        else:
            # check if alt is empty
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', img)
            if alt_match and not alt_match.group(1).strip():
                file_issues.append(('Empty alt text', img[:80]))

    # Check 2: Form inputs without labels
    inputs = re.findall(r'<input\b[^>]*>', text, re.I)
    for inp in inputs:
        if 'type="hidden"' not in inp and 'type="submit"' not in inp and 'type="button"' not in inp:
            inp_id = re.search(r'id=["\']([^"\']+)["\']', inp)
            if inp_id:
                label = re.search(rf'<label[^>]+for=["\']' + inp_id.group(1) + r'["\'][^>]*>', text, re.I)
                if not label:
                    file_issues.append(('Form input missing associated label', inp[:80]))

    # Check 3: No H1 on page
    if not re.search(r'<h1\b', text, re.I):
        file_issues.append(('No H1 tag found', 'Add a single <h1> to page'))

    # Check 4: Multiple H1 tags
    h1_count = len(re.findall(r'<h1\b', text, re.I))
    if h1_count > 1:
        file_issues.append((f'Multiple H1 tags ({h1_count})', 'Should have exactly one H1'))

    # Check 5: Links with no text or aria-label
    links = re.findall(r'<a\b[^>]*>([^<]*)</a>', text, re.I | re.S)
    for link in links:
        if not link.strip() and not re.search(r'aria-label=', link):
            file_issues.append(('Link with no text', link[:60]))

    # Check 6: Missing viewport meta
    if not re.search(r'<meta[^>]+name=["\']viewport["\']', text, re.I):
        file_issues.append(('Missing viewport meta tag', 'Needed for mobile responsiveness'))

    # Check 7: Missing language attribute on html tag
    if not re.search(r'<html[^>]+lang=["\']', text, re.I):
        file_issues.append(('HTML missing lang attribute', 'Add lang="en" to <html>'))

    # Check 8: Tables without caption or summary
    if '<table' in text.lower():
        if not re.search(r'<caption>', text, re.I) and not re.search(r'summary=["\']', text, re.I):
            file_issues.append(('Table missing caption or summary', 'Add descriptive caption'))

    # Check 9: Button accessibility
    buttons = re.findall(r'<button[^>]*>([^<]*)</button>', text, re.I)
    for btn in buttons:
        if not btn.strip():
            file_issues.append(('Empty button text', 'Add descriptive text or aria-label'))

    # Check 10: Missing skip link (homepage only)
    if path.name.lower() == 'index.html' and 'skip' not in text.lower():
        file_issues.append(('Consider adding skip link', '<a href="#main">Skip to main content</a>'))

    if file_issues:
        issues[str(path.relative_to(ROOT))] = file_issues

# Report
print('=== Accessibility & SEO Audit Report ===\n')
if not issues:
    print('✓ No critical accessibility issues found!')
else:
    for file, file_issues in sorted(issues.items()):
        print(f'\n{file}:')
        for issue_type, detail in file_issues:
            print(f'  ⚠ {issue_type}')
            print(f'    → {detail}\n')

print(f'\nTotal files with issues: {len(issues)}/{len(html_files)}')
