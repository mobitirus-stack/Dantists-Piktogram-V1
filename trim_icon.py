from PIL import Image

def trim_image(path):
    img = Image.open(path)
    bbox = img.getbbox()
    if bbox:
        cropped = img.crop(bbox)
        cropped.save(path)
        print(f"Trimmed image saved to {path}")
    else:
        print("Image is empty, nothing to trim")

if __name__ == "__main__":
    trim_image("/Users/dariuslukosius/Desktop/svytintys dantys web/Photos/Icons/dental-treatment.png")
