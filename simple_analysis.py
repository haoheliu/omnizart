#!/usr/bin/env python3
"""
Simple Omnizart music analysis using CLI commands
Performs three transcription tasks on the given audio file:
1. Musical notes of pitched instruments
2. Frame-level vocal melody (F0)
3. Chord progressions
"""

import os
import subprocess
import sys
from pathlib import Path

def run_omnizart_command(command_args):
    """Run omnizart CLI command."""
    try:
        result = subprocess.run(
            ["python", "-m", "omnizart.cli.cli"] + command_args,
            capture_output=True,
            text=True,
            cwd="/home/lxb/Disk_SSD/haoheliu_2023_dec/omnizart"
        )
        if result.returncode == 0:
            print(f"   ✓ Success: {result.stdout}")
            return True
        else:
            print(f"   ✗ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ✗ Exception: {e}")
        return False

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
    music_output = output_dir / "music_notes.mid"
    success = run_omnizart_command([
        "music", "transcribe", 
        audio_path, 
        "--output", str(music_output)
    ])
    if success:
        print(f"   ✓ Music notes saved to: {music_output}")
    
    # 2. Transcribe frame-level vocal melody (F0)
    print("2. Transcribing vocal melody...")
    vocal_output = output_dir / "vocal_melody.mid"
    success = run_omnizart_command([
        "vocal-contour", "transcribe", 
        audio_path, 
        "--output", str(vocal_output)
    ])
    if success:
        print(f"   ✓ Vocal melody saved to: {vocal_output}")
    
    # 3. Transcribe chord progressions
    print("3. Transcribing chord progressions...")
    chord_output = output_dir / "chord_progressions.mid"
    success = run_omnizart_command([
        "chord", "transcribe", 
        audio_path, 
        "--output", str(chord_output)
    ])
    if success:
        print(f"   ✓ Chord progressions saved to: {chord_output}")
    
    print("=" * 50)
    print("Analysis complete! Check the 'analysis_results' folder for output files.")

if __name__ == "__main__":
    # Audio file path
    audio_file = "/home/lxb/Disk_SSD/haoheliu_2023_dec/all-in-one/mixture_128.mp3"
    
    # Run analysis
    analyze_music(audio_file) 