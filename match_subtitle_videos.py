import os
import sys
import re

def find_video_files(video_folder):
    video_files = {}
    for filename in os.listdir(video_folder):
        if filename.lower().endswith(".mkv"):
            match = re.match(r"(S\d{2}E\d{2}) - (.+)\.mkv", filename, re.IGNORECASE)
            if match:
                key = match.group(1)  # Extract SxxExx as key
                video_files[key] = os.path.join(video_folder, filename)
    return video_files

def find_subtitle_files(subtitle_folder):
    subtitle_files = {}
    for filename in os.listdir(subtitle_folder):
        if filename.lower().endswith(".ass"):
            match = re.match(r"(S\d{2}E\d{2}) - (.+)_(\w{2})\.ass", filename, re.IGNORECASE)
            if match:
                key = match.group(1)  # Extract SxxExx as key
                language = match.group(3)  # Extract language
                if key not in subtitle_files:
                    subtitle_files[key] = []
                subtitle_files[key].append(os.path.join(subtitle_folder, filename))
    return subtitle_files

def match_subtitles_to_videos(video_folder, subtitle_folder):
    video_files = find_video_files(video_folder)
    subtitle_files = find_subtitle_files(subtitle_folder)
    
    matches = {}
    for key, video_path in video_files.items():
        if key in subtitle_files:
            matches[video_path] = subtitle_files[key]
    
    return matches

def main():
    if len(sys.argv) < 3:
        print("Usage: python match_subtitles.py <video_folder> <subtitle_folder>")
        return
    
    video_folder = sys.argv[1]
    subtitle_folder = sys.argv[2]
    
    if not os.path.isdir(video_folder) or not os.path.isdir(subtitle_folder):
        print("Invalid folder paths.")
        return
    
    matches = match_subtitles_to_videos(video_folder, subtitle_folder)
    
    for video, subs in matches.items():
        print(f"Video: {video}")
        for sub in subs:
            print(f"  -> Subtitle: {sub}")

tif __name__ == "__main__":
    main()
