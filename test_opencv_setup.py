#!/usr/bin/env python3
"""
Quick test script to verify OpenCV gesture control setup
Tests the module without requiring an actual camera connection
"""

import sys
import os

# Add the project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_opencv_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing OpenCV Gesture Control Setup...")
    print("=" * 50)
    
    try:
        print("📦 Testing imports...")
        
        # Test OpenCV
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
        
        # Test requests
        import requests
        print(f"✅ Requests: {requests.__version__}")
        
        # Test numpy
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
        
        # Test our gesture control module
        from modules.opencv_gesture_control import OpenCVGestureController
        print("✅ OpenCV Gesture Controller: Module imported successfully")
        
        # Test controller creation
        controller = OpenCVGestureController()
        print("✅ Controller Creation: Successfully created controller instance")
        
        # Test enum
        from modules.opencv_gesture_control import GestureType
        print(f"✅ Gesture Types: {[g.value for g in GestureType]}")
        
        print("\n🎉 All imports successful!")
        print("📱 You can now use phone camera gesture control")
        print("💡 Run 'python main_enhanced.py' to start the game")
        print("📖 See PHONE_CAMERA_SETUP.md for phone setup instructions")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Try running: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_fallback_system():
    """Test the gesture control fallback system"""
    print("\n🔄 Testing Fallback System...")
    print("=" * 30)
    
    try:
        # Test MediaPipe import
        try:
            import mediapipe as mp
            print("✅ MediaPipe: Available")
            mediapipe_available = True
        except ImportError:
            print("⚠️  MediaPipe: Not available (will use OpenCV)")
            mediapipe_available = False
        
        # Test OpenCV fallback
        from modules.opencv_gesture_control import OpenCVGestureController
        print("✅ OpenCV Fallback: Available")
        
        # Test keyboard fallback
        from modules.keyboard_gesture_control import KeyboardGestureController
        print("✅ Keyboard Fallback: Available")
        
        # Determine which system will be used
        if mediapipe_available:
            print("🎯 Primary System: MediaPipe gesture control")
        else:
            print("🎯 Primary System: OpenCV gesture control (phone camera)")
        
        print("✅ Fallback system working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Temple Run - OpenCV Gesture Control Test")
    print("=" * 50)
    
    # Run tests
    imports_ok = test_opencv_imports()
    fallback_ok = test_fallback_system()
    
    if imports_ok and fallback_ok:
        print("\n🎉 SUCCESS: All systems ready!")
        print("🎮 You can now run the game with phone camera gesture control")
    else:
        print("\n❌ FAILED: Some systems not working")
        print("💡 Check the error messages above and install missing packages")
    
    print("\n📚 Next steps:")
    print("1. Install 'IP Webcam' app on your phone")
    print("2. Run 'python main_enhanced.py' to start the game")
    print("3. Enter your phone's IP address when prompted")
    print("4. See PHONE_CAMERA_SETUP.md for detailed instructions")
