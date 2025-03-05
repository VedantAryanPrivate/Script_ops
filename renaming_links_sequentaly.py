import os
import re

# Define the input and output directories
input_dir = "/Users/vedantaryan/Desktop/MERGED_8_BIO_THEORY_MMD more"
output_dir = "/Users/vedantaryan/Desktop/MERGED_8_BIO_THEORY_MMD more/linkedited"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Regular expression to find image URLs inside the ![]()
image_url_pattern = re.compile(r'!\[\]\((https?://[^\)]+)\)')

def rename_image_links_in_file(mmd_file_path):
    # Read the content of the MMD file
    with open(mmd_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all image URLs
    image_urls = re.findall(image_url_pattern, content)

    # Initialize a counter for sequential numbering
    counter = 1

    # Replace the image URLs with the new format
    def replace_match(match):
        nonlocal counter
        url = match.group(1)
        # Add the counter at the beginning of the image URL (before ![]())
        new_url = f"{counter:02d}_" + f"![]({url})"
        counter += 1
        return new_url

    # Apply the replacements to the content
    updated_content = re.sub(image_url_pattern, replace_match, content)

    return updated_content

def process_file(input_file_path, output_file_path):
    # Read the file, process it, and write the changes
    updated_content = rename_image_links_in_file(input_file_path)
    
    # Write the updated content to the output directory
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

def process_folder(input_folder_path, output_folder_path):
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith(".mmd"):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, filename)

            # Process each MMD file and save it with the updated links
            process_file(input_file_path, output_file_path)
            print(f"Processed: {filename}")

# Start processing the files in the input folder
process_folder(input_dir, output_dir)

