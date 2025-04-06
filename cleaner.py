import os
import glob

def delete_mp3_files():
    mp3_files = glob.glob("*.mp3")
    for mp3_file in mp3_files:
        try:
            os.remove(mp3_file)
            print(f"Deleted: {mp3_file}")
        except OSError as e:
            print(f"Error deleting {mp3_file}: {e}")

if __name__ == "__main__":
    delete_mp3_files()