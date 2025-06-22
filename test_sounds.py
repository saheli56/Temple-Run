"""
Sound Effects Tester for Temple Run Game
Simple script to test sound loading and playback
"""

import pygame
import os
import sys

# Add the parent directory to the path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.game_config import *
from utils.game_utils import SoundManager

def test_sounds():
    """Test all sound effects"""
    print("🎵 Testing Temple Run Sound System")
    print("=" * 40)
    
    # Initialize pygame
    pygame.init()
    
    # Create sound manager
    sound_manager = SoundManager()
    
    # Test sound files
    sound_files = {
        'jump': os.path.join(SOUNDS_DIR, 'jump.wav'),
        'coin': os.path.join(SOUNDS_DIR, 'coin.wav'),
        'collision': os.path.join(SOUNDS_DIR, 'collision.wav'),
        'game_over': os.path.join(SOUNDS_DIR, 'gameover.wav'),
        'start': os.path.join(SOUNDS_DIR, 'start.wav')
    }
    
    # Load sounds
    print("Loading sound effects...")
    for name, filepath in sound_files.items():
        sound_manager.load_sound(name, filepath)
    
    # Test background music
    print("\nTesting background music...")
    music_file = os.path.join(SOUNDS_DIR, 'background_music.mp3')
    if os.path.exists(music_file):
        sound_manager.play_music(music_file, loop=0)  # Play once for testing
        print("✓ Background music loaded and playing")
    else:
        print("⚠ Background music file not found")
    
    # Interactive testing
    print("\n" + "=" * 40)
    print("Interactive Sound Test")
    print("=" * 40)
    print("Commands:")
    print("  1 - Play jump sound")
    print("  2 - Play coin sound")
    print("  3 - Play collision sound")
    print("  4 - Play game over sound")
    print("  5 - Play start sound")
    print("  m - Toggle mute")
    print("  s - Show sound status")
    print("  q - Quit")
    print("=" * 40)
    
    try:
        while True:
            command = input("\nEnter command: ").strip().lower()
            
            if command == '1':
                sound_manager.play_sound('jump')
                print("🎵 Playing jump sound")
            elif command == '2':
                sound_manager.play_sound('coin')
                print("🎵 Playing coin sound")
            elif command == '3':
                sound_manager.play_sound('collision')
                print("🎵 Playing collision sound")
            elif command == '4':
                sound_manager.play_sound('game_over')
                print("🎵 Playing game over sound")
            elif command == '5':
                sound_manager.play_sound('start')
                print("🎵 Playing start sound")
            elif command == 'm':
                muted = sound_manager.toggle_all_mute()
                print(f"🔇 All audio {'muted' if muted else 'unmuted'}")
            elif command == 's':
                status = sound_manager.get_sound_status()
                print("\n📊 Sound System Status:")
                print(f"  Sound Effects Muted: {status['sound_muted']}")
                print(f"  Music Muted: {status['music_muted']}")
                print(f"  Music Playing: {status['music_playing']}")
                print(f"  Current Music: {status['current_music']}")
                print(f"  Loaded Sounds: {', '.join(status['loaded_sounds'])}")
            elif command == 'q':
                break
            else:
                print("❌ Invalid command")
    
    except KeyboardInterrupt:
        print("\n\n👋 Exiting sound tester...")
    
    finally:
        pygame.quit()
        print("✓ Sound system cleaned up")

if __name__ == "__main__":
    test_sounds()
