#!/usr/bin/env python3
"""
Omnizart music analysis using pre-separated Demucs stems (Fixed Version)
Performs three transcription tasks on separated audio stems:
1. Musical notes of pitched instruments (from 'other' stem)
2. Frame-level vocal melody (F0) (from 'vocals' stem)
3. Chord progressions (from 'vocals' stem)
"""

import os
import sys
import traceback
import tempfile
from pathlib import Path
from typing import Dict, Optional

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

def analyze_demucs_stems(stems_dict: Dict[str, str], output_dir: str = "analysis_results"):
    """
    Analyze pre-separated Demucs stems for music transcription.
    
    Parameters:
    -----------
    stems_dict : Dict[str, str]
        Dictionary containing paths to separated stems:
        - 'vocals': Path to vocals stem
        - 'drum': Path to drums stem  
        - 'bass': Path to bass stem
        - 'other': Path to other instruments stem
    output_dir : str
        Directory to save analysis results
    """
    
    # Validate stems dictionary
    required_stems = ['vocals', 'drum', 'bass', 'other']
    missing_stems = [stem for stem in required_stems if stem not in stems_dict]
    if missing_stems:
        print(f"Error: Missing required stems: {missing_stems}")
        print(f"Available stems: {list(stems_dict.keys())}")
        return
    
    # Check if all stem files exist
    for stem_name, stem_path in stems_dict.items():
        if not os.path.exists(stem_path):
            print(f"Error: Stem file not found: {stem_path}")
            return
    
    print("🎵 Analyzing Demucs separated stems...")
    print("=" * 50)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    try:
        # Import Omnizart modules
        print("Importing Omnizart modules...")
        from omnizart.music import app as music_app
        from omnizart.vocal_contour import app as vocal_app
        from omnizart.chord import app as chord_app
        print("✓ Modules imported successfully")
        
        # 1. Transcribe musical notes from 'other' stem (pitched instruments)
        print("\n1. Transcribing musical notes from 'other' stem...")
        try:
            music_output = output_path / "music_notes_other.mid"
            print(f"   Input: {stems_dict['other']}")
            print(f"   Output: {music_output}")
            music_app.transcribe(stems_dict['other'], output=str(music_output))
            if music_output.exists():
                print(f"   ✓ Music notes saved to: {music_output}")
                print(f"   File size: {music_output.stat().st_size} bytes")
            else:
                print(f"   ✗ Music notes file not created")
        except Exception as e:
            print(f"   ✗ Error transcribing music notes: {e}")
            traceback.print_exc()
        
        # 2. Transcribe frame-level vocal melody (F0) from 'vocals' stem
        print("\n2. Transcribing vocal melody from 'vocals' stem...")
        try:
            vocal_output = output_path / "vocal_melody_vocals.mid"
            print(f"   Input: {stems_dict['vocals']}")
            print(f"   Output: {vocal_output}")
            vocal_app.transcribe(stems_dict['vocals'], output=str(vocal_output))
            if vocal_output.exists():
                print(f"   ✓ Vocal melody saved to: {vocal_output}")
                print(f"   File size: {vocal_output.stat().st_size} bytes")
            else:
                print(f"   ✗ Vocal melody file not created")
        except Exception as e:
            print(f"   ✗ Error transcribing vocal melody: {e}")
            traceback.print_exc()
        
        # 3. Transcribe chord progressions from 'vocals' stem
        print("\n3. Transcribing chord progressions from 'vocals' stem...")
        try:
            chord_output = output_path / "chord_progressions_vocals.mid"
            print(f"   Input: {stems_dict['vocals']}")
            print(f"   Output: {chord_output}")
            chord_app.transcribe(stems_dict['vocals'], output=str(chord_output))
            if chord_output.exists():
                print(f"   ✓ Chord progressions saved to: {chord_output}")
                print(f"   File size: {chord_output.stat().st_size} bytes")
            else:
                print(f"   ✗ Chord progressions file not created")
        except Exception as e:
            print(f"   ✗ Error transcribing chord progressions: {e}")
            traceback.print_exc()
        
        # 4. Optional: Transcribe bass line from 'bass' stem
        print("\n4. Transcribing bass line from 'bass' stem...")
        try:
            bass_output = output_path / "bass_line.mid"
            print(f"   Input: {stems_dict['bass']}")
            print(f"   Output: {bass_output}")
            music_app.transcribe(stems_dict['bass'], output=str(bass_output))
            if bass_output.exists():
                print(f"   ✓ Bass line saved to: {bass_output}")
                print(f"   File size: {bass_output.stat().st_size} bytes")
            else:
                print(f"   ✗ Bass line file not created")
        except Exception as e:
            print(f"   ✗ Error transcribing bass line: {e}")
            traceback.print_exc()
        
    except ImportError as e:
        print(f"✗ Error importing Omnizart modules: {e}")
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("Analysis complete! Check the 'analysis_results' folder for output files.")
    
    # List all created files
    print("\nCreated files:")
    for file_path in output_path.glob("*.mid"):
        if file_path.exists():
            print(f"  - {file_path} ({file_path.stat().st_size} bytes)")
    
    # List CSV files too
    for file_path in output_path.glob("*.csv"):
        if file_path.exists():
            print(f"  - {file_path} ({file_path.stat().st_size} bytes)")

