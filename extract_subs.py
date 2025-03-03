import os
import re
import subprocess
import sys

def select_subtitles(subtitle_tracks):
    print("\nAvailable subtitle tracks:")
    for i, (track_id, ext) in enumerate(subtitle_tracks):
        print(f"{i + 1}: Track ID {track_id} ({ext})")

    selection = input("Enter the numbers of the subtitle tracks you want to extract, separated by commas, or 'all': ")
    if selection.lower() == 'all':
        return subtitle_tracks
    
    selected_tracks = []
    try:
        indices = [int(x) - 1 for x in selection.split(',')]
        for index in indices:
            if 0 <= index < len(subtitle_tracks):
                selected_tracks.append(subtitle_tracks[index])
    except ValueError:
        print("[ERROR] Invalid selection. No subtitles will be extracted.")
    
    return selected_tracks

def extract_subtitles(file_path):
    cmd = ['mkvmerge', '--ui-language', 'en', '-i', file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] mkvmerge failed: {result.stderr}")
        return []
    
    subtitle_tracks = []
    pattern = re.compile(r"Track ID (\d+): subtitles \(([^)]+)\)")
    for line in result.stdout.splitlines():
        match = pattern.search(line)
        if match:
            track_id, track_format = match.groups()
            ext = ".srt" if "SRT" in track_format.upper() else ".ass" if "ASS" in track_format.upper() or "SUBSTATIONALPHA" in track_format.upper() else ".sub"
            subtitle_tracks.append((track_id, ext))
    
    return subtitle_tracks

def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else input("Enter the folder path: ")
    if not os.path.isdir(folder):
        print(f"'{folder}' is not a valid path.")
        return

    output_dir = os.path.join(folder, "extracted_subtitles")
    os.makedirs(output_dir, exist_ok=True)

    first_structure = None
    selected_tracks = None

    for filename in os.listdir(folder):
        if not filename.lower().endswith(".mkv"):
            continue
        
        file_path = os.path.join(folder, filename)
        print(f"\n[PROCESSING] {file_path}")
        
        subtitle_tracks = extract_subtitles(file_path)
        if not subtitle_tracks:
            print(f"[INFO] No subtitles found in {filename}.")
            continue
        
        current_structure = {ext for _, ext in subtitle_tracks}
        
        if first_structure is None:
            first_structure = current_structure
            selected_tracks = select_subtitles(subtitle_tracks)
        elif first_structure != current_structure:
            print("[INFO] Subtitle structure differs, selecting tracks manually.")
            selected_tracks = select_subtitles(subtitle_tracks)
        
        if not selected_tracks:
            print("[INFO] No subtitle tracks selected.")
            continue
        
        cmd_extract = ['mkvextract', 'tracks', file_path]
        for track_id, ext in selected_tracks:
            base = os.path.splitext(os.path.basename(file_path))[0]
            output_filename = os.path.join(output_dir, f"{base}_track{track_id}{ext}")
            cmd_extract.append(f"{track_id}:{output_filename}")
        
        print("Executing:", " ".join(cmd_extract))
        subprocess.run(cmd_extract)

if __name__ == "__main__":
    main()
