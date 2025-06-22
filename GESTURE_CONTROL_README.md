# 🤲 Hand Gesture Control System

## Overview
The Temple Run game now includes advanced hand gesture control with multiple backends: **MediaPipe** for precise hand tracking, **OpenCV with phone camera support** for Python 3.13 compatibility, and **keyboard gesture simulation** as a fallback. Players can control the game using natural hand gestures via webcam or phone camera.

## Features
- **Multiple gesture control backends** - MediaPipe, OpenCV (phone camera), keyboard simulation
- **📱 Phone camera support** - Use your phone as a webcam via IP Webcam app
- **Real-time gesture recognition** using computer vision algorithms
- **Toggle control modes** - Switch between keyboard and gesture control with 'G' key
- **Visual feedback** - See your hand tracking and gesture recognition in real-time
- **Smooth gesture detection** - Built-in smoothing to prevent false detections
- **Graceful fallback** - Automatic fallback system ensures the game always works
- **Python 3.13 compatible** - Works with latest Python versions using OpenCV

## Gesture Commands

| Gesture | Action | Description |
|---------|--------|-------------|
| ✊ **Closed Fist** | **JUMP** | Make a tight fist to make the player jump |
| ☝️ **Index Finger** | **CROUCH** | Point with your index finger to crouch/slide |
| ✋ **Open Palm** | **IDLE** | Show an open palm for normal running |

## Installation Requirements

### Automatic System Selection
The game automatically selects the best available gesture control system:

1. **MediaPipe (Priority 1)** - Most accurate, requires Python 3.7-3.11
2. **OpenCV + Phone Camera (Priority 2)** - Works with Python 3.13, uses phone via IP Webcam
3. **Keyboard Simulation (Priority 3)** - Always available fallback

### MediaPipe Installation (Optional)
```bash
pip install mediapipe
```

**Note:** MediaPipe requires:
- Python 3.7-3.11 (MediaPipe may not support newer Python versions)
- Webcam/camera access
- Compatible operating system (Windows, macOS, Linux)

### 📱 Phone Camera Setup (Recommended for Python 3.13)
1. **Install IP Webcam app** on your Android phone
2. **Connect devices** to same WiFi network
3. **Start IP Webcam** and note the IP address
4. **Enter URL** when prompted by the game

For detailed setup instructions, see [PHONE_CAMERA_SETUP.md](PHONE_CAMERA_SETUP.md)

### Camera Setup
- **Default Camera**: Usually index `0` for built-in webcam
- **Phone Camera**: IP Webcam URL (e.g., `http://192.168.1.100:8080`)
- **Resolution**: 640x480 (automatically configured)
- **Frame Rate**: 30 FPS

## Game Controls

### During Gameplay:
- **G** - Toggle between gesture and keyboard control
- **SPACE** - Jump (keyboard mode)
- **P** - Pause game
- **M** - Mute/unmute audio
- **Q** - Quit game

### Gesture Control Mode:
- **Camera window** shows your hand tracking (MediaPipe/OpenCV)
- **Phone camera feed** displays your gesture recognition (OpenCV mode)
- **Green indicators** show recognized gestures
- **Confidence display** shows detection accuracy
- **Control status** shown in game HUD
- **Press 'G'** to toggle between gesture and keyboard control

## Gesture Control Systems

### 1. 📱 OpenCV + Phone Camera (Python 3.13 Compatible)
- **Best for**: Python 3.13 users, better camera positioning
- **Setup**: Use IP Webcam app on phone
- **Recognition**: Advanced contour-based hand detection
- **Gestures**: Fist (jump), 1 finger (crouch), open hand (idle)

### 2. 🎥 MediaPipe (Most Accurate)
- **Best for**: Python 3.7-3.11 users with webcam
- **Setup**: Built-in webcam or USB camera
- **Recognition**: AI-powered hand landmark detection
- **Gestures**: Precise finger tracking and pattern recognition

### 3. ⌨️ Keyboard Simulation (Always Available)
- **Best for**: Fallback when cameras aren't available
- **Setup**: No additional hardware needed
- **Controls**: F=Fist, I=Index finger, O=Open hand
- **Use**: Press gesture keys during gameplay

## Technical Details

### Gesture Recognition Algorithms:

