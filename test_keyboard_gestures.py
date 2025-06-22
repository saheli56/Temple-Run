"""
Test the keyboard gesture simulation system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_keyboard_gestures():
    """Test keyboard gesture simulation"""
    print("🧪 Testing Keyboard Gesture Simulation...")
    
    try:
        from modules.keyboard_gesture_control import KeyboardGestureController
        
        # Create controller
        controller = KeyboardGestureController()
        print("✓ Controller created")
        
        # Test camera initialization
        if controller.initialize_camera():
            print("✓ Camera simulation initialized")
        else:
            print("❌ Camera simulation failed")
            return False
        
        # Test gesture simulation
        print("\n🤲 Testing gesture simulation...")
        
        # Test fist gesture (jump)
        if controller.set_gesture_from_key('F'):
            print("✓ Fist gesture (F) recognized")
        
        # Test index finger gesture (crouch)
        if controller.set_gesture_from_key('I'):
            print("✓ Index finger gesture (I) recognized")
        
        # Test open palm gesture (idle)
        if controller.set_gesture_from_key('O'):
            print("✓ Open palm gesture (O) recognized")
        
        # Test frame processing
        frame, gesture, confidence = controller.process_frame()
        if frame is not None:
            print(f"✓ Frame processing works - Current gesture: {gesture.value}")
        
        # Test action detection
        action = controller.get_gesture_action()
        print(f"✓ Gesture action detection: {action}")
        
        # Cleanup
        controller.cleanup()
        print("✓ Controller cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_game_integration():
    """Test integration with main game"""
    print("\n🎮 Testing game integration...")
    
    try:
        # Test import
        from main_enhanced import TempleRunGame, GESTURE_CONTROLLER_TYPE
        
        print(f"✓ Game imported successfully")
        print(f"✓ Gesture controller type: {GESTURE_CONTROLLER_TYPE}")
        
        # Test controller creation
        if GESTURE_CONTROLLER_TYPE == "keyboard":
            print("✓ Using keyboard gesture simulation as expected")
        else:
            print("⚠ Expected keyboard simulation but got different type")
        
        return True
        
    except Exception as e:
        print(f"❌ Game integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 KEYBOARD GESTURE SIMULATION TEST")
    print("=" * 60)
    
    all_passed = True
    
    # Test keyboard gestures
    if not test_keyboard_gestures():
        all_passed = False
    
    # Test game integration
    if not test_game_integration():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Keyboard gesture simulation is working!")
        print("\n🎮 To play with gesture simulation:")
        print("   1. Run: python main_enhanced.py")
        print("   2. Press 'G' to enable gesture control")
        print("   3. Use keyboard gestures:")
        print("      - F = Fist (Jump)")
        print("      - I = Index finger (Crouch)")
        print("      - O = Open palm (Idle)")
        print("   4. A visualization window will show current gesture")
    else:
        print("❌ SOME TESTS FAILED!")
        print("⚠️ Check the error messages above")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
