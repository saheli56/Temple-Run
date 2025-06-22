#!/usr/bin/env python3
"""
Test OpenCV gesture control with your specific phone camera
"""

import cv2
import sys
import os

# Add the project directory to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.opencv_gesture_control import OpenCVGestureController

def test_your_phone_camera():
    """Test gesture recognition with your phone camera"""
    print("📱 Testing Gesture Control with Your Phone Camera")
    print("=" * 50)
    
    ip_webcam_url = "http://100.102.121.116:8080"
    
    # Create gesture controller
    controller = OpenCVGestureController()
    
    print(f"🔄 Connecting to your phone: {ip_webcam_url}")
    
    # Try to initialize camera
    if not controller.initialize_camera(ip_webcam_url):
        print("❌ Failed to connect to phone camera")
        return
    
    print("✅ Successfully connected to your phone camera!")
    print("\n🤲 Gesture Recognition Test:")
    print("- Make a FIST to trigger JUMP gesture")
    print("- Show 1 FINGER to trigger CROUCH gesture") 
    print("- Show OPEN HAND for IDLE gesture")
    print("- Press 'q' to quit")
    print("- Press 'd' to toggle debug display")
    print("- Press 'ESC' to exit")
    print("\n💡 Position your hand clearly in front of your phone camera")
    
    # Main test loop
    frame_count = 0
    actions_detected = 0
    
    try:
        while True:
            # Process frame
            frame, gesture, confidence = controller.process_frame()
            
            if frame is None:
                print("⚠ No frame received from camera")
                break
            
            frame_count += 1
            
            # Get gesture action
            action = controller.get_gesture_action()
            if action:
                actions_detected += 1
                print(f"🎯 Action #{actions_detected}: {action.upper()} (confidence: {confidence:.2f})")
            
            # Display frame
            cv2.imshow("Your Phone Camera - Gesture Test", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC
                break
            elif key == ord('d'):
                debug_status = controller.toggle_debug()
                print(f"🔧 Debug display: {'ON' if debug_status else 'OFF'}")
            
            # Print status every 60 frames (about 2 seconds)
            if frame_count % 60 == 0:
                print(f"📊 Frame {frame_count}: Current gesture = {gesture.value} ({confidence:.2f}), Actions detected = {actions_detected}")
    
    except KeyboardInterrupt:
        print("\n⚠ Test interrupted by user")
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        # Cleanup
        controller.cleanup()
        cv2.destroyAllWindows()
        print(f"\n✅ Test completed! Detected {actions_detected} gesture actions")

if __name__ == "__main__":
    test_your_phone_camera()
