import os
import re
from urllib.parse import urljoin, unquote

# Configuration
PROJECT_ROOT = "/Users/dariuslukosius/Downloads/darius 2"
BASE_URL = "https://svytintysdantys.lt"

def resolve_url(current_file_path, relative_link):
    """
    Resolves a relative link found in an HTML file to an absolute URL.
    """
    # Calculate path relative to project root
    rel_path_from_root = os.path.relpath(current_file_path, PROJECT_ROOT)
    
    # We pretend the file is at BASE_URL + / + rel_path_from_root
    # But urljoin works better if we think in terms of directories.
    # Let's do it via calculating the target file path.
    
    current_dir = os.path.dirname(current_file_path)
    
    # If link is calculation (e.g. just '#'), we handle it separately
    if relative_link == "#" or not relative_link:
        return None

    # Resolve the file path on disk
    # This handles ../ stuff correctly
    target_path = os.path.normpath(os.path.join(current_dir, relative_link))
    
    # Now convert target_path to a web URL relative to root
    web_path = os.path.relpath(target_path, PROJECT_ROOT)
    
    # Ensure forward slashes
    web_path = web_path.replace(os.path.sep, '/')
    
    # Combine with base URL
    # Strip index.html for cleaner URLs if preferred, but for hreflang consistency 
    # it is often safer to be explicit or match canonical. 
    # Let's keep the full filename to be safe and match the file structure exactly.
    # actually, usually main page is simply /, but subpages are .html
    
    return f"{BASE_URL}/{web_path}"

def get_current_page_url(file_path):
    rel_path = os.path.relpath(file_path, PROJECT_ROOT)
    web_path = rel_path.replace(os.path.sep, '/')
    return f"{BASE_URL}/{web_path}"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if no head
    if "</head>" not in content:
        return

    # 1. Extract Links from Language Switcher
    # We look for the standard structure we built: 
    # >LT</a> ... >EN</a> ... >RU</a> (or span for active)
    # This involves regex.
    
    # Regex designed to capture href inside the language switcher block
    # We look for specific patterns like matched to string "LT", "EN", "RU"
    
    links = {}
    
    # Find LT link
    # Matches: <a href="../../paslaugos/..." ...>LT</a>
    match_lt = re.search(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>\s*LT\s*</a>', content, re.IGNORECASE)
    if match_lt:
        links['lt'] = resolve_url(file_path, match_lt.group(1))
    elif re.search(r'<span[^>]*>\s*LT\s*</span>', content, re.IGNORECASE):
        links['lt'] = get_current_page_url(file_path)

    # Find EN link
    match_en = re.search(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>\s*EN\s*</a>', content, re.IGNORECASE)
    if match_en:
        links['en'] = resolve_url(file_path, match_en.group(1))
    elif re.search(r'<span[^>]*>\s*EN\s*</span>', content, re.IGNORECASE):
        links['en'] = get_current_page_url(file_path)
        
    # Find RU link
    match_ru = re.search(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>\s*RU\s*</a>', content, re.IGNORECASE)
    if match_ru:
        links['ru'] = resolve_url(file_path, match_ru.group(1))
    elif re.search(r'<span[^>]*>\s*RU\s*</span>', content, re.IGNORECASE):
        links['ru'] = get_current_page_url(file_path)
        
    # Validation: We need at least 2 links to make sense, but ideally 3
    if not links:
        print(f"Skipping {os.path.basename(file_path)}: No language links found.")
        return

    # 2. Build Hreflang Tags
    hreflang_block = "\n    <!-- Hreflang Tags -->\n"
    
    # x-default: usually the main market language (LT)
    if 'lt' in links and links['lt']:
        hreflang_block += f'    <link rel="alternate" hreflang="x-default" href="{links["lt"]}" />\n'
        hreflang_block += f'    <link rel="alternate" hreflang="lt" href="{links["lt"]}" />\n'
    
    if 'en' in links and links['en']:
        hreflang_block += f'    <link rel="alternate" hreflang="en" href="{links["en"]}" />\n'
        
    if 'ru' in links and links['ru']:
        hreflang_block += f'    <link rel="alternate" hreflang="ru" href="{links["ru"]}" />\n'

    # 3. Insert into Head
    # Remove old hreflang tags if they exist (simple regex clean)
    content = re.sub(r'\s*<link rel="alternate" hreflang="[^"]+" href="[^"]+" />', '', content)
    content = re.sub(r'\s*<!-- Hreflang Tags -->', '', content)
    
    # Insert before </head>
    new_content = content.replace('</head>', f'{hreflang_block}    </head>')
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {os.path.basename(file_path)}")

def run():
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # limit to relevant folders
        if '.git' in root or 'Photos' in root or 'node_modules' in root:
            continue
            
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    run()
