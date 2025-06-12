from PIL import Image
import os
from urllib.parse import urlparse

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def upscale_image(input_path, output_path, target_size=(640, 640)):
    try:
        # Open the input image
        img = Image.open(input_path)
        
        # Calculate aspect ratio
        original_width, original_height = img.size
        target_width, target_height = target_size
        aspect_ratio = min(target_width / original_width, target_height / original_height)
        
        # Resize while maintaining aspect ratio
        new_width = int(original_width * aspect_ratio)
        new_height = int(original_height * aspect_ratio)
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a new blank image with target size and white background
        final_img = Image.new('RGB', target_size, (255, 255, 255))
        
        # Paste the resized image in the center
        offset = ((target_width - new_width) // 2, (target_height - new_height) // 2)
        final_img.paste(resized_img, offset)
        
        # Save the output image
        final_img.save(output_path, quality=95)
        print(f"Image successfully upscaled and saved to {output_path}")
        
    except Exception as e:
        print(f"Error upscaling {input_path}: {str(e)}")