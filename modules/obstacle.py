"""
Obstacle class for handling obstacle generation and movement
"""

import cv2
import numpy as np
import random
from config.game_config import *

class Obstacle:
    def __init__(self):
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.x = WINDOW_WIDTH  # Start from right edge
        self.y = WINDOW_HEIGHT - self.height - 50  # Same level as player
        self.speed = OBSTACLE_SPEED

    def update(self):
        """Update obstacle position"""
        self.x -= self.speed
        return self.x + self.width < 0  # Return True if obstacle is off screen

    def draw(self, frame):
        """Draw the obstacle on the frame"""
        cv2.rectangle(frame, 
                     (int(self.x), int(self.y)), 
                     (int(self.x + self.width), int(self.y + self.height)), 
                     RED, 
                     -1)
        return frame

    def get_bounds(self):
        """Get the bounding rectangle of the obstacle"""
        return (int(self.x), int(self.y), self.width, self.height)

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.spawn_timer = 0

    def update(self, dt):
        """Update all obstacles and spawn new ones"""
        # Update spawn timer
        self.spawn_timer += dt
        if self.spawn_timer >= OBSTACLE_SPAWN_TIME:
            self.obstacles.append(Obstacle())
            self.spawn_timer = 0

        # Update existing obstacles and remove those that are off screen
        self.obstacles = [obs for obs in self.obstacles if not obs.update()]

    def draw(self, frame):
        """Draw all obstacles"""
        for obstacle in self.obstacles:
            frame = obstacle.draw(frame)
        return frame

    def check_collision(self, player_bounds):
        """Check for collisions with player"""
        px, py, pw, ph = player_bounds
        for obstacle in self.obstacles:
            ox, oy, ow, oh = obstacle.get_bounds()
            
            # Simple AABB collision detection
            if (px < ox + ow and 
                px + pw > ox and 
                py < oy + oh and 
                py + ph > oy):
                return True
        return False
