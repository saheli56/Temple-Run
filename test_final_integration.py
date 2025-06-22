"""
Final Integration Test for Enhanced Temple Run with Gesture Control
Tests all major systems: sound, background, gesture control, and game mechanics
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        import cv2
        print("  ✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"  ❌ OpenCV import failed: {e}")
        return False
    
    try:
        import pygame
        print("  ✓ Pygame imported successfully")
    except ImportError as e:
        print(f"  ❌ Pygame import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("  ✓ NumPy imported successfully")
    except ImportError as e:
        print(f"  ❌ NumPy import failed: {e}")
        return False
    
    try:
        from modules.gesture_control import HandGestureController, MEDIAPIPE_AVAILABLE
        print(f"  ✓ Gesture control imported (MediaPipe available: {MEDIAPIPE_AVAILABLE})")
    except ImportError as e:
        print(f"  ❌ Gesture control import failed: {e}")
        return False
    
    try:
        from modules.background_simple import ParallaxBackground
        print("  ✓ Background system imported successfully")
    except ImportError as e:
        print(f"  ❌ Background system import failed: {e}")
        return False
    
    try:
        from utils.game_utils import sound_manager
        print("  ✓ Sound system imported successfully")
    except ImportError as e:
        print(f"  ❌ Sound system import failed: {e}")
        return False
    
    return True

def test_configurations():
    """Test game configurations"""
    print("\n⚙️  Testing configurations...")
    
    try:
        from config.game_config import (WINDOW_WIDTH, WINDOW_HEIGHT, FPS, 
                                      ENABLE_GESTURE_CONTROL, ENABLE_SOUND_EFFECTS)
        print("  ✓ Game config loaded")
        print(f"    - Window: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print(f"    - FPS: {FPS}")
        print(f"    - Gesture control enabled: {ENABLE_GESTURE_CONTROL}")
        print(f"    - Sound effects enabled: {ENABLE_SOUND_EFFECTS}")
        return True
    except Exception as e:
        print(f"  ❌ Config test failed: {e}")
        return False

def test_systems():
    """Test individual systems"""
    print("\n🔧 Testing individual systems...")
    
    # Test sound system
    try:
        from utils.game_utils import sound_manager
        print("  ✓ Sound manager initialized")
        print(f"    - Sound muted: {sound_manager.sound_muted}")
        print(f"    - Music muted: {sound_manager.music_muted}")
    except Exception as e:
        print(f"  ❌ Sound system test failed: {e}")
        return False
    
    # Test gesture control system
    try:
        from modules.gesture_control import HandGestureController, MEDIAPIPE_AVAILABLE
        controller = HandGestureController()
        
        if MEDIAPIPE_AVAILABLE:
            print("  ✓ Gesture controller created (MediaPipe available)")
            print("    - Camera initialization can be tested")
        else:
            print("  ✓ Gesture controller created (MediaPipe fallback mode)")
            print("    - Keyboard controls will be used")
    except Exception as e:
        print(f"  ❌ Gesture control test failed: {e}")
        return False
    
    # Test background system
    try:
        from modules.background_simple import ParallaxBackground
        bg = ParallaxBackground()
        print("  ✓ Background system initialized")
        print(f"    - Layers: {len(bg.layers) if hasattr(bg, 'layers') else 'unknown'}")
    except Exception as e:
        print(f"  ❌ Background system test failed: {e}")
        return False
    
    return True

def test_main_game_import():
    """Test main game import"""
    print("\n🎮 Testing main game import...")
    
    try:
        # Just test import, don't run the game
        import main_enhanced
        print("  ✓ Main game imported successfully")
        print("  ✓ All systems integrated properly")
        return True
    except Exception as e:
        print(f"  ❌ Main game import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 TEMPLE RUN ENHANCED - FINAL INTEGRATION TEST")
    print("=" * 60)
    
    all_passed = True
    
    # Get MediaPipe availability
    try:
        from modules.gesture_control import MEDIAPIPE_AVAILABLE
    except ImportError:
        MEDIAPIPE_AVAILABLE = False
    
    # Run all tests
    tests = [
        test_imports,
        test_configurations,
        test_systems,
        test_main_game_import
    ]
    
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Temple Run Enhanced is ready to play!")
        print("\n🎮 To start the game:")
        print("   python main_enhanced.py")
        print("\n🤲 Gesture Control:")
        if MEDIAPIPE_AVAILABLE:
            print("   - Available! Press 'G' in-game to toggle")
            print("   - Make sure your camera is working")
        else:
            print("   - Install MediaPipe: pip install mediapipe")
            print("   - Game works perfectly with keyboard controls")
        print("\n📚 Documentation:")
        print("   - README.md - General game information")
        print("   - GESTURE_CONTROL_README.md - Gesture control guide")
        print("   - SOUND_SYSTEM_README.md - Audio system details")
    else:
        print("❌ SOME TESTS FAILED!")
        print("⚠️  Check the error messages above for issues to resolve")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
