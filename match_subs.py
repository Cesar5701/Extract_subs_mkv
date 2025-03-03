import os
import re
import sys
import subprocess
import shutil
from pathlib import Path

def multiplex_subtitles(video_dir, subs_dir):
    video_pattern = re.compile(r'(S\d{2}E\d{2})', re.IGNORECASE)
    sub_pattern = re.compile(r'(S\d{2}E\d{2}).*?(?:\((\w+)\))?\.ass$', re.IGNORECASE)

    for video_file in os.listdir(video_dir):
        if not video_file.lower().endswith('.mkv'):
            continue
            
        # Extract SxxExx code
        video_match = video_pattern.search(video_file)
        if not video_match:
            continue
            
        code = video_match.group(1).upper()
        video_path = os.path.join(video_dir, video_file)
        matched_subs = []

        # Find matching subtitles
        for sub_file in Path(subs_dir).glob('*.ass'):
            sub_match = sub_pattern.search(sub_file.name)
            if not sub_match:
                continue
                
            if sub_match.group(1).upper() == code:
                lang = sub_match.group(2) or 'und'
                matched_subs.append((str(sub_file.resolve()), lang))

        if not matched_subs:
            continue
            
        # Build mkvmerge command
        temp_output = f"{video_path}.tmp"
        command = [
            'mkvmerge',
            '-o', temp_output,
            video_path
        ]

        # Add subtitles
        for sub, lang in matched_subs:
            command.extend(['--language', f'0:{lang}', sub])

        # Execute and replace if successful
        try:
            print(f"\nProcessing: {video_file}")
            print(f"Adding {len(matched_subs)} subtitle(s)")
            
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            
            os.replace(temp_output, video_path)
            print("✓ Multiplexing completed")
            
        except subprocess.CalledProcessError as e:
            print(f"Error in mkvmerge: {e.stderr}")
            if os.path.exists(temp_output):
                os.remove(temp_output)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} [video_directory] [subtitle_directory]")
        sys.exit(1)

    video_dir = sys.argv[1]
    subs_dir = sys.argv[2]

    # Check for mkvmerge
    if not shutil.which('mkvmerge'):
        print("Error: You need to install MKVToolNix (mkvmerge not found)")
        sys.exit(1)

    if not os.path.isdir(video_dir):
        print(f"Error: Video directory not found: {video_dir}")
        sys.exit(1)

    if not os.path.isdir(subs_dir):
        print(f"Error: Subtitle directory not found: {subs_dir}")
        sys.exit(1)

    multiplex_subtitles(video_dir, subs_dir)