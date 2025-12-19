
import os
import glob
import re

def update_en_root_files():
    files = glob.glob('en/*.html')
    print(f"Found {len(files)} EN root files.")
    
    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content

        # 1. Remove existing switchers (Desktop and Mobile)
        regex_remove = re.compile(r'<!-- (Mobile )?Language S(witcher|elector) -->\s*<div.*?>.*?</div>', re.DOTALL)
        new_content = regex_remove.sub('', new_content)
        
        # Also remove the one in en/index.html if it doesn't match the comment (it matched <!-- Language Switcher -->)
        # But just in case there are others without comments, or different comments.
        # lines 110-113 in en/index.html matched regex.

        # 2. Insert New Desktop Switcher
        # Find Contacts link. In root en files, it is usually href="contact.html" or "booking.html"
        # <a href="contact.html" class="...">Contacts</a>
        
        desktop_anchor_pattern = r'(<a href="contact\.html"[^>]*>Contacts</a>)'
        
        desktop_switcher = f"""

                    <!-- Language Switcher -->
                    <div class="flex items-center space-x-1 border border-gray-300 rounded-lg overflow-hidden mx-4">
                        <a href="../{filename}" class="px-3 py-1.5 text-sm font-semibold bg-white text-gray-600 hover:bg-gray-100 transition">
                            LT
                        </a>
                        <span class="px-3 py-1.5 text-sm font-semibold bg-blue-500 text-white cursor-default">
                            EN
                        </span>
                    </div>"""
        
        def replace_desktop(match):
            if 'block' in match.group(1): # Skip mobile
                return match.group(1)
            return match.group(1) + desktop_switcher

        new_content = re.sub(desktop_anchor_pattern, replace_desktop, new_content, flags=re.IGNORECASE)

        # 3. Insert New Mobile Switcher
        mobile_anchor_pattern = r'(<a href="contact\.html"[^>]*class="[^"]*block[^"]*"[^>]*>Contacts</a>)'
        
        mobile_switcher = f"""

                <!-- Mobile Language Switcher -->
                <div class="mt-4 mb-2 flex items-center space-x-1 border border-gray-300 rounded-lg overflow-hidden">
                    <a href="../{filename}" class="flex-1 px-3 py-2 text-center text-sm font-semibold bg-white text-gray-600 hover:bg-gray-100 transition">
                        LT
                    </a>
                    <span class="flex-1 px-3 py-2 text-center text-sm font-semibold bg-blue-500 text-white">
                        EN
                    </span>
                </div>"""

        if re.search(mobile_anchor_pattern, new_content, re.IGNORECASE):
            new_content = re.sub(mobile_anchor_pattern, lambda m: m.group(1) + mobile_switcher, new_content, flags=re.IGNORECASE)
        else:
            print(f"Warning: Mobile Contacts link not found in {file_path}")

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes for {file_path}")

if __name__ == "__main__":
    update_en_root_files()
