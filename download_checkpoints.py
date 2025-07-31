#!/usr/bin/env python3
"""
Download Omnizart checkpoint files
Downloads the missing model weight files needed for transcription
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

def download_checkpoints():
    """Download the archived checkpoints of different models."""
    from omnizart.remote import download_large_file_from_google_drive
    from omnizart import MODULE_PATH
    
    release_url = "https://github.com/Music-and-Culture-Technology-Lab/omnizart/releases/download/checkpoints-20211001"
    CHECKPOINTS = {
        "chord_v1": {
            "fid": f"{release_url}/chord_v1@variables.data-00000-of-00001",
            "save_as": "checkpoints/chord/chord_v1/variables/variables.data-00000-of-00001"
        },
        "music_piano": {
            "fid": f"{release_url}/music_piano@variables.data-00000-of-00001",
            "save_as": "checkpoints/music/music_piano/variables/variables.data-00000-of-00001",
        },
        "vocal_contour": {
            "fid": f"{release_url}/contour@variables.data-00000-of-00001",
            "save_as": "checkpoints/vocal/vocal_contour/variables/variables.data-00000-of-00001",
        }
    }

    output_path = MODULE_PATH
    print(f"Downloading checkpoints to: {output_path}")

    for checkpoint, info in CHECKPOINTS.items():
        print(f"\nDownloading checkpoint: {checkpoint}")
        save_name = os.path.basename(info["save_as"])
        save_path = os.path.dirname(info["save_as"])
        save_path = os.path.join(output_path, save_path)
        
        # Create directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        try:
            download_large_file_from_google_drive(
                info["fid"],
                file_length=info.get("file_length", None),
                save_path=save_path,
                save_name=save_name,
                unzip=False
            )
            print(f"✓ Successfully downloaded {checkpoint}")
        except Exception as e:
            print(f"✗ Failed to download {checkpoint}: {e}")

if __name__ == "__main__":
    download_checkpoints() 