def create_demucs_stems_dict(demucs_output_dir: str) -> Dict[str, str]:
    """
    Create a stems dictionary from Demucs output directory.
    
    Parameters:
    -----------
    demucs_output_dir : str
        Directory containing Demucs output files
        
    Returns:
    --------
    Dict[str, str]
        Dictionary mapping stem names to file paths
    """
    
    stems_dict = {}
    output_path = Path(demucs_output_dir)
    
    if not output_path.exists():
        print(f"Warning: Demucs output directory not found: {demucs_output_dir}")
        return stems_dict
    
    # Look for common Demucs output patterns
    stem_patterns = {
        'vocals': ['vocals.wav', 'vocals.mp3', '*vocals*'],
        'drum': ['drums.wav', 'drums.mp3', 'drum.wav', 'drum.mp3', '*drum*'],
        'bass': ['bass.wav', 'bass.mp3', '*bass*'],
        'other': ['other.wav', 'other.mp3', '*other*']
    }
    
    for stem_name, patterns in stem_patterns.items():
        for pattern in patterns:
            # Search recursively in the directory
            files = list(output_path.rglob(pattern))
            if files:
                stems_dict[stem_name] = str(files[0])
                print(f"✓ Found {stem_name}: {files[0]}")
                break
        else:
            print(f"⚠️  Warning: No {stem_name} file found")
    
    return stems_dict

if __name__ == "__main__":
    # Example usage with Demucs stems
    # Replace these paths with your actual Demucs stem files
    stems_dict = {
        'vocals': '/path/to/vocals.wav',
        'drum': '/path/to/drums.wav', 
        'bass': '/path/to/bass.wav',
        'other': '/path/to/other.wav'
    }
    
    # For testing, you can use the original mixture for all stems
    # (this simulates having separated stems)
    mixture_path = "/home/lxb/Disk_SSD/haoheliu_2023_dec/all-in-one/mixture_128.mp3"
    test_stems = {
        'vocals': mixture_path,
        'drum': mixture_path,
        'bass': mixture_path, 
        'other': mixture_path
    }
    
    print("🔧 DEMUCS STEMS ANALYSIS (FIXED VERSION)")
    print("=" * 50)
    print("This script analyzes pre-separated Demucs stems for music transcription.")
    print("Replace the stems_dict with your actual Demucs output files.")
    print()
    
    # Run analysis with test stems (using mixture for all stems)
    analyze_demucs_stems(test_stems)
    
    print("\n💡 To use with real Demucs stems:")
    print("1. Run Demucs to separate your audio into stems")
    print("2. Update the stems_dict with the actual file paths")
    print("3. Run this script again")
    
    print("\n📋 Example Demucs command:")
    print("demucs /path/to/audio.mp3 -o demucs_output") 