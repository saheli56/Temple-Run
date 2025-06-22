"""
Test Gesture Control Integration
Quick test script to verify gesture control system works with the game
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gesture_control import HandGestureController
import cv2
import time

def test_gesture_integration():
    """Test the gesture control system"""
    print("🧪 Testing Gesture Control Integration...")
    
    try:
        # Initialize gesture controller
        controller = HandGestureController()
        
        if not controller.initialize_camera(0):
            print("❌ Camera initialization failed")
            return False
        
        print("✓ Gesture controller initialized")
        print("📹 Testing gesture recognition for 10 seconds...")
        print("   - Make a FIST to test JUMP")
        print("   - Point INDEX FINGER to test CROUCH")  
        print("   - Show OPEN PALM for IDLE")
        print("   - Press 'q' to quit early")
        
        start_time = time.time()
        last_action_time = 0
        
        while time.time() - start_time < 10:
            # Process frame
            frame, gesture, confidence = controller.process_frame()
            
            if frame is not None:
                # Show camera feed
                cv2.imshow("Gesture Test", frame)
                
                # Get gesture action
                action = controller.get_gesture_action()
                
                # Print action if detected
                current_time = time.time()
                if action and current_time - last_action_time > 1.0:
                    print(f"🎮 Action detected: {action.upper()}")
                    last_action_time = current_time
            
            # Check for quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        # Cleanup
        controller.cleanup()
        cv2.destroyAllWindows()
        
        print("✅ Gesture control test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing MediaPipe: pip install mediapipe")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_gesture_integration()  
    if success:
        print("\n🎮 Gesture control is ready for the game!")
        print("   Start the game and press 'G' to toggle gesture control.")
    else:
        print("\n⚠ Gesture control test failed. The game will work with keyboard only.")
