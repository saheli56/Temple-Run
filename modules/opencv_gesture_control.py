"""
OpenCV-based Hand Gesture Control for Temple Run Game
Uses phone camera via IP Webcam app for gesture recognition
"""

import cv2
import numpy as np
import time
from enum import Enum
import requests
from urllib.parse import urlparse

class GestureType(Enum):
    """Enumeration of recognized gestures"""
    IDLE = "idle"
    JUMP = "jump"
    CROUCH = "crouch"
    UNKNOWN = "unknown"

class OpenCVGestureController:
    """
    OpenCV-based gesture controller using phone camera via IP Webcam
    Uses contour detection and hand analysis for gesture recognition
    """
    
    def __init__(self):
        print("📱 Initializing OpenCV gesture control with phone camera...")
        
        # Camera settings
        self.cap = None
        self.camera_active = False
        self.ip_webcam_url = None
        
        # Gesture recognition parameters
        self.current_gesture = GestureType.IDLE
        self.gesture_confidence = 0.0
        self.gesture_history = []
        self.history_size = 5
        
        # Hand detection parameters
        self.skin_lower = np.array([0, 20, 70], dtype=np.uint8)
        self.skin_upper = np.array([20, 255, 255], dtype=np.uint8)
        
        # Gesture thresholds
        self.min_contour_area = 3000
        self.finger_threshold = 0.8
        self.fist_threshold = 0.3
        
        # Timing for gesture actions
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.5
        
        # Debug and display options
        self.show_debug = True
        self.show_camera_feed = True
        
        # Background subtractor for better hand detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        self.frame_count = 0
        
        print("✓ OpenCV gesture controller initialized")
    
    def initialize_camera(self, camera_source=0):
        """Initialize camera - can be device index or IP webcam URL"""
        try:
            if isinstance(camera_source, str) and 'http' in camera_source:
                # IP Webcam URL
                self.ip_webcam_url = camera_source
                if not self.ip_webcam_url.endswith('/video'):
                    self.ip_webcam_url += '/video'
                
                # Test connection
                response = requests.get(self.ip_webcam_url, timeout=5, stream=True)
                if response.status_code == 200:
                    self.cap = cv2.VideoCapture(self.ip_webcam_url)
                    print(f"✓ Connected to IP Webcam: {camera_source}")
                else:
                    print(f"❌ Failed to connect to IP Webcam: {camera_source}")
                    return False
            else:
                # Regular camera device
                self.cap = cv2.VideoCapture(camera_source)
                print(f"✓ Connected to camera device: {camera_source}")
            
            if not self.cap.isOpened():
                print("❌ Failed to open camera")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            self.camera_active = True
            print("✓ Camera initialized successfully")
            
            # Initialize background subtractor
            for _ in range(10):
                ret, frame = self.cap.read()
                if ret:
                    self.bg_subtractor.apply(frame)
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing camera: {e}")
            return False
    
    def detect_skin(self, frame):
        """Detect skin-colored regions in the frame"""
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for skin color
        mask = cv2.inRange(hsv, self.skin_lower, self.skin_upper)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Apply Gaussian blur to smooth the mask
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        
        return mask
    
    def find_hand_contour(self, mask):
        """Find the largest hand contour in the mask"""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Find the largest contour (assuming it's the hand)
        hand_contour = max(contours, key=cv2.contourArea)
        
        # Check if contour is large enough
        if cv2.contourArea(hand_contour) < self.min_contour_area:
            return None
        
        return hand_contour
    
    def analyze_hand_gesture(self, contour, frame):
        """Analyze hand contour to determine gesture"""
        if contour is None:
            return GestureType.UNKNOWN, 0.0
        
        # Get convex hull and convexity defects
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour, hull)
        
        if defects is None:
            return GestureType.UNKNOWN, 0.0
        
        # Count fingers based on convexity defects
        finger_count = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            
            # Calculate the distance from far point to convex hull
            if d > 8000:  # Threshold for significant defect
                finger_count += 1
        
        # Adjust finger count (convexity defects count gaps between fingers)
        finger_count += 1
        
        # Get contour area and hull area for gesture analysis
        contour_area = cv2.contourArea(contour)
        hull_points = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull_points)
        
        # Calculate solidity (ratio of contour area to hull area)
        solidity = float(contour_area) / hull_area if hull_area > 0 else 0
        
        # Gesture recognition based on finger count and solidity
        gesture = GestureType.UNKNOWN
        confidence = 0.0
        
        if solidity < self.fist_threshold:
            # Closed fist - low solidity
            gesture = GestureType.JUMP
            confidence = (self.fist_threshold - solidity) / self.fist_threshold
        elif finger_count == 1:
            # One finger extended
            gesture = GestureType.CROUCH
            confidence = 0.8
        elif finger_count >= 4:
            # Open hand - multiple fingers
            gesture = GestureType.IDLE
            confidence = min(finger_count / 5.0, 1.0)
        else:
            # Ambiguous gesture
            gesture = GestureType.UNKNOWN
            confidence = 0.3
        
        return gesture, min(confidence, 1.0)
    
    def smooth_gesture(self, gesture, confidence):
        """Smooth gesture recognition using history"""
        # Add to history
        self.gesture_history.append((gesture, confidence))
        
        # Keep only recent history
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)
        
        # Count occurrences of each gesture in history
        gesture_counts = {}
        total_confidence = 0
        
        for hist_gesture, hist_confidence in self.gesture_history:
            if hist_gesture not in gesture_counts:
                gesture_counts[hist_gesture] = {'count': 0, 'confidence': 0}
            gesture_counts[hist_gesture]['count'] += 1
            gesture_counts[hist_gesture]['confidence'] += hist_confidence
            total_confidence += hist_confidence
        
        # Find most frequent gesture with highest confidence
        best_gesture = GestureType.IDLE
        best_score = 0
        
        for gest, data in gesture_counts.items():
            score = data['count'] * data['confidence']
            if score > best_score:
                best_gesture = gest
                best_score = score
        
        # Calculate smoothed confidence
        smoothed_confidence = total_confidence / len(self.gesture_history)
        
        return best_gesture, smoothed_confidence
    
    def process_frame(self):
        """Process one frame from the camera and detect gestures"""
        if not self.camera_active or not self.cap:
            return None, GestureType.IDLE, 0.0
        
        ret, frame = self.cap.read()
        if not ret:
            return None, GestureType.IDLE, 0.0
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        self.frame_count += 1
        
        # Detect skin regions
        skin_mask = self.detect_skin(frame)
        
        # Find hand contour
        hand_contour = self.find_hand_contour(skin_mask)
        
        # Analyze gesture
        gesture = GestureType.IDLE
        confidence = 0.0
        
        if hand_contour is not None:
            gesture, confidence = self.analyze_hand_gesture(hand_contour, frame)
            
            # Apply smoothing
            gesture, confidence = self.smooth_gesture(gesture, confidence)
            
            # Draw hand contour and debug info
            if self.show_debug:
                cv2.drawContours(frame, [hand_contour], -1, (0, 255, 0), 2)
                
                # Draw convex hull
                hull = cv2.convexHull(hand_contour)
                cv2.drawContours(frame, [hull], -1, (255, 0, 0), 2)
        
        # Update current gesture
        self.current_gesture = gesture
        self.gesture_confidence = confidence
        
        # Add debug information to frame
        if self.show_debug:
            self.draw_debug_info(frame, gesture, confidence, skin_mask)
        
        return frame, gesture, confidence
    
    def draw_debug_info(self, frame, gesture, confidence, skin_mask=None):
        """Draw debug information on the frame"""
        height, width = frame.shape[:2]
        
        # Gesture info
        gesture_text = f"Gesture: {gesture.value.upper()}"
        confidence_text = f"Confidence: {confidence:.2f}"
        
        # Draw background rectangle for text
        cv2.rectangle(frame, (10, 10), (350, 100), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (350, 100), (255, 255, 255), 2)
        
        # Draw text
        cv2.putText(frame, gesture_text, (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, confidence_text, (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Frame: {self.frame_count}", (20, 85), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Draw gesture indicators
        if gesture == GestureType.JUMP:
            cv2.circle(frame, (width - 80, 60), 30, (0, 0, 255), -1)
            cv2.putText(frame, "JUMP", (width - 110, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif gesture == GestureType.CROUCH:
            cv2.rectangle(frame, (width - 110, 40), (width - 50, 80), (255, 165, 0), -1)
            cv2.putText(frame, "CROUCH", (width - 130, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 2)
        
        # Instructions
        instructions = [
            "Gestures:",
            "Fist = Jump",
            "1 Finger = Crouch",
            "Open Hand = Idle",
            "",
            "Keep hand in view",
            "Good lighting helps"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (20, height - 140 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Show skin mask in corner
        if skin_mask is not None:
            mask_small = cv2.resize(skin_mask, (160, 120))
            mask_colored = cv2.cvtColor(mask_small, cv2.COLOR_GRAY2BGR)
            frame[height-130:height-10, width-170:width-10] = mask_colored
            cv2.rectangle(frame, (width-170, height-130), (width-10, height-10), (255, 255, 255), 1)
            cv2.putText(frame, "Skin Mask", (width-160, height-135), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    def get_gesture_action(self):
        """Get current gesture action with cooldown"""
        current_time = time.time()
        
        # Check if enough time has passed since last gesture action
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None
        
        # Only return action for high-confidence gestures
        if self.gesture_confidence < 0.6:
            return None
        
        # Determine action based on gesture
        if self.current_gesture == GestureType.JUMP:
            self.last_gesture_time = current_time
            return "jump"
        elif self.current_gesture == GestureType.CROUCH:
            self.last_gesture_time = current_time
            return "crouch"
        
        return None
    
    def get_camera_feed(self):
        """Get the current camera frame for display"""
        frame, gesture, confidence = self.process_frame()
        return frame
    
    def is_active(self):
        """Check if gesture control is active"""
        return self.camera_active
    
    def toggle_debug(self):
        """Toggle debug display"""
        self.show_debug = not self.show_debug
        return self.show_debug
    
    def toggle_camera_feed(self):
        """Toggle camera feed display"""
        self.show_camera_feed = not self.show_camera_feed
        return self.show_camera_feed
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.camera_active = False
        print("✓ OpenCV gesture controller cleaned up")

# OpenCV gesture control instance
opencv_gesture_controller = OpenCVGestureController()
