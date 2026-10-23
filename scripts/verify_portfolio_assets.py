import os
import re

PORTFOLIO_ROOT = r'C:\Users\KIIT\OneDrive\Documents\Karan-Portfolio'

def check_file(filename):
    filepath = os.path.join(PORTFOLIO_ROOT, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find asset references ending in media or web extensions
    pattern = re.compile(r'(?:src|href|data-img|image)\s*[:=]\s*["\']([^"\'>#]+\.(?:png|jpg|jpeg|svg|pdf|webp|css|js|json|html))["\']', re.IGNORECASE)
    matches = pattern.findall(content)

    missing = []
    found = []
    for ref in matches:
        if ref.startswith('http') or ref.startswith('mailto:') or ref.startswith('tel:'):
            continue
        # clean query params if any
        clean_ref = ref.split('?')[0].lstrip('./').replace('/', os.sep)
        full_path = os.path.join(PORTFOLIO_ROOT, clean_ref)
        if not os.path.exists(full_path):
            missing.append(ref)
        else:
            found.append(ref)
    return len(found), missing

if __name__ == '__main__':
    for fname in ['index.html', 'planet-hunters.html', 'script.js']:
        count, missing = check_file(fname)
        print(f'{fname}: {count} assets verified on disk. Missing: {missing}')
