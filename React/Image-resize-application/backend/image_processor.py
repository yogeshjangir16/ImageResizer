from PIL import Image
import os

# Define the required image sizes
sizes = [(300, 250), (728, 90), (160, 600), (300, 600)]

def resize_image(image_path, output_folder):
    """ Resizes the uploaded image into multiple sizes and saves them. """
    image = Image.open(image_path)
    resized_paths = []
    
    for size in sizes:
        resized_img = image.resize(size, Image.ANTIALIAS)
        resized_path = os.path.join(output_folder, f"{size[0]}x{size[1]}_{os.path.basename(image_path)}")
        resized_img.save(resized_path)
        resized_paths.append(resized_path)
    
    return resized_paths