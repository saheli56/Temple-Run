"""
Player class for handling character movement and animation
"""

import cv2
import numpy as np
from config.game_config import *

class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False

    def jump(self):
        """Initiate a jump if the player is on the ground"""
        if not self.is_jumping:
            self.velocity_y = JUMP_SPEED
            self.is_jumping = True

    def update(self):
        """Update player position and apply gravity"""
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        # Check ground collision
        if self.y > PLAYER_START_Y:
            self.y = PLAYER_START_Y
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, frame):
        """Draw the player on the frame"""
        # For now, draw a simple rectangle as the player
        cv2.rectangle(frame, 
                     (int(self.x), int(self.y)), 
                     (int(self.x + self.width), int(self.y + self.height)), 
                     BLUE, 
                     -1)
        return frame

    def get_bounds(self):
        """Get the bounding rectangle of the player"""
        return (int(self.x), int(self.y), self.width, self.height)
