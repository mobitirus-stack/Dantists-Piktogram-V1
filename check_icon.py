from PIL import Image

def check_image_bbox(path):
    img = Image.open(path)
    print(f"Image format: {img.format}")
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")
    bbox = img.getbbox()
    if bbox:
        print(f"Content bounding box: {bbox}")
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        print(f"Content dimensions: {width}x{height}")
        
        # Calculate empty space
        total_area = img.size[0] * img.size[1]
        content_area = width * height
        print(f"Content fills {content_area/total_area*100:.2f}% of the canvas")
    else:
        print("Image is completely transparent!")

if __name__ == "__main__":
    check_image_bbox("/Users/dariuslukosius/Desktop/svytintys dantys web/Photos/Icons/dental-treatment.png")
