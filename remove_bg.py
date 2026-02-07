from PIL import Image

def remove_black_background(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Check if the pixel is black (or very dark)
        # item is (r, g, b, a)
        if item[0] < 15 and item[1] < 15 and item[2] < 15:
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")

if __name__ == "__main__":
    input_file = "/Users/dariuslukosius/.gemini/antigravity/brain/2769c2fb-c1d0-4465-92fb-6421460ff97e/dental_treatment_icon_solid_1770390821982.png"
    output_file = "/Users/dariuslukosius/Desktop/svytintys dantys web/Photos/Icons/dental-treatment.png"
    remove_black_background(input_file, output_file)
    print("Background removed and image saved.")
