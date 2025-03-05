import os
import re
import shutil

# Function to extract the content after <start>
def extract_title_from_mmd(mmd_file_path):
    """Extract the title after <start> from the MMD file."""
    with open(mmd_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Search for <start> and capture the content following it
        match = re.search(r'<start>(.*?)\n', content)
        if match:
            # Clean the title by stripping extra spaces
            title = match.group(1).strip()
            return title
        return None

# Function to rename the MMD file based on the extracted title and save it in the new directory
def rename_mmd_file(input_folder_path, output_folder_path):
    """Rename the MMD file based on the content after <start> and save it in a new directory."""
    # Loop through all subfolders and files
    for root, dirs, files in os.walk(input_folder_path):
        for filename in files:
            if filename.endswith(".mmd"):
                mmd_file_path = os.path.join(root, filename)
                title = extract_title_from_mmd(mmd_file_path)

                if title:
                    # Handle hyphens and spaces appropriately
                    new_title = title.replace(" ", "_")  # Replace spaces with underscores
                    if "-" in new_title:
                        new_title = new_title.replace("-", "_")  # Replace hyphens with underscores
                    new_title = new_title + ".mmd"

                    # Create the new folder path in the output directory, preserving folder structure
                    relative_folder_path = os.path.relpath(root, input_folder_path)
                    new_folder_path = os.path.join(output_folder_path, relative_folder_path)
                    os.makedirs(new_folder_path, exist_ok=True)

                    # New path for the renamed MMD file
                    new_mmd_file_path = os.path.join(new_folder_path, new_title)

                    # Copy the MMD file to the new folder
                    shutil.copy2(mmd_file_path, new_mmd_file_path)  # Using copy2 to preserve file metadata
                    print(f"Copied and renamed: {mmd_file_path} to {new_mmd_file_path}")

                    # Move the image folder to the new folder if it exists
                    image_folder_path = os.path.join(root, 'image')
                    if os.path.exists(image_folder_path):
                        new_image_folder_path = os.path.join(new_folder_path, 'image')
                        shutil.move(image_folder_path, new_image_folder_path)
                        print(f"Moved image folder to: {new_image_folder_path}")

# Set the path to your top-level folder containing MMD files
input_dir = "/Users/vedantaryan/Desktop/MERGED_8_BIO_THEORY_MMD more/output2"

# Set the output folder path where you want the renamed files to be saved
output_dir = "/Users/vedantaryan/Desktop/MERGED_8_BIO_THEORY_MMD more/output_new"

# Rename the MMD files based on their content and save in the new folder
rename_mmd_file(input_dir, output_dir)
