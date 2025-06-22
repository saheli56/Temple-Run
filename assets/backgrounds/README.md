# Temple Run Background Assets

This directory contains the background layer images for the Temple Run game's parallax scrolling system.

## Layer Structure

The background system uses 6 parallax layers to create depth and immersion:

### Layer 0: Sky
- **File**: `temple_layer_0.png` or `jungle_layer_0.png`
- **Speed**: 0.2x (slowest)
- **Content**: Sky, clouds, sun rays
- **Dimensions**: 3072x307 pixels (3x window width)

### Layer 1: Distant Mountains
- **File**: `temple_layer_1.png` or `jungle_layer_1.png`
- **Speed**: 0.5x
- **Content**: Mountain silhouettes, atmospheric perspective
- **Dimensions**: 3072x230 pixels

### Layer 2: Temple Ruins
- **File**: `temple_layer_2.png` or `jungle_layer_2.png`
- **Speed**: 1.0x
- **Content**: Ancient temple structures, ruins
- **Dimensions**: 3072x307 pixels

### Layer 3: Jungle Canopy
- **File**: `temple_layer_3.png` or `jungle_layer_3.png`
- **Speed**: 2.0x
- **Content**: Dense jungle canopy, tree tops
- **Dimensions**: 3072x384 pixels

### Layer 4: Foreground Trees
- **File**: `temple_layer_4.png` or `jungle_layer_4.png`
- **Speed**: 4.0x
- **Content**: Tree trunks, large vegetation
- **Dimensions**: 3072x461 pixels

### Layer 5: Ground Vegetation
- **File**: `temple_layer_5.png` or `jungle_layer_5.png`
- **Speed**: 6.0x (fastest)
- **Content**: Ground-level plants, grass, details
- **Dimensions**: 3072x230 pixels

## Image Requirements

### File Formats
- **Preferred**: PNG (for transparency support)
- **Alternative**: JPG (for smaller file sizes)

### Dimensions
- **Width**: 3072 pixels (3x game window width for seamless scrolling)
- **Height**: Variable based on layer (see above)

### Design Guidelines

1. **Seamless Tiling**: Images must tile seamlessly horizontally
2. **Color Palette**: Use jungle/temple theme colors:
   - Earth tones: browns, tans, ochres
   - Jungle greens: various shades of green
   - Stone colors: grays, sandy browns
   - Sky colors: blues, warm sunset tones

3. **Depth Cues**:
   - Distant layers: lighter, more muted colors
   - Close layers: darker, more saturated colors
   - Atmospheric perspective: add slight blue/gray tint to distant elements

4. **Detail Level**:
   - Slower layers: less detail, larger elements
   - Faster layers: more detail, smaller elements

## Procedural Fallback

If image files are not found, the system will generate procedural backgrounds with:
- Gradient skies with clouds
- Stylized mountain silhouettes
- Temple structure outlines
- Jungle canopy textures
- Tree trunk patterns
- Ground vegetation details

## Creating Your Own Assets

### Recommended Tools
- **GIMP** (free)
- **Photoshop**
- **Krita** (free)
- **Blender** (for 3D elements)

### Workflow
1. Create base layer at 3072x768 resolution
2. Design elements with temple/jungle theme
3. Ensure seamless horizontal tiling
4. Export layers at appropriate heights
5. Test in-game for proper scrolling

### Free Resources
- [OpenGameArt.org](https://opengameart.org/)
- [Kenney.nl](https://kenney.nl/assets)
- [Freepik](https://freepik.com/) (with attribution)
- [Unsplash](https://unsplash.com/) (for photo references)

## Performance Notes

- Large images may impact performance on lower-end systems
- Consider using JPG for layers without transparency
- Optimize images for web/game use
- Test frame rate with all layers active

## Example File Structure

```
assets/backgrounds/
├── temple_layer_0.png    # Sky layer
├── temple_layer_1.png    # Mountains
├── temple_layer_2.png    # Temple ruins
├── temple_layer_3.png    # Jungle canopy
├── temple_layer_4.png    # Foreground trees
└── temple_layer_5.png    # Ground vegetation
```

The game will automatically detect and load these files when present, falling back to procedural generation if not found.
