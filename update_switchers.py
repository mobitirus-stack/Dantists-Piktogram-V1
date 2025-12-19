
import os
import glob
import re

def update_lt_files():
    files = glob.glob('paslaugos/*.html')
    print(f"Found {len(files)} LT files.")
    
    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already updated (simple check)
        if '<!-- Language Switcher -->' in content:
            print(f"Skipping {file_path} (already has switcher)")
            continue

        # Desktop Switcher
        desktop_needle = '<a href="../contact.html" class="text-gray-700 hover:text-blue-500 transition">Kontaktai</a>'
        desktop_replacement = f"""<a href="../contact.html" class="text-gray-700 hover:text-blue-500 transition">Kontaktai</a>

                    <!-- Language Switcher -->
                    <div class="flex items-center space-x-1 border border-gray-300 rounded-lg overflow-hidden mx-4">
                        <span class="px-3 py-1.5 text-sm font-semibold bg-blue-500 text-white cursor-default">
                            LT
                        </span>
                        <a href="../en/paslaugos/{filename}" class="px-3 py-1.5 text-sm font-semibold bg-white text-gray-600 hover:bg-gray-100 transition">
                            EN
                        </a>
                    </div>"""
        
        # Mobile Switcher
        mobile_needle = '<a href="../contact.html" class="block py-2 text-gray-700 hover:text-blue-500">Kontaktai</a>'
        mobile_replacement = f"""<a href="../contact.html" class="block py-2 text-gray-700 hover:text-blue-500">Kontaktai</a>

                <!-- Mobile Language Switcher -->
                <div class="mt-4 mb-2 flex items-center space-x-1 border border-gray-300 rounded-lg overflow-hidden">
                    <span class="flex-1 px-3 py-2 text-center text-sm font-semibold bg-blue-500 text-white">
                        LT
                    </span>
                    <a href="../en/paslaugos/{filename}" class="flex-1 px-3 py-2 text-center text-sm font-semibold bg-white text-gray-600 hover:bg-gray-100 transition">
                        EN
                    </a>
                </div>"""

        new_content = content
        if desktop_needle in new_content:
            new_content = new_content.replace(desktop_needle, desktop_replacement)
        else:
            print(f"Warning: Desktop anchor not found in {file_path}")

        if mobile_needle in new_content:
            new_content = new_content.replace(mobile_needle, mobile_replacement)
        else:
            print(f"Warning: Mobile anchor not found in {file_path}")

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")

def update_en_files():
    files = glob.glob('en/paslaugos/*.html')
    print(f"Found {len(files)} EN files.")
    
    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Determine replacement content
        desktop_replacement = f"""<!-- Language Switcher -->
                    <div class="flex items-center space-x-1 border border-gray-300 rounded-lg overflow-hidden mx-4">
                        <a href="../../paslaugos/{filename}" class="px-3 py-1.5 text-sm font-semibold bg-white text-gray-600 hover:bg-gray-100 transition">
                            LT
                        </a>
                        <span class="px-3 py-1.5 text-sm font-semibold bg-blue-500 text-white cursor-default">
                            EN
                        </span>
                    </div>"""
        
        mobile_replacement = f"""<!-- Mobile Language Switcher -->
                <div class="mt-4 mb-2 flex items-center space-x-1 border border-gray-300 rounded-lg overflow-hidden">
                    <a href="../../paslaugos/{filename}" class="flex-1 px-3 py-2 text-center text-sm font-semibold bg-white text-gray-600 hover:bg-gray-100 transition">
                        LT
                    </a>
                    <span class="flex-1 px-3 py-2 text-center text-sm font-semibold bg-blue-500 text-white">
                        EN
                    </span>
                </div>"""

        new_content = content

        # Replace Desktop Old Selector
        # Using regex to find the block
        desktop_pattern = re.compile(r'<!-- Language Selector -->\s*<div.*?</div>', re.DOTALL)
        if desktop_pattern.search(new_content):
            new_content = desktop_pattern.sub(desktop_replacement, new_content)
        else:
            print(f"Warning: Desktop Old Selector not found in {file_path}")

        # Replace Mobile Old Selector
        mobile_pattern = re.compile(r'<!-- Mobile Language Selector -->\s*<div.*?</div>', re.DOTALL)
        if mobile_pattern.search(new_content):
            new_content = mobile_pattern.sub(mobile_replacement, new_content)
        else:
            print(f"Warning: Mobile Old Selector not found in {file_path}")

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")

if __name__ == "__main__":
    update_lt_files()
    update_en_files()
