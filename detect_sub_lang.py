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
            
            # Detect if there's a track number
            if "_track" in base_name:
                new_filename = base_name.rsplit("_track", 1)[0] + f"_{lang}" + ext
            else:
                new_filename = base_name + f"_{lang}" + ext
            
            new_filepath = os.path.join(folder, new_filename)
            os.rename(file_path, new_filepath)
            print(f"[RENAMED] {filename} -> {new_filename}")

def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else input("Enter the folder path: ")
    if not os.path.isdir(folder):
        print(f"'{folder}' is not a valid path.")
        return
    
    rename_files(folder)

if __name__ == "__main__":
    main()
