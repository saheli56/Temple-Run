"""
Test OpenCV Gesture Control with Phone Camera
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_opencv_gesture_control():
    """Test OpenCV gesture control system"""
    print("🧪 Testing OpenCV Gesture Control...")
    
    try:
        from modules.opencv_gesture_control import OpenCVGestureController
        
        # Create controller
        controller = OpenCVGestureController()
        print("✓ Controller created")
        
        # Get IP Webcam URL from user
        print("\n📱 IP Webcam Setup:")
        print("1. Install 'IP Webcam' app on your phone")
        print("2. Start the app and note the IP address shown")
        print("3. The URL format is: http://IP_ADDRESS:8080")
        print("   Example: http://192.168.1.100:8080")
        print("4. Or use 0 for default camera")
        
        camera_source = input("\nEnter IP Webcam URL or '0' for default camera: ").strip()
        
        if camera_source == '0':
            camera_source = 0
        
        # Test camera initialization
        if controller.initialize_camera(camera_source):
            print("✓ Camera initialized successfully")
            
            print("\n🤲 Testing gesture recognition...")
            print("⚠ Press 'q' to quit the test")
            print("📹 Camera window will show gesture detection")
            
            # Test gesture detection for 30 seconds or until 'q' is pressed
            import cv2
            import time
            
            start_time = time.time()
            test_duration = 30  # seconds
            
            while time.time() - start_time < test_duration:
                frame, gesture, confidence = controller.process_frame()
                
                if frame is not None:
                    # Show the frame
                    cv2.imshow("OpenCV Gesture Test", frame)
                    
                    # Check for gesture actions
                    action = controller.get_gesture_action()
                    if action:
                        print(f"🎯 Gesture Action: {action} (confidence: {confidence:.2f})")
                    
                    # Check for quit
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        print("⚠ Test stopped by user")
                        break
                else:
                    print("⚠ No frame received")
                    break
            
            print("✓ Gesture detection test completed")
            
        else:
            print("❌ Camera initialization failed")
            return False
        
        # Cleanup
        controller.cleanup()
        print("✓ Controller cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Run the test"""
    print("=" * 60)
    print("🚀 OPENCV GESTURE CONTROL TEST")
    print("=" * 60)
    
    if test_opencv_gesture_control():
        print("\n🎉 OpenCV gesture control test passed!")
        print("✅ Ready to use with Temple Run game")
        print("\n📱 To use with the game:")
        print("1. Ensure your phone's IP Webcam is running")
        print("2. Start the game: python main_enhanced.py")
        print("3. Enter your IP Webcam URL when prompted")
        print("4. Press 'G' to enable gesture control during gameplay")
    else:
        print("\n❌ Test failed!")
        print("⚠ Check your camera connection and try again")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
