import os
import re

# Mapping of filename -> (icon_filename, from_color, to_color)
services_map = {
    # Group 1
    "burnos-higiena.html": ("oral-hygiene.png", "from-green-400", "to-green-600"),
    "balinimas-kapomis.html": ("whitening-trays.png", "from-purple-400", "to-purple-600"),
    "dantu-implantavimas.html": ("dental-implants.png", "from-indigo-400", "to-indigo-600"),
    "dantu-protezavimas.html": ("prosthetics.png", "from-cyan-400", "to-cyan-600"),
    
    # Group 2
    "periodontologinis-gydymas.html": ("periodontal.png", "from-red-400", "to-red-600"),
    "estetinis-plombavimas.html": ("aesthetic-filling.png", "from-teal-400", "to-teal-600"),
    "endodontinis-gydymas.html": ("endodontic.png", "from-lime-400", "to-lime-600"),
    "dantu-tiesinimas-ortopedija.html": ("orthodontics.png", "from-emerald-400", "to-emerald-600"),
    "ortodontinis-gydymas.html": ("orthodontics.png", "from-emerald-400", "to-emerald-600"),

    # Group 3 (Placeholders/Matches)
    "dantu-tiesinimas-vaikams.html": ("whitening-trays.png", "from-purple-400", "to-purple-600"),
    "nuodugnus-dantu-bukles-istyrimas.html": ("dental-treatment.png", "from-blue-400", "to-blue-600"),
    "tyrimai-ir-diagnostika.html": ("dental-treatment.png", "from-teal-400", "to-teal-600"),
    "issami-vaiku-dantu-patikra.html": ("oral-hygiene.png", "from-pink-400", "to-pink-600"),
    "vaiku-odontologija.html": ("oral-hygiene.png", "from-purple-400", "to-purple-600"),
    
    # Group 4
    "dantu-atstatymas-visi-ant-4.html": ("dental-implants.png", "from-cyan-400", "to-cyan-600"),
    "dantu-balinimas-lazeriu.html": ("whitening-trays.png", "from-purple-400", "to-purple-600"),
    
    # Main/Other
    "dantu-gydymas.html": ("dental-treatment.png", "from-blue-400", "to-blue-600"),
    "dantu-tiesinimas.html": ("orthodontics.png", "from-emerald-400", "to-emerald-600"),
    "dantu-plombavimas.html": ("aesthetic-filling.png", "from-teal-400", "to-teal-600"),
    "dantu-salinimas.html": ("dental-implants.png", "from-red-400", "to-red-600"), 
    "dantu-laminates.html": ("aesthetic-filling.png", "from-teal-400", "to-teal-600"), 
    "kaulo-priauginimas.html": ("dental-implants.png", "from-indigo-400", "to-indigo-600"), 
    "sinuso-pakelimas.html": ("dental-implants.png", "from-indigo-400", "to-indigo-600"), 
    "implantacijos-eiga.html": ("dental-implants.png", "from-indigo-400", "to-indigo-600"),
    "vienmomete-implantacija.html": ("dental-implants.png", "from-indigo-400", "to-indigo-600"),
    "dantu-implantu-rusys.html": ("dental-implants.png", "from-indigo-400", "to-indigo-600"),

}

base_dir = "/Users/dariuslukosius/Desktop/svytintys dantys web/paslaugos"

patterns = [
    # Original exact match (rounded-2xl shadow-2xl)
    r'(<img[^>]*?alt="([^"]+)"[^>]*?class="rounded-2xl shadow-2xl"[^>]*?>)',
    # Variation (rounded-2xl shadow-xl)
    r'(<img[^>]*?alt="([^"]+)"[^>]*?class="rounded-2xl shadow-xl[^"]*"[^>]*?>)',
    # Variation (w-full h-auto object-cover transform) - for estetinis
    r'(<img[^>]*?alt="([^"]+)"[^>]*?class="w-full h-auto object-cover transform[^"]*"[^>]*?>)',
    # Variation (w-full h-auto object-cover) - generic fallback for others
    r'(<img[^>]*?alt="([^"]+)"[^>]*?class="w-full h-auto object-cover"[^>]*?>)',
    # Catch-all for "object-cover" if it looks like a main image (risky but last resort)
    r'(<img[^>]*?alt="([^"]+)"[^>]*?class="[^"]*object-cover[^"]*"[^>]*?>)'
]

def update_file(filename, config):
    icon, from_col, to_col = config
    filepath = os.path.join(base_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"Skipping {filename} (not found)")
        return

    with open(filepath, 'r') as f:
        content = f.read()

    # If already updated (contains Photos/Icons), skip
    if f"Photos/Icons/{icon}" in content:
        print(f"Skipping {filename} (already updated)")
        return

    matched = False
    for i, pattern in enumerate(patterns):
        match = re.search(pattern, content, re.DOTALL)
        if match:
            full_img_tag = match.group(1)
            alt_text = match.group(2)
            
            # Sanity check: don't replace small icons or logos
            if "logo" in full_img_tag.lower() or "rounded-full" in full_img_tag:
                continue
                
            print(f"File: {filename} matched pattern {i+1}")
            
            new_html = f'''<div class="rounded-2xl shadow-2xl bg-gradient-to-br {from_col} {to_col} h-64 md:h-96 flex items-center justify-center p-8">
                            <img src="../Photos/Icons/{icon}" alt="{alt_text}" class="w-full h-full object-contain drop-shadow-lg">
                        </div>'''
            
            new_content = content.replace(full_img_tag, new_html)
            
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"UPDATED: {filename}")
            matched = True
            break
    
    if not matched:
        print(f"NO MATCH found for: {filename}")

if __name__ == "__main__":
    for filename, config in services_map.items():
        update_file(filename, config)
