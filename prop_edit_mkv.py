import subprocess
import glob
import os
import argparse

def process_mkv_files(directory):
    """Process MKV files in a directory to modify specific track properties."""
    
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist")
        return

    mkv_files = glob.glob(os.path.join(directory, '*.mkv'))
    
    if not mkv_files:
        print(f"No MKV files found in {directory}")
        return

    for file_path in mkv_files:
        try:
            subprocess.run([
                'mkvpropedit',
                file_path,
                # Modify subtitle track 1
                '--edit', 'track:s1',
                '--set', 'name=English',
                '--set', 'language=en',
                '--set', 'flag-default=0',
                
                # Modify subtitle track 2
                '--edit', 'track:s2',
                '--set', 'name=Spanish(Latin_America)',
                '--set', 'language=es',
                '--set', 'flag-default=1',
                
                # Modify audio track 1
                '--edit', 'track:a1',
                '--set', 'name=AAC 2.0',
                '--set', 'language=jpn',
                '--set', 'flag-default=1'
            ], check=True)
            
            print(f"✓ Processed: {os.path.basename(file_path)}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error in {os.path.basename(file_path)}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Modify MKV track properties in batch',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('--dir', 
                        type=str, 
                        default='.', 
                        help='''Directory containing MKV files
Examples:
  python script.py --dir "D:\\my_videos"
  python script.py (uses current directory)''')
    
    args = parser.parse_args()
    
    print(f"\nProcessing files in: {os.path.abspath(args.dir)}\n")
    process_mkv_files(args.dir)
    print("\n✅ Process completed. Verify with:")
    print("   mkvmerge -i file.mkv | findstr /i 'track name language default'")
    print("   mkvinfo file.mkv | grep -E 'Track|Name|Language|Default'")