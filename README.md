# Temple Run CV

A Temple Run-style endless runner game implemented using Python, OpenCV, and Pygame.

## Features

- Endless running gameplay
- Jump mechanics with gravity
- Obstacle avoidance
- Score tracking
- OpenCV-based graphics
- Pygame sound system (to be implemented)

## Requirements

- Python 3.8+
- OpenCV (cv2)
- Pygame
- NumPy

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```
   python main.py
   ```
2. Controls:
   - Spacebar: Jump
   - Q: Quit game

## Project Structure

- `main.py`: Game loop and control flow
- `modules/`: Game components
  - `player.py`: Character class and movement
  - `obstacle.py`: Obstacle generation and collision
- `config/`: Game settings
- `utils/`: Helper functions
- `assets/`: Game resources (images, sounds)

## Future Enhancements

- Add character sprites and animations
- Implement sound effects
- Add hand gesture controls using OpenCV
- Add power-ups and varying obstacles
- Implement high score system
