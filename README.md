# Temple Run CV - Enhanced Edition

An advanced Temple Run-style endless runner game implemented using Python, OpenCV, and Pygame with semi-3D visual effects and enhanced gameplay mechanics.

## 🎮 Features

### Core Gameplay
- **Endless running** with increasing difficulty
- **Enhanced jump mechanics** with realistic gravity physics
- **Obstacle avoidance** with varied obstacle types (rocks, fire)
- **Coin collection** system with animated coins
- **Score tracking** with persistent high scores
- **Lives system** with visual hearts display

### Visual Effects
- **Parallax scrolling background** with multiple layers for depth
- **Semi-3D obstacle scaling** that creates perspective effects
- **Screen shake** and flash effects on collision
- **Animated character sprites** with running animation
- **Particle effects** for enhanced visual feedback
- **Gradient backgrounds** and lighting effects

### Audio System
- **Background music** support
- **Sound effects** for jumping, coin collection, and collisions
- **Volume control** for music and effects

### Advanced Features
- **Multiple game states** (Menu, Playing, Paused, Game Over)
- **High score persistence** with JSON storage
- **Camera effects** including shake and motion blur
- **Optimized rendering** at 60 FPS
- **Modular code architecture** for easy expansion

## 🛠️ Requirements

- Python 3.8+
- OpenCV (opencv-python-headless)
- Pygame
- NumPy
- MediaPipe (optional, for future gesture controls)

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/saheli56/Temple-Run.git
   cd Temple-Run
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 How to Play

### Basic Controls
- **SPACE**: Jump over obstacles
- **P**: Pause/Resume game
- **Q**: Quit game
- **S**: Restart game (when game over)

### Game Objective
1. Run as far as possible while avoiding obstacles
2. Collect coins to increase your score
3. Survive as long as possible as the game speeds up
4. Beat your high score!

### Game Elements
- **Blue Runner**: Your character (animated)
- **Red/Gray Obstacles**: Avoid these or game over
- **Yellow Coins**: Collect for bonus points
- **Green Ground**: Safe running surface

## 🏗️ Project Structure

```
Temple Run Game Dev/
├── main.py                 # Main game loop (original)
├── main_enhanced.py        # Enhanced game with all features
├── config/
│   └── game_config.py     # Game configuration and constants
├── modules/
│   ├── player.py          # Enhanced player class with animation
│   ├── obstacle.py        # Obstacle and coin management
│   ├── background.py      # Parallax background system
│   └── ui.py             # User interface and menus
├── utils/
│   └── game_utils.py     # Utility functions and sound manager
├── assets/
│   ├── backgrounds/      # Background images (add your own)
│   ├── sprites/          # Character and object sprites
│   └── sounds/           # Sound effects and music
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Running the Game

### Basic Version
```bash
python main.py
```

### Enhanced Version (Recommended)
```bash
python main_enhanced.py
```

## 🎨 Customization

### Adding Your Own Assets

1. **Background Images**: Place in `assets/backgrounds/`
2. **Character Sprites**: Place in `assets/sprites/`
3. **Sound Effects**: Place in `assets/sounds/`

### Modifying Game Settings

Edit `config/game_config.py` to adjust:
- Window size and FPS
- Player physics (gravity, jump speed)
- Obstacle spawn rate and speed
- Colors and visual effects
- Sound volume levels

### Adding New Features

The modular architecture makes it easy to add:
- New obstacle types in `modules/obstacle.py`
- Additional animations in `modules/player.py`
- More background layers in `modules/background.py`
- Enhanced UI elements in `modules/ui.py`

## 🎮 Game Mechanics

### Difficulty Progression
- Game speed increases over time
- More frequent obstacle spawning
- Varied obstacle types and patterns

### Scoring System
- **Distance**: Points for time survived
- **Coins**: Bonus points for collection
- **Speed Multiplier**: Higher speeds = more points

### Visual Effects
- **Parallax Scrolling**: Creates depth illusion
- **3D Scaling**: Obstacles grow as they approach
- **Camera Shake**: Impact feedback
- **Screen Flash**: Collision indication

## 🔧 Development

### Code Structure
- **Object-Oriented Design**: Each game element is a class
- **State Management**: Clean separation of game states
- **Event-Driven**: Responsive input handling
- **Modular Components**: Easy to modify and extend

### Performance Optimization
- **Efficient Rendering**: Optimized OpenCV operations
- **Memory Management**: Proper cleanup of game objects
- **Frame Rate Control**: Consistent 60 FPS gameplay
- **Asset Streaming**: Load assets as needed

## 🐛 Troubleshooting

### Common Issues

1. **OpenCV Window Issues**:
   - Use `opencv-python-headless` instead of `opencv-python`
   - Ensure Pygame is properly initialized

2. **Sound Not Working**:
   - Check if sound files exist in `assets/sounds/`
   - Verify Pygame mixer initialization

3. **Performance Issues**:
   - Lower FPS in `game_config.py`
   - Reduce number of background layers
   - Disable screen effects

### System Requirements
- **Windows**: Tested on Windows 10/11
- **macOS**: Should work with minor adjustments
- **Linux**: Fully supported

## 🚀 Future Enhancements

### Planned Features
- **Hand Gesture Controls** using MediaPipe
- **Multiple Characters** with different abilities
- **Power-ups** and special items
- **Achievement System** with unlockables
- **Online Leaderboards** for score sharing
- **Mobile Touch Controls** for broader accessibility

### Advanced Graphics
- **Shader Effects** for better lighting
- **Particle Systems** for environmental effects
- **Dynamic Weather** system
- **Day/Night Cycle** with lighting changes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by the original Temple Run mobile game
- Built with Python, OpenCV, and Pygame
- Sound effects and music assets (add your own)
- Community feedback and contributions

---

**Enjoy playing Temple Run CV Enhanced Edition!** 🎮

For questions, issues, or feature requests, please open an issue on GitHub.
