"""
Hand Gesture Control Module for Temple Run Game
Uses MediaPipe for real-time hand tracking and gesture recognition
"""

import cv2
import numpy as np
import math
import time
from enum import Enum

# Try to import MediaPipe with fallback
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    print("⚠ Warning: MediaPipe not available. Gesture control will be disabled.")
    MEDIAPIPE_AVAILABLE = False
    mp = None

class GestureType(Enum):
    """Enumeration of recognized gestures"""
    IDLE = "idle"
    JUMP = "jump"
    CROUCH = "crouch"
    UNKNOWN = "unknown"

class HandGestureController:
    def __init__(self):
        if not MEDIAPIPE_AVAILABLE:
            print("❌ MediaPipe not available - gesture control disabled")
            self.mp_hands = None
            self.hands = None
            self.mp_drawing = None
            self.camera_active = False
            return
            
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,  # Only track one hand for simplicity
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Camera setup
        self.cap = None
        self.camera_active = False
        
        # Gesture recognition parameters
        self.current_gesture = GestureType.IDLE
        self.gesture_confidence = 0.0
        self.gesture_history = []
        self.history_size = 5  # Number of frames to smooth over
        
        # Gesture thresholds and parameters
        self.fist_threshold = 0.03  # Distance threshold for closed fist
        self.finger_threshold = 0.05  # Distance threshold for extended fingers
        self.gesture_stability_frames = 3  # Frames needed for stable gesture
        
        # Timing for gesture actions
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.5  # Minimum time between gesture actions
          # Debug and display options
        self.show_debug = True
        self.show_camera_feed = True
        
        print("✓ Hand gesture controller initialized")
    
    def initialize_camera(self, camera_index=0):
        """Initialize the webcam"""
        if not MEDIAPIPE_AVAILABLE:
            print("⚠ Warning: Cannot initialize camera - MediaPipe not available")
            return False
            
        try:
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                print(f"⚠ Warning: Could not open camera {camera_index}")
                return False
            
            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.camera_active = True
            print("✓ Camera initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Error initializing camera: {e}")
            return False
    
    def calculate_finger_distances(self, landmarks):
        """Calculate distances between finger tips and palm center"""
        if not landmarks:
            return None
        
        # Palm center (approximately wrist landmark)
        palm_center = landmarks[0]  # Wrist landmark
        
        # Finger tip landmarks (thumb, index, middle, ring, pinky)
        finger_tips = [4, 8, 12, 16, 20]
        
        distances = []
        for tip_id in finger_tips:
            tip = landmarks[tip_id]
            distance = math.sqrt(
                (tip.x - palm_center.x) ** 2 + 
                (tip.y - palm_center.y) ** 2
            )
            distances.append(distance)
        
        return distances
    
    def recognize_gesture(self, landmarks):
        """Recognize gesture based on hand landmarks"""
        if not landmarks:
            return GestureType.UNKNOWN, 0.0
        
        # Calculate finger distances from palm
        finger_distances = self.calculate_finger_distances(landmarks)
        if not finger_distances:
            return GestureType.UNKNOWN, 0.0
        
        # Count extended fingers
        extended_fingers = sum(1 for dist in finger_distances if dist > self.finger_threshold)
        
        # Calculate average distance (for fist detection)
        avg_distance = sum(finger_distances) / len(finger_distances)
        
        # Gesture recognition logic
        confidence = 0.0
        
        if avg_distance < self.fist_threshold:
            # Closed fist = JUMP
            gesture = GestureType.JUMP
            confidence = 1.0 - (avg_distance / self.fist_threshold)
            
        elif extended_fingers == 1 and finger_distances[1] > self.finger_threshold:
            # Only index finger extended = CROUCH
            gesture = GestureType.CROUCH
            confidence = 0.8 if finger_distances[1] > finger_distances[0] else 0.6
            
        elif extended_fingers >= 4:
            # Open palm = IDLE
            gesture = GestureType.IDLE
            confidence = min(extended_fingers / 5.0, 1.0)
            
        else:
            # Ambiguous gesture
            gesture = GestureType.UNKNOWN
            confidence = 0.3
        
        return gesture, confidence
    
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
        if not MEDIAPIPE_AVAILABLE or not self.camera_active or not self.cap:
            return None, GestureType.IDLE, 0.0
        
        ret, frame = self.cap.read()
        if not ret:
            return None, GestureType.IDLE, 0.0
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = self.hands.process(rgb_frame)
        
        gesture = GestureType.IDLE
        confidence = 0.0
        
        if results.multi_hand_landmarks:
            # Get first hand landmarks
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Recognize gesture
            raw_gesture, raw_confidence = self.recognize_gesture(hand_landmarks.landmark)
            
            # Apply smoothing
            gesture, confidence = self.smooth_gesture(raw_gesture, raw_confidence)
            
            # Draw hand landmarks on frame
            if self.show_debug:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
        
        # Update current gesture
        self.current_gesture = gesture
        self.gesture_confidence = confidence
        
        # Add debug information to frame
        if self.show_debug:
            self.draw_debug_info(frame, gesture, confidence)
        
        return frame, gesture, confidence
    
    def draw_debug_info(self, frame, gesture, confidence):
        """Draw debug information on the frame"""
        height, width = frame.shape[:2]
        
        # Gesture info
        gesture_text = f"Gesture: {gesture.value.upper()}"
        confidence_text = f"Confidence: {confidence:.2f}"
        
        # Draw background rectangle for text
        cv2.rectangle(frame, (10, 10), (300, 80), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (300, 80), (255, 255, 255), 2)
        
        # Draw text
        cv2.putText(frame, gesture_text, (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, confidence_text, (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Draw gesture indicators
        if gesture == GestureType.JUMP:
            cv2.circle(frame, (width - 60, 60), 30, (0, 0, 255), -1)
            cv2.putText(frame, "JUMP", (width - 90, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif gesture == GestureType.CROUCH:
            cv2.rectangle(frame, (width - 90, 40), (width - 30, 80), (255, 165, 0), -1)
            cv2.putText(frame, "CROUCH", (width - 110, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 2)
        
        # Instructions
        instructions = [
            "Gestures:",
            "Fist = Jump",
            "Index finger = Crouch",
            "Open palm = Idle"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (20, height - 80 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def get_gesture_action(self):
        """Get current gesture action with cooldown"""
        current_time = time.time()
        
        # Check if enough time has passed since last gesture action
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None
        
        # Only return action for high-confidence gestures
        if self.gesture_confidence < 0.7:
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
        print("✓ Gesture controller cleaned up")

# Gesture control instance
gesture_controller = HandGestureController()
