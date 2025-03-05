import os
import re

def extract_chapter_number(file_name):
    match = re.search(r'Ch_(\d+)', file_name, re.IGNORECASE)
    return str(int(match.group(1))) if match else "1"  # Convert to int to remove leading zeros

def extract_chapter_name(file_name):
    # Remove prefix like 'Ch_01_' and file extension
    name = re.sub(r'Ch_\d+_', '', os.path.splitext(file_name)[0], flags=re.IGNORECASE)
    return name.strip()

def chunk_mmd(file_path, output_base_dir):
    # Extract chapter number and name from file name
    file_name = os.path.basename(file_path)
    chapter_number = extract_chapter_number(file_name)
    chapter_name = extract_chapter_name(file_name)
    
    # Define output directory based on extracted chapter name
    output_dir = os.path.join(output_base_dir, chapter_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the .mmd file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Adjust regex to handle multi-line subsection titles
    pattern = re.split(r'\\subsection\*\{\s*([\s\S]*?)\s*\}', content)

    if len(pattern) < 2:
        print("No subsections found.")
        return
    
    # Iterate over chunks (pattern[0] is pre-subsection text, discard it if empty)
    section_count = 0
    for i in range(1, len(pattern), 2):
        section_title = " ".join(pattern[i].split())  # Normalize multi-line titles into one line
        section_content = pattern[i + 1].strip()

        if not section_content:
            print(f"Skipping empty subsection: {section_title}")
            continue  # Skip empty sections
        
        # Create folder with extracted chapter number
        section_folder = os.path.join(output_dir, f"{chapter_number}.{section_count}")
        os.makedirs(section_folder, exist_ok=True)
        
        # Ensure safe file naming
        safe_section_title = section_title.replace(" ", " ").replace("/", "-")
        file_name = f"{safe_section_title}.mmd"
        file_path = os.path.join(section_folder, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as out_file:
            out_file.write(f"<start>{section_title}\n\n")  # Add <start> tag before title
            out_file.write(section_content)
        
        print(f"Saved: {file_path}")
        section_count += 1

# Example usage
input_mmd = "/Users/vedantaryan/Desktop/NewSt copy/pdf_uploads/Ch_13_LIGHT/Ch_13_LIGHT.mmd"
output_base_directory = "/Users/vedantaryan/Desktop/NewSt copy/Output"
chunk_mmd(input_mmd, output_base_directory)
