import os
import re
# Directory to scan
target_dir = "/Users/dariuslukosius/Downloads/darius 2/ru/services"

# collected strings set to avoid duplicates
unique_strings = set()

def extract_text_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to extract content specifically from user-visible tags that typically contain descriptions/FAQs
    # Targeting: <p>, <li>, <h3>, <h4>, <span> (if reasonable length)
    
    # Simple regex extraction to avoid heavy soup parsing dependency if not installed, 
    # but BS4 is safer for exact text. Let's assume BS4 might not be available in standard env?
    # Actually, standard env usually doesn't have bs4. I should check or use regex.
    # I will use Regex for robustness in restricted env.
    
    # 1. Paragraphs <p>...</p>
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for p in paragraphs:
        clean_text = re.sub(r'<[^>]+>', '', p).strip() # Remove inner tags
        clean_text = re.sub(r'\s+', ' ', clean_text) # Normalize whitespace
        if len(clean_text) > 2 and "{" not in clean_text: # Skip empty or code-like
            unique_strings.add(clean_text)
            
    # 2. List items <li>...</li>
    list_items = re.findall(r'<li[^>]*>(.*?)</li>', content, re.DOTALL)
    for li in list_items:
        clean_text = re.sub(r'<[^>]+>', '', li).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        if len(clean_text) > 2:
            unique_strings.add(clean_text)

    # 3. Headings h3, h4 for FAQ questions etc
    headings = re.findall(r'<h[34][^>]*>(.*?)</h[34]>', content, re.DOTALL)
    for h in headings:
        clean_text = re.sub(r'<[^>]+>', '', h).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        if len(clean_text) > 2:
            unique_strings.add(clean_text)

def run():
    for f in os.listdir(target_dir):
        if f.endswith(".html"):
            extract_text_from_file(os.path.join(target_dir, f))
            
    # Sort and print
    # We sort by length to potential help translation order (longest first)
    sorted_strings = sorted(list(unique_strings), key=len, reverse=True)
    
    # Output to a file or stdout
    # I will print to stdout to capture in tool output
    for s in sorted_strings:
        # Filter out numbers or very short garbage
        if len(s) < 3: continue
        if "&nbsp;" in s: continue 
        print(f"|||{s}|||")

if __name__ == "__main__":
    run()
