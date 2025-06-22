# Sample Sound Files Creation Script
# This script creates placeholder sound files for testing purposes

import numpy as np
import wave
import os
from config.game_config import SOUNDS_DIR

def create_beep_sound(filename, frequency=440, duration=0.2, sample_rate=22050):
    """Create a simple beep sound"""
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate sine wave
    wave_data = np.sin(2 * np.pi * frequency * t)
    
    # Apply fade in/out to prevent clicks
    fade_frames = int(sample_rate * 0.01)  # 10ms fade
    wave_data[:fade_frames] *= np.linspace(0, 1, fade_frames)
    wave_data[-fade_frames:] *= np.linspace(1, 0, fade_frames)
    
    # Convert to 16-bit integers
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Write to WAV file
    filepath = os.path.join(SOUNDS_DIR, filename)
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    print(f"✓ Created: {filename}")

def main():
    """Create sample sound effects"""
    print("🎵 Creating sample sound effects...")
    
    # Ensure sounds directory exists
    os.makedirs(SOUNDS_DIR, exist_ok=True)
    
    # Create different sound effects with different frequencies/patterns
    create_beep_sound('jump.wav', frequency=523, duration=0.15)      # High C
    create_beep_sound('coin.wav', frequency=880, duration=0.1)       # High A
    create_beep_sound('collision.wav', frequency=220, duration=0.3)  # Low A
    create_beep_sound('gameover.wav', frequency=165, duration=0.8)   # Low E
    create_beep_sound('start.wav', frequency=659, duration=0.2)      # High E
    
    print("✓ All sample sound effects created!")
    print("📁 Location:", SOUNDS_DIR)
    print("📋 Replace these files with actual sound effects for better audio experience.")

if __name__ == "__main__":
    main()
