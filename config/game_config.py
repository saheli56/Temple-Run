"""
Game configuration constants
"""

# Window Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Temple Run CV"

# Game Configuration
FPS = 30
GRAVITY = 0.8
JUMP_SPEED = -15

# Colors (BGR format for OpenCV)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)

# Player Configuration
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
PLAYER_START_X = 100
PLAYER_START_Y = WINDOW_HEIGHT - PLAYER_HEIGHT - 50  # 50 pixels above bottom

# Obstacle Configuration
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 80
OBSTACLE_SPEED = 5
OBSTACLE_SPAWN_TIME = 2  # seconds between spawns
