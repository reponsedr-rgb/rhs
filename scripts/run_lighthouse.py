#!/usr/bin/env python3
"""
Lighthouse Audit Runner
Generates HTML performance reports for Core Web Vitals analysis.
Requires: Node.js and lighthouse CLI
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path('/workspaces/rhs')
REPORT_DIR = ROOT / 'lighthouse-reports'
REPORT_DIR.mkdir(exist_ok=True)

# Domains to test (replace with your domain)
DOMAIN = 'https://rusumohighschool.org'
PAGES = [
    '/',
    '/our-school.html',
    '/admissions/Admissions.html',
    '/gallery/Gallery.html',
]

print('Checking for Lighthouse...')
try:
    result = subprocess.run(['npm', 'list', '-g', 'lighthouse'], capture_output=True, text=True)
    if result.returncode != 0:
        print('Installing Lighthouse globally...')
        subprocess.run(['npm', 'install', '-g', 'lighthouse'], check=True)
except Exception as e:
    print(f'Error: {e}')
    print('Install Node.js first: https://nodejs.org/')
    sys.exit(1)

print('\nRunning Lighthouse audits...\n')

for page in PAGES:
    url = DOMAIN + page
    report_file = REPORT_DIR / f"audit-{page.replace('/', '-').lstrip('-')}-{datetime.now().strftime('%Y%m%d')}.html"
    
    print(f'Auditing: {url}')
    try:
        subprocess.run([
            'lighthouse',
            url,
            f'--output-path={report_file}',
            '--output=html',
            '--chrome-flags=--headless'
        ], check=True)
        print(f'  ✓ Report saved: {report_file}\n')
    except subprocess.CalledProcessError as e:
        print(f'  ✗ Error: {e}\n')

print(f'\nAll reports saved to: {REPORT_DIR}')
print('\nOpen reports in browser to see:')
print('- Performance score (target: 80+)')
print('- Largest Contentful Paint (LCP) — target: < 2.5s')
print('- Cumulative Layout Shift (CLS) — target: < 0.1')
print('- First Input Delay (FID) — target: < 100ms')
print('- Interaction to Next Paint (INP) — target: < 200ms')
