import os
import sys
import langdetect

def detect_language(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            if not text.strip():
                return "unknown"
            lang = langdetect.detect(text)
            return lang
    except Exception as e:
        return "error"

def rename_files(folder):
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.srt', '.ass', '.sub')):
            file_path = os.path.join(folder, filename)
            lang = detect_language(file_path)
            
            if lang == "error" or lang == "unknown":
                print(f"[SKIPPED] {filename} (Language detection failed)")
                continue
            
            base_name, ext = os.path.splitext(filename)
            
            # Check if there's a track number
            if "_track" in base_name:
                new_filename = base_name.rsplit("_track", 1)[0] + f"_{lang}" + ext
            else:
                new_filename = base_name + f"_{lang}" + ext
            
            new_filepath = os.path.join(folder, new_filename)
            os.rename(file_path, new_filepath)
            print(f"[RENAMED] {filename} -> {new_filename}")

def process_headers(folder):
    # Get list of files with specified extensions
    files = [filename for filename in os.listdir(folder) if filename.lower().endswith(('.srt', '.ass', '.sub'))]
    if not files:
        print("No files found with the specified extensions.")
        return

    # Open the first file to display its header
    first_file = files[0]
    first_path = os.path.join(folder, first_file)
    try:
        with open(first_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file {first_file}: {e}")
        return

    header = lines[:8]
    print(f"Header of the first file ({first_file}):")
    for line in header:
        print(line, end="")
    print("\n" + "-"*40 + "\n")

    # Ask if user wants to remove a text string from headers
    response = input("Do you want to remove a text string from the headers of all files? (y/n): ")
    if response.lower() == 'y':
        unwanted = input("Enter the text string you want to remove: ")
        # Process all files, including the first one
        for filename in files:
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
                continue

            # Replace the string in the first 6 lines
            new_header = [line.replace(unwanted, "") for line in lines[:6]]
            lines[:8] = new_header
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"Removed '{unwanted}' from the header of {filename}.")
            except Exception as e:
                print(f"Error writing to file {filename}: {e}")

    # Show updated headers of all files
    print("\nUpdated headers of all files:\n")
    for filename in files:
        file_path = os.path.join(folder, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            continue
        header = lines[:6]
        print(f"Header of {filename}:")
        for line in header:
            print(line, end="")
        print("\n" + "-"*40 + "\n")

def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else input("Enter the folder path: ")
    if not os.path.isdir(folder):
        print(f"'{folder}' is not a valid path.")
        return
    
    rename_files(folder)
    process_headers(folder)

if __name__ == "__main__":
    main()