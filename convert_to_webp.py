from PIL import Image
import os

files_to_convert = [
    "Photos/nuotraukos naujos/herro1.jpg",
    "Photos/nuotraukos naujos/dantu tiesinimas kapomis.jpg"
]

for file_path in files_to_convert:
    try:
        img = Image.open(file_path)
        new_path = file_path.rsplit('.', 1)[0] + ".webp"
        img.save(new_path, "WEBP", quality=85)
        print(f"Converted {file_path} to {new_path}")
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