#### MediaPipe System:
1. **Hand Detection**: MediaPipe Hands detects hand landmarks
2. **Distance Calculation**: Measures finger positions relative to palm
3. **Gesture Classification**: Analyzes finger patterns for gestures
4. **Smoothing**: Uses 5-frame history to prevent flickering
5. **Cooldown**: 0.5-second minimum between actions

#### OpenCV System:
1. **Skin Detection**: HSV color space filtering for hand regions
2. **Contour Analysis**: Finds largest hand contour in frame
3. **Convexity Detection**: Analyzes hand shape and finger positions
4. **Gesture Classification**: Uses solidity and finger count
5. **Background Subtraction**: Isolates hand from background
6. **Smoothing**: History-based gesture stabilization

### Performance Optimization:
- **Single hand tracking** for better performance
- **Confidence thresholds** to ensure accurate detection
- **Background processing** doesn't block game rendering
- **Automatic cleanup** of camera resources

## Troubleshooting

### System Selection Issues
```
📢 Using OpenCV gesture control (phone camera support)
```
This means MediaPipe isn't available and the system is using OpenCV with phone camera support.

### MediaPipe Not Available
```
⚠ Warning: MediaPipe not available. Gesture control will be disabled.
```
**Solution**: This is normal for Python 3.13. The system will use OpenCV gesture control instead.

### Phone Camera Connection Issues
```
❌ Failed to connect to phone camera
```
**Solutions**:
- Ensure IP Webcam app is running on your phone
- Check that both devices are on the same WiFi network
- Verify the IP address is correct (include http://)
- Try restarting the IP Webcam app

### Camera Access Issues
```
⚠ Warning: Could not open camera 0
```
**Solutions**:
- Ensure webcam is connected and not used by other apps
- Try different camera index (0, 1, 2...)
- Check camera permissions in system settings
- For phone camera, ensure IP Webcam URL is correct

### Poor Gesture Recognition
**Tips for Better Recognition**:
- **Good Lighting**: Ensure adequate lighting on your hand
- **Clear Background**: Use contrasting background behind your hand
- **Proper Distance**: Keep hand 1-2 feet from camera
- **Steady Movement**: Make clear, deliberate gestures
- **Single Hand**: Use only one hand for better tracking

### Performance Issues
- **Close camera window** if not needed (toggle with camera_feed setting)
- **Disable debug overlay** for better performance
- **Lower camera resolution** in configuration if needed

## Configuration Options

In `config/game_config.py`:

```python
# Gesture Control Configuration
ENABLE_GESTURE_CONTROL = True           # Enable/disable gesture system
GESTURE_CAMERA_INDEX = 0                # Camera device index
GESTURE_CONFIDENCE_THRESHOLD = 0.7      # Minimum confidence for actions
GESTURE_COOLDOWN_TIME = 0.5            # Seconds between gesture actions
SHOW_GESTURE_DEBUG = True              # Show debug information
SHOW_CAMERA_FEED = True                # Display camera window
GESTURE_CAMERA_WIDTH = 320             # Camera display width
GESTURE_CAMERA_HEIGHT = 240            # Camera display height
```

## File Structure

```
modules/
├── gesture_control.py          # Main gesture recognition system
└── ...

config/
├── game_config.py             # Gesture control configuration
└── ...

test_gesture_integration.py    # Test script for gesture system
GESTURE_CONTROL_README.md      # This documentation
```

## Testing

Run the gesture control test:
```bash
python test_gesture_integration.py
```

This will:
- Test MediaPipe installation
- Initialize camera and gesture recognition
- Show live gesture detection for 10 seconds
- Verify all gestures work correctly

## Future Enhancements

Potential improvements:
- **Two-hand gestures** for more complex controls
- **Custom gesture training** for personalized controls
- **Gesture sensitivity adjustment** in-game
- **Voice commands** integration
- **Eye tracking** for enhanced control

## Support

If you encounter issues:
1. Check MediaPipe installation: `pip list | grep mediapipe`
2. Test camera access: `python -c "import cv2; print(cv2.VideoCapture(0).read())"`
3. Run gesture test: `python test_gesture_integration.py`
4. Check Python version compatibility with MediaPipe

The gesture control system is designed to be robust and will gracefully fall back to keyboard controls if any issues occur, ensuring the game always remains playable!
