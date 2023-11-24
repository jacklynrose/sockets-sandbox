import os
from PIL import Image
import json

# Specify the folder where your PNG images are located
folder_path = r'C:\Users\josep\Desktop\images'

# List all PNG files in the folder
png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
images = {}

for png_file in png_files:
    # Load the PNG image
    image_path = os.path.join(folder_path, png_file)
    image = Image.open(image_path)

    pixels = []
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            # Get the pixel value at (x, y)
            pixel_value = image.getpixel((x, y))

            # Check if the pixel is black or white (all channels are 0 or 255)
            is_black = (pixel_value[3] == 0)
            is_white = (pixel_value[3] != 0)

            if is_white is True:
                pixels.append((x, y))

    images[png_file.replace('.png', '')] = {
        'size': [image.size[0], image.size[1]],
        'pizel_values': pixels
    }

with open(r'C:\Users\josep\Desktop\images\images.json', 'w') as f:
    json.dump(images, f)
