from PIL import Image
import os

def process_image(input_path, output_path):
    print(f"Processing {input_path} -> {output_path}")
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found")
        return

    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Check if the pixel is black (or very dark)
        if item[0] < 15 and item[1] < 15 and item[2] < 15:
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    
    # Trim
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        img.save(output_path, "PNG")
        print(f"Saved to {output_path}")
    else:
        print("Image is empty after background removal")

base_path = "/Users/dariuslukosius/.gemini/antigravity/brain/2769c2fb-c1d0-4465-92fb-6421460ff97e/"
dest_path = "/Users/dariuslukosius/Desktop/svytintys dantys web/Photos/Icons/"

files = [
    ("periodontal_solid_1770391356892.png", "periodontal.png"),
    ("aesthetic_filling_solid_1770391387156.png", "aesthetic-filling.png"),
    ("endodontic_solid_1770391433462.png", "endodontic.png"),
    ("orthodontics_solid_1770391460710.png", "orthodontics.png")
]

for input_file, output_file in files:
    process_image(base_path + input_file, dest_path + output_file)
