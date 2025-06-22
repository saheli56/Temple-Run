#!/usr/bin/env python3
"""
Test script for OpenCV gesture control with phone camera via IP Webcam
"""

import cv2
import sys
import os

# Add the project directory to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.opencv_gesture_control import OpenCVGestureController

def test_phone_camera():
    """Test phone camera connection and gesture recognition"""
    print("📱 Testing phone camera gesture control...")
    print("="*50)
    
    # Create gesture controller
    controller = OpenCVGestureController()
    
    # Get IP Webcam URL from user
    print("\n📱 Phone Camera Setup:")
    print("1. Install 'IP Webcam' app on your phone")
    print("2. Start the app and note the IP address shown")
    print("3. Example URL: http://192.168.1.100:8080")
    print("4. Make sure your phone and computer are on the same WiFi network")
    
    ip_webcam_url = input("\nEnter your phone's IP Webcam URL: ").strip()
    
    if not ip_webcam_url or 'http' not in ip_webcam_url:
        print("❌ Invalid URL provided. Please enter a valid IP Webcam URL.")
        return
    
    print(f"\n🔄 Connecting to: {ip_webcam_url}")
    
    # Try to initialize camera
    if not controller.initialize_camera(ip_webcam_url):
        print("❌ Failed to connect to phone camera")
        print("💡 Make sure:")
        print("   - IP Webcam app is running on your phone")
        print("   - Phone and computer are on same WiFi network")
        print("   - URL is correct (should include http://)")
        return
    
    print("✅ Successfully connected to phone camera!")
    print("\n🤲 Gesture Recognition Test:")
    print("- Make a FIST to trigger JUMP gesture")
    print("- Show 1 FINGER to trigger CROUCH gesture") 
    print("- Show OPEN HAND for IDLE gesture")
    print("- Press 'q' to quit")
    print("- Press 'd' to toggle debug display")
    print("- Press 'ESC' to exit")
    
    # Main test loop
    frame_count = 0
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
                print(f"🎯 Action detected: {action.upper()} (confidence: {confidence:.2f})")
            
            # Display frame
            cv2.imshow("Phone Camera Gesture Test", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC
                break
            elif key == ord('d'):
                debug_status = controller.toggle_debug()
                print(f"🔧 Debug display: {'ON' if debug_status else 'OFF'}")
            
            # Print status every 30 frames
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame_count}: {gesture.value} ({confidence:.2f})")
    
    except KeyboardInterrupt:
        print("\n⚠ Test interrupted by user")
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        # Cleanup
        controller.cleanup()
        cv2.destroyAllWindows()
        print("\n✅ Test completed!")

if __name__ == "__main__":
    test_phone_camera()
