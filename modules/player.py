"""
Enhanced Player class with animation and improved physics
"""

import cv2
import numpy as np
import math
from config.game_config import *

class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False
        self.is_falling = False
        
        # Animation properties
        self.animation_frame = 0.0
        self.animation_speed = PLAYER_ANIMATION_SPEED
        self.running_frames = 4  # Number of running animation frames
        
        # Visual effects
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        
        # Create simple sprite frames (can be replaced with actual sprites)
        self.sprite_frames = self.create_sprite_frames()
        
    def create_sprite_frames(self):
        """Create simple animated sprite frames"""
        frames = []
        for i in range(self.running_frames):
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Body
            body_color = BLUE
            cv2.rectangle(frame, (15, 20), (45, 70), body_color, -1)
            
            # Head
            cv2.circle(frame, (30, 15), 12, body_color, -1)
            
            # Legs (animated)
            leg_offset = int(5 * math.sin(i * math.pi / 2))
            cv2.rectangle(frame, (20 + leg_offset, 70), (25 + leg_offset, 85), body_color, -1)
            cv2.rectangle(frame, (35 - leg_offset, 70), (40 - leg_offset, 85), body_color, -1)
            
            # Arms (animated)
            arm_offset = int(3 * math.cos(i * math.pi / 2))
            cv2.rectangle(frame, (10 + arm_offset, 30), (15 + arm_offset, 50), body_color, -1)
            cv2.rectangle(frame, (45 - arm_offset, 30), (50 - arm_offset, 50), body_color, -1)
            
            frames.append(frame)
        
        return frames
    
    def jump(self):
        """Enhanced jump with better physics"""
        if not self.is_jumping and not self.is_falling:
            self.velocity_y = JUMP_SPEED
            self.is_jumping = True
            return True  # Return True to indicate successful jump
        return False
    
    def update(self, dt):
        """Enhanced update with improved physics"""
        # Update animation
        if not self.is_jumping:
            self.animation_frame += self.animation_speed
            if self.animation_frame >= self.running_frames:
                self.animation_frame = 0
        
        # Apply gravity
        if self.is_jumping or self.is_falling:
            self.velocity_y += GRAVITY
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED
        
        # Update position
        self.y += self.velocity_y
        
        # Ground collision with improved detection
        ground_y = PLAYER_START_Y
        if self.y >= ground_y:
            self.y = ground_y
            if self.velocity_y > 0:  # Was falling
                self.velocity_y = 0
                self.is_jumping = False
                self.is_falling = False
        elif self.velocity_y > 0:  # Moving downward
            self.is_falling = True
    
    def add_screen_shake(self, intensity=CAMERA_SHAKE_INTENSITY):
        """Add screen shake effect"""
        self.shake_offset_x = np.random.randint(-intensity, intensity)
        self.shake_offset_y = np.random.randint(-intensity, intensity)
    
    def update_screen_shake(self, dt):
        """Update screen shake effect"""
        # Gradually reduce shake
        self.shake_offset_x *= 0.9
        self.shake_offset_y *= 0.9
        
        if abs(self.shake_offset_x) < 0.5:
            self.shake_offset_x = 0
        if abs(self.shake_offset_y) < 0.5:
            self.shake_offset_y = 0
    
    def draw(self, frame):
        """Enhanced drawing with animation"""
        # Apply screen shake
        draw_x = int(self.x + self.shake_offset_x)
        draw_y = int(self.y + self.shake_offset_y)
        
        # Get current sprite frame
        if self.is_jumping:
            # Use a specific jump frame (could be different sprite)
            current_frame = self.sprite_frames[1]  # Use frame 1 for jump
        else:
            frame_index = int(self.animation_frame) % len(self.sprite_frames)
            current_frame = self.sprite_frames[frame_index]
        
        # Draw the sprite
        try:
            # Ensure we don't draw outside frame bounds
            sprite_h, sprite_w = current_frame.shape[:2]
            frame_h, frame_w = frame.shape[:2]
            
            # Calculate drawing bounds
            start_x = max(0, draw_x)
            start_y = max(0, draw_y)
            end_x = min(frame_w, draw_x + sprite_w)
            end_y = min(frame_h, draw_y + sprite_h)
            
            # Calculate sprite bounds
            sprite_start_x = max(0, -draw_x)
            sprite_start_y = max(0, -draw_y)
            sprite_end_x = sprite_start_x + (end_x - start_x)
            sprite_end_y = sprite_start_y + (end_y - start_y)
            
            if end_x > start_x and end_y > start_y:
                frame[start_y:end_y, start_x:end_x] = current_frame[sprite_start_y:sprite_end_y, sprite_start_x:sprite_end_x]
                
        except Exception as e:
            # Fallback to simple rectangle
            cv2.rectangle(frame, 
                         (draw_x, draw_y), 
                         (draw_x + self.width, draw_y + self.height), 
                         BLUE, -1)
        
        # Update screen shake
        self.update_screen_shake(1/60)  # Assume 60 FPS for shake decay
        
        return frame
    
    def get_bounds(self):
        """Get collision bounds with shake offset"""
        return (int(self.x + self.shake_offset_x), 
                int(self.y + self.shake_offset_y), 
                self.width, self.height)
    
    def get_center(self):
        """Get center point of player"""
        return (int(self.x + self.width // 2), 
                int(self.y + self.height // 2))
