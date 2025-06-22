"""
Enhanced utility functions for the Temple Run game
"""

import cv2
import numpy as np
import pygame
import json
import os
from config.game_config import *

def init_pygame_mixer():
    """Initialize Pygame mixer for sound with better settings"""
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    return pygame.mixer

def load_high_score():
    """Load high score from file"""
    try:
        if os.path.exists("high_score.json"):
            with open("high_score.json", "r") as f:
                data = json.load(f)
                return data.get("high_score", 0), data.get("total_coins", 0)
    except:
        pass
    return 0, 0

def save_high_score(score, total_coins):
    """Save high score to file"""
    try:
        data = {"high_score": score, "total_coins": total_coins}
        with open("high_score.json", "w") as f:
            json.dump(data, f)
    except:
        pass

def create_gradient_background(width, height, color1, color2, direction="vertical"):
    """Create a gradient background"""
    background = np.zeros((height, width, 3), dtype=np.uint8)
    
    if direction == "vertical":
        for y in range(height):
            ratio = y / height
            color = [int(c1 * (1 - ratio) + c2 * ratio) for c1, c2 in zip(color1, color2)]
            background[y, :] = color
    else:  # horizontal
        for x in range(width):
            ratio = x / width
            color = [int(c1 * (1 - ratio) + c2 * ratio) for c1, c2 in zip(color1, color2)]
            background[:, x] = color
    
    return background

def apply_screen_shake(image, intensity):
    """Apply screen shake effect to an image"""
    if intensity <= 0:
        return image
    
    shake_x = np.random.randint(-intensity, intensity)
    shake_y = np.random.randint(-intensity, intensity)
    
    # Create transformation matrix
    M = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
    
    # Apply transformation
    shaken = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    
    return shaken

def add_motion_blur(image, intensity=5):
    """Add motion blur effect"""
    if intensity <= 0:
        return image
    
    # Create motion blur kernel
    kernel = np.zeros((intensity, intensity))
    kernel[intensity//2, :] = np.ones(intensity)
    kernel = kernel / intensity
    
    # Apply blur
    blurred = cv2.filter2D(image, -1, kernel)
    return blurred

def create_particle_effect(frame, center, num_particles=10, color=WHITE):
    """Create particle explosion effect"""
    for _ in range(num_particles):
        # Random position around center
        offset_x = np.random.randint(-20, 20)
        offset_y = np.random.randint(-20, 20)
        particle_pos = (center[0] + offset_x, center[1] + offset_y)
        
        # Random size
        size = np.random.randint(2, 6)
        
        # Draw particle
        cv2.circle(frame, particle_pos, size, color, -1)
    
    return frame

def interpolate_color(color1, color2, ratio):
    """Interpolate between two colors"""
    return tuple(int(c1 * (1 - ratio) + c2 * ratio) for c1, c2 in zip(color1, color2))

def create_glowing_text(text, font_size=36, glow_color=(255, 255, 0), text_color=(255, 255, 255)):
    """Create glowing text effect using pygame"""
    font = pygame.font.Font(None, font_size)
    
    # Create text surface
    text_surface = font.render(text, True, text_color)
    
    # Create glow effect (multiple renders with offset)
    glow_surface = pygame.Surface((text_surface.get_width() + 20, text_surface.get_height() + 20))
    glow_surface.fill((0, 0, 0))
    glow_surface.set_colorkey((0, 0, 0))
    
    # Render glow
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if dx != 0 or dy != 0:
                glow_text = font.render(text, True, glow_color)
                glow_surface.blit(glow_text, (10 + dx, 10 + dy))
    
    # Render main text on top
    glow_surface.blit(text_surface, (10, 10))
    
    return glow_surface

def calculate_3d_position(x, z, camera_distance=500):
    """Calculate 2D screen position from 3D world position"""
    # Simple perspective projection
    screen_x = x
    scale = camera_distance / (camera_distance + z)
    
    return int(screen_x), scale

def create_road_perspective(width, height, road_width=200):
    """Create a perspective road effect"""
    road = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Fill background
    road[:] = GREEN
    
    # Draw road with perspective
    for y in range(height):
        # Calculate road width at this Y position (perspective effect)
        perspective_ratio = y / height
        current_road_width = int(road_width * (0.3 + 0.7 * perspective_ratio))
        
        # Calculate road position (centered)
        road_left = width // 2 - current_road_width // 2
        road_right = width // 2 + current_road_width // 2
        
        # Draw road surface
        road[y, road_left:road_right] = (139, 69, 19)  # Brown road
        
        # Draw road markings
        if y % 40 < 20 and current_road_width > 20:  # Dashed lines
            center_line_start = width // 2 - 2
            center_line_end = width // 2 + 2
            road[y, center_line_start:center_line_end] = WHITE
    
    return road

def ease_in_out(t):
    """Easing function for smooth animations"""
    return t * t * (3.0 - 2.0 * t)

def clamp(value, min_val, max_val):
    """Clamp a value between min and max"""
    return max(min_val, min(max_val, value))

class SoundManager:
    """Enhanced sound management"""
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        
    def load_sound(self, name, filepath):
        """Load a sound file"""
        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(SOUND_VOLUME)
            self.sounds[name] = sound
        except:
            # Create placeholder sound if file doesn't exist
            self.sounds[name] = None
    
    def play_sound(self, name):
        """Play a sound effect"""
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
    
    def play_music(self, filepath, loop=-1):
        """Play background music"""
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(loop)
            self.music_playing = True
        except:
            pass
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.music_playing = False

# Global sound manager instance
sound_manager = SoundManager()
