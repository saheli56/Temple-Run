# Temple Run Sound System Documentation

## 🎵 Overview

The Temple Run CV game features a comprehensive sound system built with `pygame.mixer` that includes:

- **Background Music**: Looping ambient music during gameplay
- **Sound Effects**: Jump, coin collection, collision, game over, and start sounds
- **Mute Controls**: Toggle sound effects and music independently or together
- **Volume Control**: Separate volume controls for music and sound effects
- **Error Handling**: Graceful fallback when sound files are missing

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install pygame opencv-python numpy
```

### 2. Sound File Requirements

Place your sound files in the `assets/sounds/` directory:

```
assets/sounds/
├── background_music.mp3    # Main background music (loops)
├── jump.wav               # Player jump sound
├── coin.wav               # Coin collection sound  
├── collision.wav          # Collision/hit sound
├── gameover.wav          # Game over sound
└── start.wav             # Game start sound
```

### 3. Supported Audio Formats

- **Music**: MP3, OGG, WAV
- **Sound Effects**: WAV, OGG (recommended for best compatibility)

## 🎮 Controls

| Key | Action |
|-----|--------|
| `M` | Toggle all audio (mute/unmute) |
| `SPACE` | Jump (plays jump sound) |
| `P` | Pause (pauses music) |

## 🔊 Sound Events

### Automatic Sound Triggers

1. **Game Start**: Plays `start.wav` when game begins
2. **Jump**: Plays `jump.wav` when player jumps (prevents overlap)
3. **Coin Collection**: Plays `coin.wav` when collecting coins
4. **Collision**: Plays `collision.wav` + `gameover.wav` on collision
5. **Background Music**: Loops `background_music.mp3` continuously

### Volume Levels

- **Sound Effects**: 70% volume (configurable via `SOUND_VOLUME`)
- **Background Music**: 50% volume (configurable via `MUSIC_VOLUME`)
- **Collision/Game Over**: Slightly reduced volume to prevent harsh sounds

## 🛠 Technical Features

### Sound Manager Features

- **Prevent Overlap**: Jump sounds won't overlap for cleaner audio
- **Volume Control**: Individual volume settings for each sound type
- **Fade Effects**: Background music fades in when starting
- **Pause/Resume**: Music pauses when game is paused
- **Error Recovery**: Missing sound files are handled gracefully
- **Status Tracking**: Real-time sound system status monitoring

### Performance Optimizations

- **Pre-loading**: All sounds loaded once at startup
- **Efficient Mixing**: Optimized pygame mixer settings
- **Channel Management**: Smart audio channel allocation
- **Memory Management**: Proper cleanup of audio resources

## 🧪 Testing

### Run the Sound Tester

```bash
python test_sounds.py
```

This interactive tester allows you to:
- Test individual sound effects
- Toggle mute functionality
- Check sound system status
- Verify all audio files are loading correctly

### Test Commands

1. `1` - Test jump sound
2. `2` - Test coin sound  
3. `3` - Test collision sound
4. `4` - Test game over sound
5. `5` - Test start sound
6. `m` - Toggle mute
7. `s` - Show system status
8. `q` - Quit tester

## 🎨 UI Integration

The game HUD displays:
- **Sound Status**: 🔊 (unmuted) / 🔇 MUTED (muted)
- **Controls Hint**: Shows available keyboard shortcuts
- **Real-time Updates**: Status changes immediately when toggling mute

## 🔍 Troubleshooting

### Common Issues

1. **No Sound Playing**
   - Check if sound files exist in `assets/sounds/`
   - Verify pygame mixer is initialized
   - Check system audio settings

2. **Poor Audio Quality**
   - Use WAV files for sound effects
   - Ensure proper audio normalization
   - Check mixer frequency settings (22050 Hz)

3. **Sound Lag**
   - Reduce buffer size in mixer settings
   - Use shorter sound files
   - Optimize sound file formats

### Debug Information

The sound system provides console output:
- ✓ Success messages for loaded sounds
- ⚠ Warning messages for missing files
- 🔇 Mute status changes
- 🎵 Music playback status

## 📁 File Structure

```
Temple-Run/
├── assets/sounds/          # Sound files directory
│   ├── README.md          # Sound assets documentation
│   ├── background_music.mp3
│   ├── jump.wav
│   ├── coin.wav
│   ├── collision.wav
│   ├── gameover.wav
│   └── start.wav
├── config/
│   └── game_config.py     # Sound configuration
├── utils/
│   └── game_utils.py      # SoundManager class
├── modules/
│   └── ui.py             # UI with sound status
├── main_enhanced.py       # Main game with sound integration
└── test_sounds.py         # Sound testing utility
```
## 🎯 Advanced Features

### Custom Sound Settings

Edit `config/game_config.py` to customize:

```python
# Volume levels (0.0 to 1.0)
SOUND_VOLUME = 0.7
MUSIC_VOLUME = 0.5

# Enable/disable sound systems
ENABLE_SOUND_EFFECTS = True
ENABLE_BACKGROUND_MUSIC = True
```

### Adding New Sounds

1. Add sound file to `assets/sounds/`
2. Update `SOUND_FILES` in `game_config.py`
3. Load sound in `init_sounds()` method
4. Use `sound_manager.play_sound('new_sound')` in game logic

## 🎪 Free Sound Resources

- [Freesound.org](https://freesound.org) - Free sound effects
- [Zapsplat.com](https://zapsplat.com) - Professional sound library
- [Adobe Audition](https://adobe.com/audition) - Built-in sound samples
- [GarageBand](https://apple.com/garageband) - Built-in loops and sounds

## 📄 License

Sound system code is part of the Temple Run CV project. 
Individual sound files may have their own licenses - check with sound providers.
