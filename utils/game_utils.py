"""
Utility functions for the game
"""

import cv2
import numpy as np
from config.game_config import *

def init_pygame_mixer():
    """Initialize Pygame mixer for sound"""
    import pygame
    pygame.mixer.init()
    return pygame.mixer

def draw_score(frame, score):
    """Draw score on the frame"""
    score_text = f"Score: {score}"
    cv2.putText(frame, 
                score_text, 
                (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                WHITE, 
                2)
    return frame

def create_background():
    """Create a simple background"""
    background = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
    # Draw ground
    cv2.rectangle(background,
                 (0, WINDOW_HEIGHT - 50),
                 (WINDOW_WIDTH, WINDOW_HEIGHT),
                 GREEN,
                 -1)
    return background
