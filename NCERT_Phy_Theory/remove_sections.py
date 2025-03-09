import os
import re
def process_mmd_file(input_path, output_path):
    """Process .mmd file: Remove \section*{}, \subsection*{} but keep text,
       and keep \subsection*{} only for 'X.Y Title' format, even for multi-line content."""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()  # Read entire file as a single string
    # Handle multi-line \section*{} and \subsection*{}
    content = re.sub(r'\\section\*\{([\s\S]*?)\}', r'\1', content)
    content = re.sub(r'\\subsection\*\{([\s\S]*?)\}', r'\1', content)
    # Convert lines back to list for further processing
    lines = content.split("\n")
    updated_content = []
    for line in lines:
        stripped_line = line.strip()
        # Keep \subsection*{} if it starts with 'X.Y Something'
        if re.match(r'^\d+\.\d+\s+.+', stripped_line):
            stripped_line = f"\\subsection*{{{stripped_line}}}"
        updated_content.append(stripped_line)
    # Save the modified file to the output directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(updated_content))
    print(f":white_tick: Processed: {input_path} → {output_path}")
def process_directory(input_folder, output_folder):
    """Process all '.mmd' files inside the input directory and save to output directory."""
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".mmd"):
                input_path = os.path.join(root, file)
                # Create corresponding output path
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)
                process_mmd_file(input_path, output_path)
# :small_blue_diamond: Set your input and output folder paths here
input_folder = "/Users/vedantaryan/Desktop/NewSt/input_dir"
output_folder = "/Users/vedantaryan/Desktop/NewSt/output_dir"
process_directory(input_folder, output_folder)
