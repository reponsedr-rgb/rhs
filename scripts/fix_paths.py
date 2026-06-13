import re
import pathlib

root = pathlib.Path(__file__).resolve().parents[1]
html_files = list(root.glob('**/*.html'))
print(f'Found {len(html_files)} HTML files')

href_html_re = re.compile(r'(href=\")(?!/|https?:|#|mailto:)([^\"]+?\.html)(\")')
attr_assets_re = re.compile(r'(["\'])(?:\.\./|\./)*(assets/[^"\']+)')
url_assets_re = re.compile(r'(url\(\s*["\']?)(?:\.\./|\./)*(assets/[^"\')]+)(["\']?\s*\))')

for path in html_files:
    if str(path).endswith('.bak'):
        continue
    text = path.read_text(encoding='utf-8')
    orig = text
    # href to html -> root-relative
    text = href_html_re.sub(lambda m: f'{m.group(1)}/{m.group(2)}{m.group(3)}', text)
    # assets paths -> root-relative
    text = attr_assets_re.sub(lambda m: f'{m.group(1)}/{m.group(2)}', text)
    # url('assets/...') -> url('/assets/...')
    text = url_assets_re.sub(lambda m: f"{m.group(1)}/{m.group(2)}{m.group(3)}", text)
    if text != orig:
        path.write_text(text, encoding='utf-8')
        print(f'Updated: {path.relative_to(root)}')
print('Done')
