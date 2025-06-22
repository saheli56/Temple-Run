# Phone Camera Gesture Control Setup Guide

## Overview
This Temple Run game now supports hand gesture control using your phone's camera via the IP Webcam app and OpenCV. This allows you to control the game with hand gestures detected through your phone's camera.

## Prerequisites

### 1. Install Required Packages
Make sure you have installed all required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Set up IP Webcam on Your Phone

#### For Android:
1. **Install IP Webcam App**
   - Download "IP Webcam" by Pavel Khlebovich from Google Play Store
   - It's a free app with good reviews

2. **Configure IP Webcam**
   - Open the IP Webcam app
   - Scroll down and start the server by tapping "Start server"
   - The app will show you the IP address (e.g., `http://192.168.1.100:8080`)
   - Keep the app running while playing the game

#### For iOS:
1. **Install a Compatible App**
   - Download "WebCamera" or similar IP camera app from App Store
   - Configure it to stream video over HTTP

### 3. Network Setup
- Ensure your phone and computer are connected to the same WiFi network
- Note down the IP address shown in the app (e.g., `192.168.1.100:8080`)

## How to Use

### 1. Running the Game
```bash
python main_enhanced.py
```

### 2. Camera Setup
When you run the game, it will prompt you for the IP Webcam URL:
```
📱 OpenCV Gesture Control - Phone Camera Setup:
1. Install 'IP Webcam' app on your phone
2. Start the app and note the IP address shown
3. Make sure phone and computer are on same WiFi network
4. Example URL: http://192.168.1.100:8080
Enter your phone's IP Webcam URL (or press Enter for default camera):
```

Enter your phone's IP address (including `http://` and port number).

### 3. Hand Gestures

The game recognizes these hand gestures:

| Gesture | Action | Description |
|---------|--------|-------------|
| **Closed Fist** | Jump | Make a tight fist to make the player jump |
| **One Finger** | Crouch | Point with index finger to crouch/slide |
| **Open Hand** | Idle | Open palm for normal running |

### 4. Game Controls

#### Keyboard Controls:
- `SPACE` - Jump (keyboard alternative)
- `G` - Toggle gesture control on/off
- `P` - Pause/Resume game
- `M` - Mute/Unmute audio
- `Q` - Quit game

#### Gesture Tips:
- Keep your hand clearly visible to the camera
- Use good lighting for better detection
- Hold gestures for a moment to ensure recognition
- Position your hand 1-2 feet from the phone camera

### 5. Game Interface

The game will show:
- **Gesture Control Status**: Green icon when active
- **Camera Feed Window**: Shows your hand and gesture detection (if enabled)
- **Debug Information**: Gesture type and confidence level

## Testing Gesture Control

### Test Script
Use the test script to verify your setup before playing:
```bash
python test_phone_camera.py
```

This will:
- Test connection to your phone camera
- Show live gesture recognition
- Display debug information
- Let you practice gestures

### Test Controls:
- `Q` or `ESC` - Quit test
- `D` - Toggle debug display

## Troubleshooting

### Camera Connection Issues
1. **"Failed to connect to phone camera"**
   - Check if phone and computer are on same WiFi network
   - Verify the IP address is correct
   - Make sure IP Webcam app is running on phone
   - Try restarting the IP Webcam app

2. **"No frame received from camera"**
   - Check internet connection stability
   - Try moving closer to WiFi router
   - Restart the IP Webcam app

### Gesture Recognition Issues
1. **Gestures not detected**
   - Ensure good lighting
   - Keep hand clearly visible
   - Try different distances from camera
   - Check if debug window shows your hand outline

2. **False gesture detection**
   - Remove background objects that might look like hands
   - Ensure only one hand is visible
   - Try adjusting camera angle

3. **Delayed response**
   - Check network latency
   - Close other applications using network
   - Try reducing camera resolution in IP Webcam settings

### Performance Issues
1. **Game running slowly**
   - Close camera feed window (`SHOW_CAMERA_FEED = False` in config)
   - Reduce IP Webcam resolution/quality in app settings
   - Close other applications

## Configuration

You can modify settings in `config/game_config.py`:

```python
# Gesture Control Configuration
ENABLE_GESTURE_CONTROL = True
SHOW_CAMERA_FEED = True          # Show gesture camera window
SHOW_GESTURE_DEBUG = True        # Show debug information

# IP Webcam Configuration
IP_WEBCAM_URL = None             # Set to skip URL prompt
# IP_WEBCAM_URL = "http://192.168.1.100:8080"  # Example

# OpenCV Gesture Thresholds
OPENCV_GESTURE_CONFIDENCE_THRESHOLD = 0.6
OPENCV_GESTURE_COOLDOWN = 0.5
OPENCV_MIN_CONTOUR_AREA = 3000
```

## Advanced Features

### Gesture Smoothing
The system uses gesture history smoothing to reduce false positives and provide stable recognition.

### Background Subtraction
Advanced background subtraction helps isolate hand movements from background changes.

### Confidence Scoring
Each gesture has a confidence score - only high-confidence gestures trigger actions.

## Fallback Options

If OpenCV gesture control doesn't work:

1. **MediaPipe Gesture Control** (if available)
   - Automatically used if MediaPipe is installed
   - More accurate but may not work on Python 3.13

2. **Keyboard Gesture Simulation**
   - Press `F` for fist (jump)
   - Press `I` for index finger (crouch)
   - Press `O` for open hand (idle)

## Tips for Best Experience

1. **Camera Position**: Position phone camera at chest/face level
2. **Lighting**: Use good, even lighting (avoid backlighting)
3. **Background**: Use a plain background behind your hand
4. **Hand Size**: Keep hand medium distance - not too close or far
5. **Gesture Clarity**: Make distinct, clear gestures
6. **Network**: Use 5GHz WiFi for better performance if available

## Support

If you encounter issues:
1. Check this documentation
2. Run the test script to diagnose problems
3. Try the fallback keyboard gesture mode
4. Check network connectivity between phone and computer
