"""
Keyboard-based Gesture Simulation for Temple Run Game
This provides gesture control functionality without requiring MediaPipe
"""

import cv2
import numpy as np
import time
from enum import Enum

class GestureType(Enum):
    """Enumeration of recognized gestures"""
    IDLE = "idle"
    JUMP = "jump"
    CROUCH = "crouch"
    UNKNOWN = "unknown"

class KeyboardGestureController:
    """
    Keyboard-based gesture simulation controller
    This allows testing gesture functionality without MediaPipe/camera
    """
    
    def __init__(self):
        print("⌨️ Initializing keyboard gesture simulation...")
        
        # Gesture state
        self.current_gesture = GestureType.IDLE
        self.gesture_confidence = 1.0
        self.gesture_history = []
        self.history_size = 5
        
        # Timing for gesture actions
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.5
        
        # Camera simulation
        self.camera_active = True  # Always active for keyboard simulation
        self.show_debug = True
        self.show_camera_feed = False  # No actual camera feed
        
        # Keyboard gesture mapping
        self.gesture_keys = {
            'F': GestureType.JUMP,      # F = Fist gesture
            'I': GestureType.CROUCH,    # I = Index finger gesture  
            'O': GestureType.IDLE       # O = Open palm gesture
        }
        
        print("✓ Keyboard gesture controller initialized")
        print("💡 Gesture Keys: F=Fist(Jump), I=Index(Crouch), O=Open(Idle)")
    
    def initialize_camera(self, camera_index=0):
        """Initialize the simulated camera (always successful)"""
        print("✓ Keyboard gesture simulation ready (no camera needed)")
        self.camera_active = True
        return True
    
    def set_gesture_from_key(self, key):
        """Set current gesture based on keyboard input"""
        key_upper = key.upper()
        if key_upper in self.gesture_keys:
            self.current_gesture = self.gesture_keys[key_upper]
            self.gesture_confidence = 1.0
            print(f"🤲 Gesture simulated: {self.current_gesture.value.upper()}")
            return True
        return False
    
    def recognize_gesture(self, landmarks=None):
        """Simulate gesture recognition (always returns current gesture)"""
        return self.current_gesture, self.gesture_confidence
    
    def smooth_gesture(self, gesture, confidence):
        """Smooth gesture recognition using history"""
        # Add to history
        self.gesture_history.append((gesture, confidence))
        
        # Keep only recent history
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)
        
        # Return the most recent gesture (keyboard input is already smooth)
        return gesture, confidence
    
    def process_frame(self):
        """Process simulated frame (no actual camera processing)"""
        if not self.camera_active:
            return None, GestureType.IDLE, 0.0
        
        # Create a simple visualization frame
        frame = self.create_visualization_frame()
        
        return frame, self.current_gesture, self.gesture_confidence
    
    def create_visualization_frame(self):
        """Create a visualization frame showing current gesture"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add background
        frame[:] = (20, 20, 40)  # Dark blue background
        
        # Add title
        cv2.putText(frame, "KEYBOARD GESTURE SIMULATION", (120, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add current gesture display
        gesture_text = f"Current Gesture: {self.current_gesture.value.upper()}"
        cv2.putText(frame, gesture_text, (150, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Add confidence
        confidence_text = f"Confidence: {self.gesture_confidence:.2f}"
        cv2.putText(frame, confidence_text, (200, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Add gesture indicators
        if self.current_gesture == GestureType.JUMP:
            cv2.circle(frame, (320, 300), 60, (0, 0, 255), -1)
            cv2.putText(frame, "JUMP", (280, 310), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        elif self.current_gesture == GestureType.CROUCH:
            cv2.rectangle(frame, (260, 270), (380, 330), (255, 165, 0), -1)
            cv2.putText(frame, "CROUCH", (270, 310), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        elif self.current_gesture == GestureType.IDLE:
            cv2.rectangle(frame, (260, 270), (380, 330), (0, 255, 0), 3)
            cv2.putText(frame, "IDLE", (290, 310), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add instructions
        instructions = [
            "Keyboard Controls:",
            "F = Fist (Jump)",
            "I = Index Finger (Crouch)", 
            "O = Open Palm (Idle)",
            "",
            "Press keys during gameplay"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (50, 380 + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        return frame
    
    def get_gesture_action(self):
        """Get current gesture action with cooldown"""
        current_time = time.time()
        
        # Check if enough time has passed since last gesture action
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None
        
        # Only return action for non-idle gestures
        if self.current_gesture == GestureType.JUMP:
            self.last_gesture_time = current_time
            return "jump"
        elif self.current_gesture == GestureType.CROUCH:
            self.last_gesture_time = current_time
            return "crouch"
        
        return None
    
    def get_camera_feed(self):
        """Get the current visualization frame"""
        return self.create_visualization_frame()
    
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
        cv2.destroyAllWindows()
        self.camera_active = False
        print("✓ Keyboard gesture controller cleaned up")

# Create the controller instance
keyboard_gesture_controller = KeyboardGestureController()
