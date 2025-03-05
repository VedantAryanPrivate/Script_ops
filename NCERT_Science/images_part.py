import os
import re
import requests
# Set the main directory (CHANGE THIS TO YOUR PATH)
main_directory = "/Users/vedantaryan/Desktop/NewSt copy/Output/SOUND"
# Regular expression to find image URLs inside <figure><img src="...">
image_pattern = re.compile(r'(<img src=")(https?://.*?)(?=")')
# Global counter for image numbering
image_counter = 1
# Function to process an .mmd file, download images, and update file
def extract_download_replace_images(mmd_file_path):
    global image_counter  # Use the global counter for unique numbering
    parent_folder = os.path.dirname(mmd_file_path)  # Get the folder where .mmd file exists
    with open(mmd_file_path, "r", encoding="utf-8") as file:
        content = file.read()
    # Find all image matches (src="image_url")
    image_matches = image_pattern.findall(content)
    if not image_matches:  # If no images found, don't create the images folder
        return
    images_folder = os.path.join(parent_folder, "images")  # "images" folder inside the same directory
    os.makedirs(images_folder, exist_ok=True)  # Create folder if images exist
    for match in image_matches:
        full_match, image_url = match  # Extract URL from regex match
        new_image_name = f"Figure{image_counter:02d}.png"  # Naming format: Figure01.png, Figure02.png
        new_image_path = os.path.join(images_folder, new_image_name)
        try:
            # Download and save the image
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(new_image_path, "wb") as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                print(f":white_tick: Downloaded: {new_image_path}")
                # Replace the image URL inside the .mmd file with placeholder <Figure01>
                placeholder = f"<{new_image_name[:-4]}>"  # Remove .png from filename
                content = content.replace(image_url, placeholder)
                # Increment global image counter
                image_counter += 1
            else:
                print(f":warning: Failed to download: {image_url} (Status Code: {response.status_code})")
        except Exception as e:
            print(f":x: Error downloading {image_url}: {e}")
    # Save the modified .mmd file with updated image placeholders
    with open(mmd_file_path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f":pencil2: Updated {mmd_file_path} with new image placeholders!")
# Get all folders inside the main directory (sorted in ascending order)
subfolders = sorted(
    [os.path.join(main_directory, d) for d in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, d))]
)
# Process each folder in ascending order
for subfolder in subfolders:
    for root, dirs, files in sorted(os.walk(subfolder)):  # Ensures subfolders are also processed in order
        files.sort()  # Ensure files inside folders are processed in order
        for file in files:
            if file.endswith(".mmd"):
                mmd_file_path = os.path.join(root, file)
                extract_download_replace_images(mmd_file_path)
print(":tada: Image extraction, downloading, and replacement completed!")
