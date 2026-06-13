#!/usr/bin/env python3
"""
Structured Data Validation Script
Checks JSON-LD validity and suggests fixes for Google Rich Results.
"""
import re
import json
from pathlib import Path

ROOT = Path('/workspaces/rhs')
EXCLUDE_DIRS = {'assets','lib','.git','node_modules'}
html_files = [p for p in ROOT.rglob('*.html') if not any(part in EXCLUDE_DIRS for part in p.parts)]

issues = []

for path in html_files:
    text = path.read_text(encoding='utf-8')
    
    # Extract all JSON-LD blocks
    jsonld_blocks = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.I | re.S)
    
    for i, block in enumerate(jsonld_blocks):
        try:
            # Clean block
            block_clean = block.strip()
            data = json.loads(block_clean)
            
            # Basic validation checks
            if '@context' not in data:
                issues.append((path.name, f'JSON-LD block {i+1}: Missing @context'))
            
            if '@type' not in data:
                issues.append((path.name, f'JSON-LD block {i+1}: Missing @type'))
            
            # Type-specific checks
            schema_type = data.get('@type')
            
            if schema_type == 'Organization':
                if 'name' not in data:
                    issues.append((path.name, 'Organization: Missing "name" field'))
                if 'url' not in data:
                    issues.append((path.name, 'Organization: Missing "url" field'))
                if 'logo' not in data:
                    issues.append((path.name, 'Organization: Missing "logo" field (recommended)'))
                if 'contactPoint' not in data:
                    issues.append((path.name, 'Organization: Missing "contactPoint" (recommended)'))
            
            elif schema_type == 'BreadcrumbList':
                if 'itemListElement' not in data:
                    issues.append((path.name, 'BreadcrumbList: Missing "itemListElement"'))
                else:
                    for item in data.get('itemListElement', []):
                        if 'position' not in item or 'name' not in item or 'item' not in item:
                            issues.append((path.name, f'BreadcrumbList: Item missing position/name/item: {item}'))
            
            elif schema_type == 'FAQPage':
                if 'mainEntity' not in data or not data['mainEntity']:
                    issues.append((path.name, 'FAQPage: Missing or empty "mainEntity"'))
                else:
                    for qa in data.get('mainEntity', []):
                        if '@type' not in qa or qa['@type'] != 'Question':
                            issues.append((path.name, 'FAQPage: mainEntity must be "Question" type'))
                        if 'name' not in qa or 'acceptedAnswer' not in qa:
                            issues.append((path.name, 'FAQPage: Question missing "name" or "acceptedAnswer"'))
            
            elif schema_type == 'EducationalOrganization':
                if 'name' not in data:
                    issues.append((path.name, 'EducationalOrganization: Missing "name"'))
                if 'url' not in data:
                    issues.append((path.name, 'EducationalOrganization: Missing "url"'))
                if 'address' not in data:
                    issues.append((path.name, 'EducationalOrganization: Missing "address" (recommended)'))
        
        except json.JSONDecodeError as e:
            issues.append((path.name, f'JSON-LD block {i+1}: Invalid JSON — {str(e)[:60]}'))
        except Exception as e:
            issues.append((path.name, f'JSON-LD block {i+1}: {str(e)[:80]}'))

# Report
print('=== Structured Data Validation Report ===\n')
if not issues:
    print('✓ All JSON-LD snippets are valid!')
    print('⊙ Next: Test with Google Rich Results Test (https://search.google.com/test/rich-results)')
else:
    print(f'Found {len(issues)} issue(s):\n')
    for file, issue in issues:
        print(f'{file}: {issue}')

print(f'\n\n=== Manual Testing (Google Rich Results) ===')
print('Visit: https://search.google.com/test/rich-results')
print('Paste your site URL to check for rich snippets:')
print('- Organization details (logo, name, contact)')
print('- BreadcrumbList navigation')
print('- FAQ snippet eligibility')
print('\nIf any snippets fail, the tool will show exact fixes needed.')
