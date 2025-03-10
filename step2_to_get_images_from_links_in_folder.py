import os
import re
import requests
from urllib.parse import unquote
from PIL import Image
from io import BytesIO

# Define the input and output directories
input_dir = "/Users/vedantaryan/Desktop/MERGED_8_BIO_THEORY_MMD more/output"
output_dir = "/Users/vedantaryan/Desktop/MERGED_8_BIO_THEORY_MMD more/output2"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Regular expression to find image URLs inside the ![]()
image_url_pattern = re.compile(r'(\d{3})_!?\[\]\((https?://[^\)]+)\)')

def download_image(image_url, save_path):
    """Download image from the URL and save it as PNG, sanitizing the URL."""
    # Sanitize the URL by unescaping any special characters like backslashes
    sanitized_url = unquote(image_url)
    
    # Fix any problematic backslashes in the URL (escaping issue in the original URL)
    sanitized_url = sanitized_url.replace("\\", "")
    
    # Check if the URL is valid
    print(f"Downloading image from: {sanitized_url}")
    
    # Download the image
    try:
        response = requests.get(sanitized_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(save_path, "PNG")
            return True
        else:
            print(f"Failed to download image, status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

def process_mmd_file(mmd_file_path, output_folder):
    """Process MMD file to download images and update the links."""
    # Read the content of the MMD file
    with open(mmd_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Initialize a counter for sequential numbering
    images_processed = {}

    def replace_image_links(match):
        # Extract the serial number and URL
        serial_number = match.group(1)
        image_url = match.group(2)
        
        # Create the image folder path for the current chapter/subfolder
        image_folder = os.path.join(output_folder, 'image')
        os.makedirs(image_folder, exist_ok=True)
        
        # Define the new image file name
        image_filename = f"Figure{serial_number}.png"
        image_path = os.path.join(image_folder, image_filename)
        
        # Download and save the image
        if download_image(image_url, image_path):
            # Replace the image link in the content with <FigureXX>
            return f"<Figure{serial_number}>"
        else:
            return match.group(0)  # Return the original if image download failed

    # Replace image URLs with the new format
    updated_content = re.sub(image_url_pattern, replace_image_links, content)

    return updated_content

def process_folder(input_folder_path, output_folder_path):
    """Process all MMD files in the folder."""
    for root, dirs, files in os.walk(input_folder_path):
        for filename in files:
            if filename.endswith(".mmd"):
                input_file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, input_folder_path)
                output_folder = os.path.join(output_folder_path, relative_path)

                # Create output subdirectories
                os.makedirs(output_folder, exist_ok=True)

                output_file_path = os.path.join(output_folder, filename)

                # Process and save the updated MMD file
                updated_content = process_mmd_file(input_file_path, output_folder)
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)
                print(f"Processed and saved: {output_file_path}")

# Start processing the files in the input folder
process_folder(input_dir, output_dir)
