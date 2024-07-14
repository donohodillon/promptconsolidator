import os

# List of file extensions we want to include
TEXT_EXTENSIONS = [
    '.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml',
    '.yml', '.yaml', '.ini', '.cfg', '.conf', '.sh', '.bat',
    '.c', '.cpp', '.h', '.hpp', '.java', '.rb', '.pl', '.php', '.mjs'
]

def is_text_file(filename):
    """Check if a file is a text file based on its extension."""
    return any(filename.lower().endswith(ext) for ext in TEXT_EXTENSIONS)

def should_include_file(filepath):
    """Determine if a file should be included based on various criteria."""
    filename = os.path.basename(filepath)
    
    # Exclude git-related files and directories
    if '.git' in filepath.split(os.sep):
        return False
    if filename.startswith('.git'):
        return False
    
    # Include only text files
    return is_text_file(filename)

def combine_files(directory, outfile, indent=""):
    # Iterate through all items in the directory
    for item in os.listdir(directory):
        # Get the full path
        item_path = os.path.join(directory, item)
        
        # If it's a directory, recurse into it (except .git directories)
        if os.path.isdir(item_path) and item != '.git':
            outfile.write(f"\n\n{'='*50}\n")
            outfile.write(f"Directory: {item_path}\n")
            outfile.write(f"{'='*50}\n\n")
            combine_files(item_path, outfile, indent + "  ")
        
        # If it's a file, check if we should include it
        elif os.path.isfile(item_path) and should_include_file(item_path):
            # Skip the script itself and the output file
            if item == os.path.basename(__file__) or item == 'combined_files.txt':
                continue
            
            try:
                # Write the file name as a header
                outfile.write(f"\n\n{'='*50}\n")
                outfile.write(f"File: {item_path}\n")
                outfile.write(f"{'='*50}\n\n")
                
                # Read and write the contents of the file
                with open(item_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            except Exception as e:
                outfile.write(f"Error reading file {item_path}: {str(e)}\n")

def main():
    # Get the current directory
    current_dir = os.getcwd()
    
    # Name of the output file
    output_filename = 'combined_files.txt'
    
    # Open the output file in write mode (this will overwrite the file if it exists)
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        combine_files(current_dir, outfile)

    print(f"All text files have been combined into '{output_filename}'")

if __name__ == "__main__":
    main()