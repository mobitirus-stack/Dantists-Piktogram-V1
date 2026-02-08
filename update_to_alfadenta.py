#!/usr/bin/env python3
"""
Batch update script for Alfadenta website customization.
Replaces LamaLocal branding with Alfadenta info across all HTML files.
"""

import os
import re
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent

# Replacement mappings
REPLACEMENTS = [
    # Clinic name
    ("LamaLocal", "Alfadenta"),
    ("Švytintys dantys", "Alfadenta"),
    ("svytintysdantys.lt", "alfadenta.lt"),
    ("Sveiki dantys", "Alfadenta"),
    
    # Phone numbers
    ("+37064195947", "+37037221566"),
    ("+370 64 195 947", "+370 37 221 566"),
    ("tel:+37064195947", "tel:+37037221566"),
    ("+370 5 205 2405", "+370 37 221 566"),
    ("+370 686 24050", "+370 612 03030"),
    
    # Email
    ("info@lamalocal.com", "info@alfadenta.lt"),
    ("info@sveikidantys.lt", "info@alfadenta.lt"),
    
    # Address
    ("Arsenalo g. 1, Vilnius, 01143 Vilniaus m. sav.", "Vytauto pr. 83-2, Kaunas"),
    ("Arsenalo g. 1, Vilnius", "Vytauto pr. 83-2, Kaunas"),
    ("Lvivo g. 25, Vilnius", "Vytauto pr. 83-2, Kaunas"),
    
    # City references in content
    ("Vilniuje", "Kaune"),
    ("Vilnius", "Kaunas"),
    
    # Working hours
    ("I-V: 8:00 - 20:00", "I-V: 9:00 - 16:00"),
    ("I-V: 8:00-20:00", "I-V: 9:00-16:00"),
    ("VI: 8:00 - 14:00", "VI: Nedirbame"),
    ("VI: 8:00-14:00", "VI: Nedirbame"),
    ("08:00", "09:00"),
    ("20:00", "16:00"),
    
    # Footer text
    ("Jūsų šypsenos priežiūra nuo 1999", "Estetinės odontologijos klinika"),
    ("Teikiame kokybišką odontologijos priežiūrą daugiau nei 26 metų.", "Estetinės odontologijos klinika Kauno centre."),
    
    # Postal/geo codes
    ("09100", "44299"),
    ("01143", "44299"),
    ("LT-VL", "LT-KA"),
    
    # Schema.org geo coordinates (Vilnius -> Kaunas city center)
    ("54.7075388", "54.8985"),
    ("25.3040408", "23.9036"),
    ("54.68764222259485", "54.8985"),
    ("25.287434713191896", "23.9036"),
]

# Files to process
HTML_FILES = []

def find_html_files():
    """Find all HTML files in the project."""
    global HTML_FILES
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                HTML_FILES.append(Path(root) / file)
    return HTML_FILES

def update_file(filepath):
    """Apply all replacements to a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for old, new in REPLACEMENTS:
            content = content.replace(old, new)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def update_google_maps_embed():
    """Update Google Maps iframe to show Kaunas location."""
    # New Maps embed for Vytauto pr. 83, Kaunas
    old_iframe = 'src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2306.2492013916103!2d25.287434713191896!3d54.68764222259485!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46dd9419fda9d605%3A0x2503d17455c3ef25!2sLNM%20Naujasis%20arsenalas!5e0!3m2!1slt!2slt!4v1770379870373!5m2!1slt!2slt"'
    
    # Kaunas center location embed
    new_iframe = 'src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2293.7!2d23.9036!3d54.8985!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zVnl0YXV0byBwci4gODMsIEthdW5hcw!5e0!3m2!1slt!2slt"'
    
    for filepath in HTML_FILES:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_iframe in content:
                content = content.replace(old_iframe, new_iframe)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated Maps in: {filepath.name}")
        except Exception as e:
            print(f"Error updating maps in {filepath}: {e}")

def main():
    print("=" * 60)
    print("Alfadenta Website Customization - Batch Update")
    print("=" * 60)
    
    # Find all HTML files
    files = find_html_files()
    print(f"\nFound {len(files)} HTML files to process\n")
    
    # Apply replacements
    updated = 0
    for filepath in files:
        if update_file(filepath):
            print(f"✓ Updated: {filepath.relative_to(BASE_DIR)}")
            updated += 1
        else:
            print(f"  Skipped: {filepath.relative_to(BASE_DIR)} (no changes)")
    
    print(f"\n{'=' * 60}")
    print(f"Completed! Updated {updated} of {len(files)} files")
    print("=" * 60)
    
    # Update Google Maps embeds
    print("\nUpdating Google Maps embeds...")
    update_google_maps_embed()
    
    print("\nDone!")

if __name__ == "__main__":
    main()
