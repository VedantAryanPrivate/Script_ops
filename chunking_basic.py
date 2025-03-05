import os
import re
import zipfile
# Read the content of the uploaded MMD file
input_file_path = '/Users/vedantaryan/Desktop/MERGED_8_BIO_THEORY_MMD more/linkedited/Heredity and Evolution F- JEE- NEET Theory.mmd'  # Update the file path
output_parent_folder = '/Users/vedantaryan/Desktop/MERGED_8_BIO_THEORY_MMD more/output/CLASS8_BIO_CHAP6'  # Set the parent folder for chunked files
# Read the content of the .mmd file
with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()
# Split the content into chunks based on <start> tags
chunks = content.split('<start>')
# Create the parent folder if it doesn't exist
os.makedirs(output_parent_folder, exist_ok=True)
# Save each chunk as a separate file in its own folder
for idx, chunk in enumerate(chunks[1:], start=1):  # Start from 1 to skip the first empty chunk
    # Create a folder for each chunk based on the index (e.g., 7.1, 7.2, etc.)
    chunk_folder = os.path.join(output_parent_folder, f"6.{idx}")
    os.makedirs(chunk_folder, exist_ok=True)
    # Define the file path for the chunk
    chunk_file_path = os.path.join(chunk_folder, f"Heredity and Evolution F- JEE- NEET Theory_6.{idx}.mmd")
    # Write the chunk to the file
    with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
        chunk_file.write('<start>' + chunk)  # Add <start> back to the chunk
# Now, zip all chunked files into one file
output_zip_path = '/Users/vedantaryan/Desktop/MERGED_8_BIO_THEORY_MMD more/output/CLASS8_BIO_CHAP6/Heredity and Evolution F- JEE- NEET Theory_6_chunks.zip'  # Set the desired zip output path
with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Iterate over all the folders and add files to the zip
    for idx, chunk in enumerate(chunks[1:], start=1):
        chunk_folder = os.path.join(output_parent_folder, f"6.{idx}")
        chunk_filename = f"Heredity and Evolution F- JEE- NEET Theory_6.{idx}.mmd"
        chunk_file_path = os.path.join(chunk_folder, chunk_filename)
        # Add the chunk file to the zip archive
        zipf.write(chunk_file_path, arcname=f"6.{idx}/{chunk_filename}")
print(f"All chunked files have been saved in their respective folders and zipped at {output_zip_path}")
