# Sound Assets

Place your sound files in this directory:

## Required Sound Files:
- `background_music.mp3` - Main background music (loops continuously)
- `jump.wav` - Player jump sound effect
- `gameover.wav` - Game over sound effect
- `coin.wav` - Coin collection sound effect
- `start.wav` - Game start sound effect
- `collision.wav` - Collision/hit sound effect

## File Formats:
- Music: MP3, OGG
- Sound Effects: WAV, OGG

## Volume Levels:
All sounds should be normalized to prevent audio clipping.
Recommended levels:
- Background music: -12dB to -6dB
- Sound effects: -6dB to 0dB

## Free Sound Resources:
- Freesound.org
- Zapsplat.com
- Adobe Audition (built-in samples)
- GarageBand (built-in samples)

## Notes:
The game will run without these files, but no sound will play.
Missing files are handled gracefully with console warnings.
