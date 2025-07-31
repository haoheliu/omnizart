#!/usr/bin/env python3
"""
Direct Omnizart music analysis using the API
Performs three transcription tasks on the given audio file:
1. Musical notes of pitched instruments
2. Frame-level vocal melody (F0)
3. Chord progressions
"""

import os
import sys
import traceback
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

def analyze_music(audio_path):
    """Analyze music file with three transcription tasks."""
    
    # Check if audio file exists
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found: {audio_path}")
        return
    
    print(f"Analyzing: {audio_path}")
    print("=" * 50)
    
    # Create output directory
    output_dir = Path("analysis_results")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Import Omnizart modules
        print("Importing Omnizart modules...")
        from omnizart.music import app as music_app
        from omnizart.vocal_contour import app as vocal_app
        from omnizart.chord import app as chord_app
        print("✓ Modules imported successfully")
        
        # 1. Transcribe musical notes of pitched instruments
        print("\n1. Transcribing musical notes...")
        try:
            music_output = output_dir / "music_notes.mid"
            print(f"   Output: {music_output}")
            music_app.transcribe(audio_path, output=str(music_output))
            if music_output.exists():
                print(f"   ✓ Music notes saved to: {music_output}")
                print(f"   File size: {music_output.stat().st_size} bytes")
            else:
                print(f"   ✗ Music notes file not created")
        except Exception as e:
            print(f"   ✗ Error transcribing music notes: {e}")
            traceback.print_exc()
        
        # 2. Transcribe frame-level vocal melody (F0)
        print("\n2. Transcribing vocal melody...")
        try:
            vocal_output = output_dir / "vocal_melody.mid"
            print(f"   Output: {vocal_output}")
            vocal_app.transcribe(audio_path, output=str(vocal_output))
            if vocal_output.exists():
                print(f"   ✓ Vocal melody saved to: {vocal_output}")
                print(f"   File size: {vocal_output.stat().st_size} bytes")
            else:
                print(f"   ✗ Vocal melody file not created")
        except Exception as e:
            print(f"   ✗ Error transcribing vocal melody: {e}")
            traceback.print_exc()
        
        # 3. Transcribe chord progressions
        print("\n3. Transcribing chord progressions...")
        try:
            chord_output = output_dir / "chord_progressions.mid"
            print(f"   Output: {chord_output}")
            chord_app.transcribe(audio_path, output=str(chord_output))
            if chord_output.exists():
                print(f"   ✓ Chord progressions saved to: {chord_output}")
                print(f"   File size: {chord_output.stat().st_size} bytes")
            else:
                print(f"   ✗ Chord progressions file not created")
        except Exception as e:
            print(f"   ✗ Error transcribing chord progressions: {e}")
            traceback.print_exc()
        
    except ImportError as e:
        print(f"✗ Error importing Omnizart modules: {e}")
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("Analysis complete! Check the 'analysis_results' folder for output files.")
    
    # List all created files
    print("\nCreated files:")
    for file_path in output_dir.glob("*.mid"):
        if file_path.exists():
            print(f"  - {file_path} ({file_path.stat().st_size} bytes)")

if __name__ == "__main__":
    # Audio file path
    audio_file = "/home/lxb/Disk_SSD/haoheliu_2023_dec/all-in-one/mixture_128.mp3"
    
    # Run analysis
    analyze_music(audio_file) 