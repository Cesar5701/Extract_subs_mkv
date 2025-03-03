# Subtitle Extractor

This script extracts subtitle tracks from MKV files in a specified folder. It uses `mkvmerge` to identify subtitle tracks and `mkvextract` to extract them.

## Requirements

- Python 3.x
- `mkvmerge` and `mkvextract` from the MKVToolNix package

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/).
2. Install MKVToolNix from [mkvtoolnix.download](https://mkvtoolnix.download/).

## Usage

1. Place the `subs.py` script in a folder.
2. Open a terminal or command prompt.
3. Navigate to the folder containing the `subs.py` script.
4. Run the script with the folder path containing the MKV files as an argument:

    ```sh
    python subs.py /path/to/mkv/files
    ```

    Alternatively, you can run the script without arguments and it will prompt you to enter the folder path:

    ```sh
    python subs.py
    ```

## How It Works

1. The script scans the specified folder for MKV files.
2. It uses `mkvmerge` to identify subtitle tracks in each MKV file.
3. If all MKV files have the same subtitle tracks, it allows you to select the tracks to extract once and applies the selection to all files.
4. If the MKV files have different subtitle tracks, it prompts you to select the tracks for each file individually.
5. The selected subtitle tracks are extracted using `mkvextract` and saved in a subfolder named `extracted_subtitles`.

## Functions

### [select_subtitles(subtitle_tracks)](http://_vscodecontentref_/1)

Prompts the user to select which subtitle tracks to extract.

### [extract_subtitles(file_path)](http://_vscodecontentref_/2)

Identifies and extracts subtitle tracks from an MKV file.

### [main()](http://_vscodecontentref_/3)

Main function that processes all MKV files in the specified folder.

## Example

```sh
python subs.py C:/user/user_name/Videos/