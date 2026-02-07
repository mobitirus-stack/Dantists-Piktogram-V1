import os
import re

# Mapping of filename -> photo_filename (in Photos/nuotraukos naujos)
# Note: "Dantu gydymas.html" is already done.
image_map = {
    "dantu-protezavimas.html": "Dantu protezai.png",
    "periodontologinis-gydymas.html": "Periodontologinis gydymas.jpg",
    "vaiku-odontologija.html": "Vaiku odontologija.jpg",
    "balinimas-kapomis.html": "balinimas kapomis.jpg",
    "dantu-balinimas-lazeriu.html": "balinimas lazeriu.jpg",
    "dantu-atstatymas-visi-ant-4.html": 'dantu atsatymas "visi ant 4".jpg',
    "dantu-implantavimas.html": "dantu implantavimas.png",
    "dantu-tiesinimas-vaikams.html": "dantu tiesinimas kapomis.jpg",
    "dantu-tiesinimas.html": "dantu tiesinimas.jpg",
    "endodontinis-gydymas.html": "endontontinis gydymas.jpg",
    "estetinis-plombavimas.html": "estetinis plombavimas.jpg",
    "issami-vaiku-dantu-patikra.html": "issami vaiku dantu patikra.jpg",
    "nuodugnus-dantu-bukles-istyrimas.html": "nuodugnus dantu bukles istyrimas.jpg",
    "ortodontinis-gydymas.html": "ortodontis gydymas.jpg",
    "tyrimai-ir-diagnostika.html": "tyrimai ir diagnistika.jpg",
    "dantu-tiesinimas-ortopedija.html": "dantu tiesinimas.jpg",
    
    # Mappings for files without exact name match, using best fit
    "dantu-plombavimas.html": "estetinis plombavimas.jpg",
    "dantu-laminates.html": "estetinis plombavimas.jpg",
    "dantu-implantu-rusys.html": "dantu implantavimas.png",
    "kaulo-priauginimas.html": "dantu implantavimas.png",
    "sinuso-pakelimas.html": "dantu implantavimas.png",
    "vienmomete-implantacija.html": "dantu implantavimas.png",
    "implantacijos-eiga.html": "dantu implantavimas.png", 
    "burnos-higiena.html": "nuodugnus dantu bukles istyrimas.jpg", # Fallback
    "dantu-salinimas.html": "dantu implantavimas.png", # Fallback
}

base_dir = "/Users/dariuslukosius/Desktop/svytintys dantys web/paslaugos"

def replace_hero_image(filename, photo_name):
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename} (not found)")
        return

    with open(filepath, 'r') as f:
        content = f.read()

    # We need to replace the div container we added recently:
    # <div class="rounded-2xl shadow-2xl bg-gradient-to-br ...">
    #     <img src="../Photos/Icons/..." ...>
    # </div>
    
    # Regex to match this specific container structure
    # We match the opening div key classes, then the img inside, then closing div
    container_pattern = r'(<div class="rounded-2xl shadow-2xl bg-gradient-to-br.*?<img src="../Photos/Icons/.*?".*?</div>)'
    
    match = re.search(container_pattern, content, re.DOTALL)
    
    # If not found, maybe it's still the old image style (if my previous script failed/skipped it)
    # <img ... class="rounded-2xl shadow-2xl">
    fallback_pattern = r'(<img[^>]*?class="rounded-2xl shadow-2xl"[^>]*?>)'
    
    # Also check for the specific aesthetic one I might have missed or handled differently
    # class="w-full h-auto object-cover transform..."
    aesthetic_pattern = r'(<img[^>]*?class="w-full h-auto object-cover transform[^"]*"[^>]*?>)'

    original_tag = None
    
    if match:
        original_tag = match.group(1)
        print(f"Found Icon Container in {filename}")
    else:
        # Try fallback
        match_fb = re.search(fallback_pattern, content, re.DOTALL)
        if match_fb:
            original_tag = match_fb.group(1)
            print(f"Found Fallback Image in {filename}")
        else:
             match_aes = re.search(aesthetic_pattern, content, re.DOTALL)
             if match_aes:
                 original_tag = match_aes.group(1)
                 print(f"Found Aesthetic Image in {filename}")

    if original_tag:
        # Extract alt text from original if possible
        alt_match = re.search(r'alt="([^"]+)"', original_tag)
        alt_text = alt_match.group(1) if alt_match else "Paslaugos nuotrauka"
        
        # Build new image tag
        # Use proper relative path formatting
        new_img_tag = f'''<img src="../Photos/nuotraukos naujos/{photo_name}" alt="{alt_text}"
                        class="rounded-3xl shadow-2xl w-full h-auto object-cover transform hover:scale-[1.02] transition duration-500">'''
        
        new_content = content.replace(original_tag, new_img_tag)
        
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"UPDATED: {filename} -> {photo_name}")
    else:
        print(f"NO MATCH found in {filename}")

if __name__ == "__main__":
    for filename, photo_name in image_map.items():
        replace_hero_image(filename, photo_name)
