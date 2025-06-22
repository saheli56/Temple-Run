"""
Enhanced Obstacle system with 3D effects and coins
"""

import cv2
import numpy as np
import random
import math
from config.game_config import *

class Obstacle:
    def __init__(self, obstacle_type="rock"):
        self.type = obstacle_type
        self.base_width = 50
        self.base_height = 60
        self.x = WINDOW_WIDTH  # Start from right edge
        self.distance = 1.0  # Distance from camera (1.0 = far, 0.0 = very close)
        self.speed = OBSTACLE_BASE_SPEED
        self.color = RED if obstacle_type == "fire" else (100, 100, 100)  # Gray for rocks
        
        # Calculate initial position
        self.update_scale_and_position()
        
    def update_scale_and_position(self):
        """Update size and position based on distance (3D effect)"""
        # Scale factor based on distance (closer = bigger)
        scale_factor = 2.0 - self.distance  # Range: 1.0 to 2.0
        
        self.width = int(self.base_width * scale_factor)
        self.height = int(self.base_height * scale_factor)
        
        # Y position gets lower as obstacle gets closer (perspective effect)
        base_y = WINDOW_HEIGHT - 150
        self.y = int(base_y - (scale_factor - 1.0) * 50)
        
    def update(self, dt, speed_multiplier=1.0):
        """Update obstacle position with 3D scaling effect"""
        # Move obstacle towards camera
        move_distance = self.speed * speed_multiplier * dt * 60  # Normalize for framerate
        self.x -= move_distance
        
        # Update distance based on X position (simulate 3D approach)
        progress = (WINDOW_WIDTH - self.x) / WINDOW_WIDTH  # 0.0 to 1.0+
        self.distance = max(0.1, 1.0 - progress)  # Closer as it moves left
        
        # Update scale and position
        self.update_scale_and_position()
        
        # Return True if obstacle is off screen
        return self.x + self.width < 0
    
    def draw(self, frame):
        """Draw obstacle with 3D perspective effect"""
        try:
            if self.type == "fire":
                # Animated fire effect
                flame_height = self.height + int(10 * math.sin(cv2.getTickCount() / 1000))
                # Draw flame with gradient effect
                for i in range(0, flame_height, 5):
                    intensity = int(255 * (1 - i / flame_height))
                    color = (0, max(0, intensity), 255)  # Red to yellow gradient
                    cv2.rectangle(frame,
                                (int(self.x), int(self.y + i)),
                                (int(self.x + self.width), int(self.y + i + 7)),
                                color, -1)
            else:
                # Rock obstacle with shading
                # Main body
                cv2.rectangle(frame,
                            (int(self.x), int(self.y)),
                            (int(self.x + self.width), int(self.y + self.height)),
                            self.color, -1)
                
                # Add highlight for 3D effect
                highlight_color = tuple(min(255, c + 50) for c in self.color)
                cv2.rectangle(frame,
                            (int(self.x), int(self.y)),
                            (int(self.x + self.width//3), int(self.y + self.height//3)),
                            highlight_color, -1)
                
                # Add shadow
                shadow_color = tuple(max(0, c - 30) for c in self.color)
                cv2.rectangle(frame,
                            (int(self.x + 2*self.width//3), int(self.y + 2*self.height//3)),
                            (int(self.x + self.width), int(self.y + self.height)),
                            shadow_color, -1)
        except:
            # Fallback drawing
            cv2.rectangle(frame,
                        (int(self.x), int(self.y)),
                        (int(self.x + self.width), int(self.y + self.height)),
                        self.color, -1)
        
        return frame
    
    def get_bounds(self):
        """Get collision bounds"""
        return (int(self.x), int(self.y), self.width, self.height)

class Coin:
    def __init__(self):
        self.x = WINDOW_WIDTH + random.randint(0, 200)
        self.y = WINDOW_HEIGHT - random.randint(100, 200)
        self.width = 30
        self.height = 30
        self.speed = OBSTACLE_BASE_SPEED * 0.8  # Slightly slower than obstacles
        self.rotation = 0
        self.scale_factor = 1.0
        self.collected = False
        
    def update(self, dt, speed_multiplier=1.0):
        """Update coin position and animation"""
        if not self.collected:
            # Move coin
            self.x -= self.speed * speed_multiplier * dt * 60
            
            # Animate rotation and scaling
            self.rotation += 5
            self.scale_factor = 1.0 + 0.2 * math.sin(cv2.getTickCount() / 500)
            
            # Floating effect
            self.y += math.sin(cv2.getTickCount() / 300) * 0.5
            
        return self.x + self.width < 0
    
    def draw(self, frame):
        """Draw animated coin"""
        if not self.collected:
            # Calculate actual size with scaling
            actual_size = int(self.width * self.scale_factor)
            center_x = int(self.x + self.width // 2)
            center_y = int(self.y + self.height // 2)
            
            # Draw rotating coin (ellipse that changes width based on rotation)
            rotation_factor = abs(math.cos(math.radians(self.rotation)))
            ellipse_width = int(actual_size * rotation_factor)
            
            if ellipse_width > 5:  # Only draw if visible
                cv2.ellipse(frame,
                          (center_x, center_y),
                          (ellipse_width // 2, actual_size // 2),
                          0, 0, 360,
                          YELLOW, -1)
                
                # Add shine effect
                cv2.ellipse(frame,
                          (center_x - ellipse_width//4, center_y - actual_size//4),
                          (ellipse_width // 4, actual_size // 4),
                          0, 0, 360,
                          WHITE, -1)
        
        return frame
    
    def get_bounds(self):
        """Get collision bounds"""
        return (int(self.x), int(self.y), self.width, self.height)
    
    def collect(self):
        """Mark coin as collected"""
        self.collected = True

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.coins = []
        self.obstacle_spawn_timer = 0
        self.coin_spawn_timer = 0
        self.speed_multiplier = 1.0
        self.score = 0
        
    def update(self, dt):
        """Update all obstacles and coins"""
        # Increase difficulty over time
        self.speed_multiplier = 1.0 + (self.score / 1000) * 0.1
        
        # Update obstacle spawn timer
        self.obstacle_spawn_timer += dt
        adjusted_spawn_time = OBSTACLE_SPAWN_TIME / self.speed_multiplier
        
        if self.obstacle_spawn_timer >= adjusted_spawn_time:
            obstacle_type = random.choice(["rock", "fire"])
            self.obstacles.append(Obstacle(obstacle_type))
            self.obstacle_spawn_timer = 0
        
        # Update coin spawn timer
        self.coin_spawn_timer += dt
        if self.coin_spawn_timer >= 1.0 and random.random() < COIN_SPAWN_CHANCE:
            self.coins.append(Coin())
            self.coin_spawn_timer = 0
        
        # Update existing obstacles
        self.obstacles = [obs for obs in self.obstacles 
                         if not obs.update(dt, self.speed_multiplier)]
        
        # Update existing coins
        self.coins = [coin for coin in self.coins 
                     if not coin.update(dt, self.speed_multiplier)]
        
        # Increase score based on time survived
        self.score += dt * 10 * self.speed_multiplier
    
    def draw(self, frame):
        """Draw all obstacles and coins"""
        # Draw obstacles (back to front for proper layering)
        sorted_obstacles = sorted(self.obstacles, key=lambda x: x.distance, reverse=True)
        for obstacle in sorted_obstacles:
            frame = obstacle.draw(frame)
        
        # Draw coins
        for coin in self.coins:
            frame = coin.draw(frame)
        
        return frame
    
    def check_collision(self, player_bounds):
        """Check for collisions with obstacles"""
        px, py, pw, ph = player_bounds
        for obstacle in self.obstacles:
            ox, oy, ow, oh = obstacle.get_bounds()
            
            # AABB collision detection with some tolerance
            if (px < ox + ow - 5 and 
                px + pw > ox + 5 and 
                py < oy + oh - 5 and 
                py + ph > oy + 5):
                return True
        return False
    
    def check_coin_collection(self, player_bounds):
        """Check for coin collection and return collected coins"""
        px, py, pw, ph = player_bounds
        collected_coins = 0
        
        for coin in self.coins:
            if not coin.collected:
                cx, cy, cw, ch = coin.get_bounds()
                
                # Check collision
                if (px < cx + cw and 
                    px + pw > cx and 
                    py < cy + ch and 
                    py + ph > cy):
                    coin.collect()
                    collected_coins += 1
        
        return collected_coins
    
    def get_score(self):
        """Get current score"""
        return int(self.score)
