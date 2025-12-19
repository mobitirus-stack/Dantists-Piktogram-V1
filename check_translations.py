import os
import re
from pathlib import Path

def is_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def has_latin(text):
    # Check for Latin characters, ignoring common technical terms or short abbreviations might be tricky, 
    # but let's just find any Latin text for now to flag files.
    # We'll ignore HTML tags and attributes roughly by only checking text content.
    # This is a simple heuristic.
    return bool(re.search('[a-zA-Z]', text))

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Very basic HTML parsing to remove tags
    # Remove scripts and styles
    content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style.*?>.*?</style>', '', content, flags=re.DOTALL)
    
    # Remove comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Get text outside of tags
    text_content = re.sub(r'<[^>]+>', ' ', content)
    
    # common words to ignore
    ignored_words = {'Shining', 'Teeth', 'Dr.', 'Danielius', 'Azoulas', 'Ažuolas', 'Book', 'Facebook', 'Instagram', 'Youtube', 'Copyright', 'All', 'rights', 'reserved', 'SEO', 'Meta', 'Tags', 'Open', 'Graph', 'width', 'device-width', 'initial-scale', 'viewport', 'charset', 'UTF-8', 'X-UA-Compatible', 'IE=edge', 'format-detection', 'telephone=no', 'tailwindcss', 'cloudflare', 'font-awesome', 'icon', 'apple-touch-icon', 'manifest', 'theme-color', 'msapplication-TileColor', 'shortcut', 'alternate', 'hreflang', 'x-default', 'stylesheet', 'linear-gradient', 'scroll-behavior', 'border-left', 'background-color', 'bg-gray-50', 'scroll-smooth', 'fixed', 'top-0', 'w-full', 'bg-white', 'shadow-lg', 'z-50', 'container', 'mx-auto', 'px-4', 'flex', 'justify-between', 'items-center', 'py-4', 'space-x-2', 'hover:opacity-80', 'transition', 'text-blue-500', 'text-2xl', 'text-xl', 'font-bold', 'text-gray-800', 'hidden', 'md:flex', 'space-x-6', 'text-gray-700', 'hover:text-blue-500', 'border', 'border-gray-300', 'rounded-lg', 'overflow-hidden', 'mx-4', 'px-3', 'py-1.5', 'text-sm', 'font-semibold', 'text-gray-600', 'hover:bg-gray-100', 'bg-blue-500', 'text-white', 'cursor-default', 'md:hidden', 'space-x-3', 'bg-indigo-500', 'px-4', 'py-2', 'hover:bg-indigo-600', 'id', 'mobile-menu-btn', 'mobile-menu', 'block', 'mt-4', 'mb-2', 'flex-1', 'text-center', 'py-2', 'border-t', 'border-gray-100', 'pt-2', 'font-medium', 'text-gray-300', 'pt-20', 'pb-4', 'border-b', 'border-gray-200', 'ol', 'li', 'fas', 'fa-chevron-right', 'text-gray-400', 'relative', 'py-12', 'md:py-20', 'flex-col', 'md:flex-row', 'gap-12', 'md:w-1/2', 'space-y-6', 'inline-block', 'bg-indigo-100', 'text-indigo-800', 'py-1', 'rounded-full', 'text-4xl', 'md:text-5xl', 'leading-tight', 'text-indigo-600', 'text-gray-900', 'rounded-xl', 'shadow-lg', 'border-2', 'border-gray-200', 'hover:border-indigo-600', 'hover:text-indigo-600', 'mr-2', 'rounded-3xl', 'shadow-2xl', 'md:max-w-lg', 'object-cover', 'transform', 'hover:scale-105', 'duration-700', 'absolute', 'bottom-0', 'left-0', 'right-0', 'bg-gradient-to-t', 'from-black/70', 'to-transparent', 'p-6', 'opacity-90', 'py-16', 'max-w-4xl', 'doctor-quote', 'rounded-r-xl', 'shadow-sm', 'items-start', 'gap-6', 'flex-shrink-0', 'w-24', 'h-24', 'border-4', 'border-white', 'shadow-md', 'mb-2', 'italic', 'leading-relaxed', 'mb-16', 'rounded-2xl', 'shadow-xl', 'mb-6', 'ul', 'space-y-4', 'fa-check-circle', 'text-green-500', 'mr-3', 'grid', 'md:grid-cols-4', 'gap-8', 'w-14', 'h-14', 'justify-center', 'bg-indigo-900', 'bg-white/10', 'backdrop-blur-sm', 'border-white/20', 'hover:bg-white/20', 'text-yellow-400', 'mb-3', 'text-indigo-100', 'mt-12', 'hover:bg-indigo-50', 'hover:shadow-md', 'ml-8', 'border-t', 'md:grid-cols-2', 'w-5', 'hover:text-indigo-700', 'ml-1', 'fa-arrow-right', 'w-16', 'h-16', 'text-xs', 'text-gray-500', 'bg-gray-100', 'hover:bg-gray-200', 'bg-gray-900', 'grid-cols-1', 'text-blue-400', 'fab', 'fa-facebook', 'fa-instagram', 'fa-youtube', 'mb-4', 'fa-phone', 'fa-map-marker-alt', 'fa-envelope', 'pt-8', 'border-gray-800', 'copy', 'LT', 'EN', 'RU', 'I-V', 'VI', 'VII', 'Shining', 'Teeth', 'Booking', 'Contact', 'Services', 'Doctors', 'Home'}

    # Clean up text content
    words = re.findall(r'\b[a-zA-Z]+\b', text_content)
    
    latin_words_found = []
    for word in words:
        if len(word) > 1 and word not in ignored_words and word.lower() not in {w.lower() for w in ignored_words}:
             latin_words_found.append(word)

    if latin_words_found:
        return latin_words_found
    return None

def main():
    services_dir = Path('/Users/dariuslukosius/Downloads/darius 2/ru/services')
    files = sorted(services_dir.glob('*.html'))
    
    print(f"Checking {len(files)} files in {services_dir}...")
    
    for file_path in files:
        result = check_file(file_path)
        if result:
            print(f"\nPotential untranslated content in: {file_path.name}")
            # print(f"Sample words: {result[:10]}")

if __name__ == "__main__":
    main()
