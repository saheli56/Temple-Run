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
    """Enhanced sound management with mute functionality and better error handling"""
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.sound_muted = False
        self.music_muted = False
        self.current_music_file = None
        self.sound_channels = {}
        
        # Initialize pygame mixer if not already done
        self.init_mixer()
        
    def init_mixer(self):
        """Initialize pygame mixer with optimal settings"""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.init()
            print("✓ Sound system initialized successfully")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize sound system: {e}")
        
    def load_sound(self, name, filepath):
        """Load a sound file with error handling"""
        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(SOUND_VOLUME)
                self.sounds[name] = sound
                print(f"✓ Loaded sound: {name}")
            else:
                print(f"⚠ Warning: Sound file not found: {filepath}")
                self.sounds[name] = None
        except Exception as e:
            print(f"⚠ Warning: Could not load sound {name}: {e}")
            self.sounds[name] = None
    
    def play_sound(self, name, volume=None, prevent_overlap=False):
        """Play a sound effect with advanced options"""
        if self.sound_muted or name not in self.sounds or not self.sounds[name]:
            return None
            
        try:
            sound = self.sounds[name]
            
            # Stop previous instance if preventing overlap
            if prevent_overlap and name in self.sound_channels:
                if self.sound_channels[name].get_busy():
                    self.sound_channels[name].stop()
            
            # Set custom volume if provided
            if volume is not None:
                sound.set_volume(volume)
            
            # Play sound and store channel reference
            channel = sound.play()
            if channel:
                self.sound_channels[name] = channel
            
            return channel
        except Exception as e:
            print(f"⚠ Warning: Could not play sound {name}: {e}")
            return None
    
    def play_music(self, filepath, loop=-1, fade_in=0):
        """Play background music with fade-in option"""
        if self.music_muted:
            return
            
        try:
            if os.path.exists(filepath):
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(MUSIC_VOLUME)
                
                if fade_in > 0:
                    pygame.mixer.music.play(loop, fade_ms=fade_in)
                else:
                    pygame.mixer.music.play(loop)
                
                self.music_playing = True
                self.current_music_file = filepath
                print(f"✓ Playing music: {os.path.basename(filepath)}")
            else:
                print(f"⚠ Warning: Music file not found: {filepath}")
        except Exception as e:
            print(f"⚠ Warning: Could not play music: {e}")
    
    def stop_music(self, fade_out=0):
        """Stop background music with optional fade-out"""
        try:
            if fade_out > 0:
                pygame.mixer.music.fadeout(fade_out)
            else:
                pygame.mixer.music.stop()
            
            self.music_playing = False
            self.current_music_file = None
        except Exception as e:
            print(f"⚠ Warning: Could not stop music: {e}")
    
    def pause_music(self):
        """Pause background music"""
        try:
            pygame.mixer.music.pause()
        except Exception as e:
            print(f"⚠ Warning: Could not pause music: {e}")
    
    def resume_music(self):
        """Resume paused music"""
        try:
            pygame.mixer.music.unpause()
        except Exception as e:
            print(f"⚠ Warning: Could not resume music: {e}")
    
    def toggle_sound_mute(self):
        """Toggle sound effects mute"""
        self.sound_muted = not self.sound_muted
        status = "muted" if self.sound_muted else "unmuted"
        print(f"🔇 Sound effects {status}")
        return self.sound_muted
    
    def toggle_music_mute(self):
        """Toggle music mute"""
        self.music_muted = not self.music_muted
        
        if self.music_muted:
            pygame.mixer.music.set_volume(0)
            print("🔇 Music muted")
        else:
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            print("🔊 Music unmuted")
        
        return self.music_muted
    
    def toggle_all_mute(self):
        """Toggle all audio mute"""
        # If either is unmuted, mute both
        if not self.sound_muted or not self.music_muted:
            self.sound_muted = True
            self.music_muted = True
            pygame.mixer.music.set_volume(0)
            print("🔇 All audio muted")
            return True
        else:
            self.sound_muted = False
            self.music_muted = False
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            print("🔊 All audio unmuted")
            return False
    
    def set_sound_volume(self, volume):
        """Set master sound effects volume (0.0 to 1.0)"""
        volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(volume)
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)
    
    def is_music_playing(self):
        """Check if music is currently playing"""
        return pygame.mixer.music.get_busy() and self.music_playing
    
    def get_sound_status(self):
        """Get current sound system status"""
        return {
            'sound_muted': self.sound_muted,
            'music_muted': self.music_muted,
            'music_playing': self.is_music_playing(),
            'current_music': os.path.basename(self.current_music_file) if self.current_music_file else None,
            'loaded_sounds': list(self.sounds.keys())
        }

# Global sound manager instance
sound_manager = SoundManager()
