import os
import re

# Path to the directory containing the mp3 audio files
DIRECTORY = "/Users/macbook-pro/Downloads/Chapter_book/chapter_book_listening"

def clean_track_filenames(dir_path: str, dry_run: bool = False, pad_digits: int = 3):
    """
    Scans the given directory for mp3 files starting with 'Track <number>'
    and renames them to a clean format like 'Track 001.mp3', 'Track 027.mp3', etc.
    
    :param dir_path: Absolute path to the folder containing mp3 files
    :param dry_run: If True, only prints proposed changes without renaming files
    :param pad_digits: Number of digits for zero-padding (default 3, e.g. Track 001)
    """
    if not os.path.exists(dir_path):
        print(f"Error: Directory '{dir_path}' does not exist.")
        return

    # Regular expression to find 'Track' followed by a number
    pattern = re.compile(r'Track\s*(\d+)', re.IGNORECASE)
    
    files = sorted(os.listdir(dir_path))
    mp3_files = [f for f in files if f.lower().endswith('.mp3')]
    
    print(f"Found {len(mp3_files)} MP3 files in: {dir_path}\n")

    # Pass 1: Count target clean filenames to handle potential duplicates safely
    target_counts = {}
    parsed_files = []
    
    for filename in mp3_files:
        match = pattern.search(filename)
        if match:
            track_num = int(match.group(1))
            base_clean_name = f"Track {track_num:0{pad_digits}d}"
            target_counts[base_clean_name] = target_counts.get(base_clean_name, 0) + 1
            parsed_files.append((filename, base_clean_name))
        else:
            print(f"Skipping (no track number found): {filename}")

    # Pass 2: Perform renaming (with suffix if duplicate track numbers exist)
    seen_counts = {}
    renamed_count = 0

    for original_name, base_clean in parsed_files:
        if target_counts[base_clean] > 1:
            seen_counts[base_clean] = seen_counts.get(base_clean, 0) + 1
            new_name = f"{base_clean}_{seen_counts[base_clean]}.mp3"
        else:
            new_name = f"{base_clean}.mp3"
        
        if original_name != new_name:
            renamed_count += 1
            old_path = os.path.join(dir_path, original_name)
            new_path = os.path.join(dir_path, new_name)
            
            if dry_run:
                print(f"[DRY RUN] Would rename: '{original_name}' -> '{new_name}'")
            else:
                os.rename(old_path, new_path)
                print(f"Renamed: '{original_name}' -> '{new_name}'")

    print(f"\nTotal files processed: {len(parsed_files)}")
    print(f"Files {'that would be ' if dry_run else ''}renamed: {renamed_count}")

if __name__ == "__main__":
    # Set dry_run=False to actually perform the renaming
    clean_track_filenames(DIRECTORY, dry_run=False, pad_digits=3)
