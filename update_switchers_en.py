
import os
import glob
import re

def update_en_files_robust():
    files = glob.glob('en/paslaugos/*.html')
    print(f"Found {len(files)} EN files.")
    
    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content

        # 1. Remove existing switchers (Desktop and Mobile)
        # Patterns to match: <!-- Language Switcher --> ... </div> or <!-- Language Selector --> ... </div>
        # We need to match nested divs? No, usually they are simple.
        # But regex matching matching </div> is risky if nested.
        # Assuming indentation helps or they are not deeply nested.
        # The observed switchers end with </div> and are followed by indentation or </a>.
        
        # A safer way might be to just remove the known patterns I've seen.
        
        # Pattern 1: The one in dantu-implantavimas (Selector)
        # <div class="flex items-center space-x-2 border-l pl-4 border-gray-300">...</div>
        
        # Pattern 2: The one in balinimas-kapomis (Switcher)
        # <div class="flex items-center space-x-2 border rounded-lg p-1">...</div>

        # Pattern 3: Mobile Selector
        # <div class="flex items-center space-x-4 py-2 border-t border-gray-100 mt-2">...</div>

        # I will use a regex that matches the comment + the div.
        # Pattern: <!-- (Mobile )?Language S(witcher|elector) -->\s*<div.*?</div>
        # This relies on the comment being present.
        
        regex_remove = re.compile(r'<!-- (Mobile )?Language S(witcher|elector) -->\s*<div.*?>.*?</div>', re.DOTALL)
        
        # Remove all matches
        new_content = regex_remove.sub('', new_content)

        # 2. Insert New Desktop Switcher
        # Find Contacts link
        # <a href="../contact.html" class="text-gray-700 hover:text-blue-500 transition">Contacts</a>
        desktop_anchor = re.compile(r'(<a href="\.\./contact\.html"[^>]*>Contacts</a>)', re.IGNORECASE)
        
        desktop_switcher = f"""

                    <!-- Language Switcher -->
                    <div class="flex items-center space-x-1 border border-gray-300 rounded-lg overflow-hidden mx-4">
                        <a href="../../paslaugos/{filename}" class="px-3 py-1.5 text-sm font-semibold bg-white text-gray-600 hover:bg-gray-100 transition">
                            LT
                        </a>
                        <span class="px-3 py-1.5 text-sm font-semibold bg-blue-500 text-white cursor-default">
                            EN
                        </span>
                    </div>"""
        
        # We need to insert it only in the Desktop Menu block. 
        # The Desktop Menu usually starts with <!-- Desktop Menu -->
        # But simply replacing the anchor should work as long as I check if I am replacing the desktop one.
        # The desktop anchor usually has class "... transition">Contacts</a>
        # The mobile anchor usually has class "... block ...">Contacts</a>
        
        # Desktop replacement
        def replace_desktop(match):
            # Check if it has 'block' class (Mobile)
            if 'block' in match.group(1):
                return match.group(1) # Skip
            return match.group(1) + desktop_switcher

        new_content = desktop_anchor.sub(replace_desktop, new_content)

        # 3. Insert New Mobile Switcher
        mobile_anchor = re.compile(r'(<a href="\.\./contact\.html"[^>]*class="[^"]*block[^"]*"[^>]*>Contacts</a>)', re.IGNORECASE)
        
        mobile_switcher = f"""

                <!-- Mobile Language Switcher -->
                <div class="mt-4 mb-2 flex items-center space-x-1 border border-gray-300 rounded-lg overflow-hidden">
                    <a href="../../paslaugos/{filename}" class="flex-1 px-3 py-2 text-center text-sm font-semibold bg-white text-gray-600 hover:bg-gray-100 transition">
                        LT
                    </a>
                    <span class="flex-1 px-3 py-2 text-center text-sm font-semibold bg-blue-500 text-white">
                        EN
                    </span>
                </div>"""

        if mobile_anchor.search(new_content):
            new_content = mobile_anchor.sub(lambda m: m.group(1) + mobile_switcher, new_content)
        else:
            print(f"Warning: Mobile Contacts link not found in {file_path}")

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes for {file_path}")

if __name__ == "__main__":
    update_en_files_robust()
