import os
import sys
import langdetect

def detect_language(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            if not text.strip():
                return "[UNKNOWN] Empty or unreadable file"
            lang = langdetect.detect(text)
            return lang
    except Exception as e:
        return f"[ERROR] {e}"

def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else input("Enter the folder path: ")
    if not os.path.isdir(folder):
        print(f"'{folder}' is not a valid path.")
        return
    
    print("\n[LANGUAGE DETECTION RESULTS]")
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.srt', '.ass', '.sub')):
            file_path = os.path.join(folder, filename)
            lang = detect_language(file_path)
            print(f"{filename}: {lang}")

if __name__ == "__main__":
    main()
