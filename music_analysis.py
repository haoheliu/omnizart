#!/usr/bin/env python3
"""
Simple Omnizart music analysis script
Performs three transcription tasks on the given audio file:
1. Musical notes of pitched instruments
2. Frame-level vocal melody (F0)
3. Chord progressions
"""

import os
import sys
from pathlib import Path

# Import Omnizart modules
from omnizart.music import app as music_app
from omnizart.vocal_contour import app as vocal_app
from omnizart.chord import app as chord_app

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
    
    # 1. Transcribe musical notes of pitched instruments
    print("1. Transcribing musical notes...")
    try:
        music_output = output_dir / "music_notes.mid"
        music_app.transcribe(audio_path, output=str(music_output))
        print(f"   ✓ Music notes saved to: {music_output}")
    except Exception as e:
        print(f"   ✗ Error transcribing music notes: {e}")
    
    # 2. Transcribe frame-level vocal melody (F0)
    print("2. Transcribing vocal melody...")
    try:
        vocal_output = output_dir / "vocal_melody.mid"
        vocal_app.transcribe(audio_path, output=str(vocal_output))
        print(f"   ✓ Vocal melody saved to: {vocal_output}")
    except Exception as e:
        print(f"   ✗ Error transcribing vocal melody: {e}")
    
    # 3. Transcribe chord progressions
    print("3. Transcribing chord progressions...")
    try:
        chord_output = output_dir / "chord_progressions.mid"
        chord_app.transcribe(audio_path, output=str(chord_output))
        print(f"   ✓ Chord progressions saved to: {chord_output}")
    except Exception as e:
        print(f"   ✗ Error transcribing chord progressions: {e}")
    
    print("=" * 50)
    print("Analysis complete! Check the 'analysis_results' folder for output files.")

if __name__ == "__main__":
    # Audio file path
    audio_file = "/home/lxb/Disk_SSD/haoheliu_2023_dec/all-in-one/mixture_128.mp3"
    
    # Run analysis
    analyze_music(audio_file) 