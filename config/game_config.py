"""
Enhanced Temple Run Game Configuration
"""

import os

# Window Configuration
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
WINDOW_TITLE = "Temple Run CV - Enhanced Edition"

# Game Configuration
FPS = 60
GRAVITY = 0.6
JUMP_SPEED = -18
MAX_FALL_SPEED = 15

# Colors (BGR format for OpenCV)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 255)

# Player Configuration
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 90
PLAYER_START_X = 150
PLAYER_START_Y = WINDOW_HEIGHT - PLAYER_HEIGHT - 100
PLAYER_ANIMATION_SPEED = 0.15

# Obstacle Configuration
OBSTACLE_BASE_SPEED = 8
OBSTACLE_SPEED_INCREMENT = 0.1
OBSTACLE_SPAWN_TIME = 1.5
OBSTACLE_MIN_GAP = 300
OBSTACLE_MAX_GAP = 500

# Parallax Background Layers
BACKGROUND_LAYERS = 4
BACKGROUND_SPEEDS = [1, 2, 4, 6]  # Different scroll speeds for depth

# Coin Configuration
COIN_SPAWN_CHANCE = 0.3
COIN_VALUE = 10
COIN_ANIMATION_SPEED = 0.2

# Sound Configuration
SOUND_VOLUME = 0.7
MUSIC_VOLUME = 0.5

# Camera Effects
CAMERA_SHAKE_INTENSITY = 5
CAMERA_SHAKE_DURATION = 0.3

# Asset Paths
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR, "backgrounds")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# Game States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_PAUSED = "paused"
