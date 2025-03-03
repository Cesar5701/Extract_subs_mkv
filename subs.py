import os
import re
import subprocess
import sys

def select_subtitles(subtitle_tracks):
    """
    Allows the user to select which subtitle tracks to extract.
    """
    print("\nAvailable subtitle tracks:")
    for i, (track_id, ext) in enumerate(subtitle_tracks):
        print(f"{i + 1}: Track ID {track_id} ({ext})")

    print("\nEnter the numbers of the subtitle tracks you want to extract, separated by commas.")
    print("Enter 'all' to extract all subtitle tracks.")
    selection = input("Your choice: ")

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

def extract_subtitles(file_path, output_dir):
    """
    Extracts subtitle tracks from an MKV file.
    """
    # Get track information from the file using mkvmerge.
    cmd = ['mkvmerge', '--ui-language', 'en', '-i', file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check if the command executed successfully
    if result.returncode != 0:
        print(f"[ERROR] The mkvmerge command failed with exit code {result.returncode}")
        print(f"[ERROR] Error message: {result.stderr}")
        return

    output = result.stdout
    print(f"[DEBUG] mkvmerge output:\n{output}")

    subtitle_tracks = []
    # Pattern to identify subtitle tracks in the output.
    # Example line: "Track ID 2: subtitles (S_TEXT/ASS)"
    pattern = re.compile(r"Track ID (\d+): subtitles \(([^)]+)\)")
    for line in output.splitlines():
        match = pattern.search(line)
        if match:
            track_id = match.group(1)
            track_format = match.group(2)
            # Determine the output extension based on the format
            if "SRT" in track_format.upper():
                ext = ".srt"
            elif "ASS" in track_format.upper() or "SUBSTATIONALPHA" in track_format.upper():
                ext = ".ass"
            else:
                ext = ".sub"
            
            subtitle_tracks.append((track_id, ext))
    
    if not subtitle_tracks:
        print(f"[INFO] No subtitle tracks found in: {file_path}")
        return

    # Allow the user to select which subtitle tracks to extract.
    selected_tracks = select_subtitles(subtitle_tracks)
    if not selected_tracks:
        print("[INFO] No subtitle tracks selected.")
        return

    # Build the command to extract all selected subtitle tracks.
    # An output file will be created for each track, named based on the original file.
    cmd_extract = ['mkvextract', 'tracks', file_path]
    for track_id, ext in selected_tracks:
        base = os.path.splitext(os.path.basename(file_path))[0]
        output_filename = os.path.join(output_dir, f"{base}_track{track_id}{ext}")
        cmd_extract.append(f"{track_id}:{output_filename}")

    print("Executing:", " ".join(cmd_extract))
    subprocess.run(cmd_extract)

def main():
    # Get the folder path from arguments or input
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = input("Enter the folder path: ")

    if not os.path.isdir(folder):
        print(f"'{folder}' is not a valid path.")
        return

    # Create a new directory for the extracted subtitles
    output_dir = os.path.join(folder, "extracted_subtitles")
    os.makedirs(output_dir, exist_ok=True)

    # Process each MKV file in the specified folder
    for filename in os.listdir(folder):
        if filename.lower().endswith(".mkv"):
            file_path = os.path.join(folder, filename)
            print(f"\n[PROCESSING] {file_path}")
            extract_subtitles(file_path, output_dir)

if __name__ == "__main__":
    main()
