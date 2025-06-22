"""
Enhanced Background with Parallax Scrolling
"""

import cv2
import numpy as np
import os
from config.game_config import *

# Define the path to the assets directory
ASSETS_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets')

class ParallaxBackground:
    def __init__(self):
        self.layers = []
        self.initialize_layers()
        
    def initialize_layers(self):
        """Initialize background layers with different scroll speeds"""
        for i in range(BACKGROUND_LAYERS):
            layer = self.load_layer_image(i) or self.create_layer(i)
            self.layers.append({
                'image': layer,
                'x_offset': 0,
                'speed': BACKGROUND_SPEEDS[i],
                'width': layer.shape[1]
            })
    
    def load_layer_image(self, layer_index):
        """Load high-quality image for a specific layer if available"""
        asset_paths = [
            os.path.join(ASSETS_PATH, 'backgrounds', f'layer_{layer_index}.png'),
            os.path.join(ASSETS_PATH, 'backgrounds', f'layer_{layer_index}.jpg')
        ]
        for path in asset_paths:
            if os.path.exists(path):
                image = cv2.imread(path)
                return cv2.resize(image, (WINDOW_WIDTH * 2, WINDOW_HEIGHT // (layer_index + 1)))
        return None
    
    def create_layer(self, layer_index):
        """Create a procedural background layer"""
        height = WINDOW_HEIGHT
        width = WINDOW_WIDTH * 2  # Make it wider for scrolling
        
        if layer_index == 0:  # Sky layer
            layer = np.full((height//2, width, 3), (200, 150, 100), dtype=np.uint8)
        elif layer_index == 1:  # Mountains/Hills
            layer = np.full((height//3, width, 3), (100, 120, 80), dtype=np.uint8)
            # Add some mountain-like shapes
            for x in range(0, width, 200):
                pts = np.array([[x, height//3], [x+100, height//6], [x+200, height//3]], np.int32)
                cv2.fillPoly(layer, [pts], (80, 100, 60))
        elif layer_index == 2:  # Trees/Forest
            layer = np.full((height//2, width, 3), (60, 80, 40), dtype=np.uint8)
            # Add tree-like shapes
            for x in range(0, width, 50):
                cv2.rectangle(layer, (x+20, height//4), (x+30, height//2), (40, 60, 30), -1)
                cv2.circle(layer, (x+25, height//4), 15, (50, 70, 35), -1)
        else:  # Ground texture layer
            # This layer will be a scrolling texture for the ground.
            # The path will be drawn separately and overlaid.
            layer_height = WINDOW_HEIGHT // 2
            layer = np.full((layer_height, width, 3), GREEN, dtype=np.uint8)
            # Add some slanted lines to give a sense of motion on the grass
            for x_pos in range(0, width, 40):
                cv2.line(layer, (x_pos, 0), (x_pos - 20, layer_height), (0, 180, 0), 3)
        
        return layer
    
    def update(self, dt):
        """Update background scrolling"""
        for layer in self.layers:
            # Use modulo to create an infinite scrolling loop
            layer['x_offset'] = (layer['x_offset'] + layer['speed']) % layer['width']
    
    def draw_path(self, frame):
        """Draws the pseudo-3D path on the frame with gradient effects."""
        path_y_start = WINDOW_HEIGHT // 2
        path_top_width = WINDOW_WIDTH * 0.1
        path_bottom_width = WINDOW_WIDTH * 0.95

        for y in range(path_y_start, WINDOW_HEIGHT):
            progress = (y - path_y_start) / (WINDOW_HEIGHT - path_y_start)
            current_width = path_top_width + (path_bottom_width - path_top_width) * progress

            start_x = int(WINDOW_WIDTH / 2 - current_width / 2)
            end_x = int(WINDOW_WIDTH / 2 + current_width / 2)

            # Gradient effect for the path
            color_intensity = int(100 + 155 * progress)
            path_color = (color_intensity, color_intensity - 20, color_intensity - 40)

            # Draw path segment
            cv2.line(frame, (start_x, y), (end_x, y), path_color, 2)

            # Draw rumble strips on the edges
            if (y // 5) % 2 == 0:
                strip_color = (255, 255, 255)
            else:
                strip_color = (200, 0, 0)
            
            if start_x > 0:
                cv2.circle(frame, (start_x, y), 2, strip_color, -1)
            if end_x < WINDOW_WIDTH:
                cv2.circle(frame, (end_x, y), 2, strip_color, -1)

    def draw(self, frame):
        """Draw all background layers with parallax effect"""
        for i, layer in enumerate(self.layers):
            layer_img = layer['image']
            x_offset = int(layer['x_offset'])
            
            # Calculate vertical position for each layer
            if i == 0:  # Sky
                y_pos = 0
            elif i == 1:  # Mountains
                y_pos = WINDOW_HEIGHT // 4
            elif i == 2:  # Trees
                y_pos = WINDOW_HEIGHT // 2
            else:  # Ground
                y_pos = WINDOW_HEIGHT - layer_img.shape[0]
            
            # Draw the layer with offset
            try:
                # First part
                src_start = x_offset
                src_end = min(x_offset + WINDOW_WIDTH, layer_img.shape[1])
                dst_start = 0
                dst_end = src_end - src_start
                
                if dst_end > 0 and src_end > src_start:
                    layer_section = layer_img[:, src_start:src_end]
                    if y_pos + layer_section.shape[0] <= WINDOW_HEIGHT:
                        frame[y_pos:y_pos + layer_section.shape[0], 
                              dst_start:dst_start + layer_section.shape[1]] = layer_section
                
                # Second part (wrap around)
                if dst_end < WINDOW_WIDTH:
                    remaining_width = WINDOW_WIDTH - dst_end
                    wrap_section = layer_img[:, :remaining_width]
                    if y_pos + wrap_section.shape[0] <= WINDOW_HEIGHT:
                        frame[y_pos:y_pos + wrap_section.shape[0], 
                              dst_end:dst_end + wrap_section.shape[1]] = wrap_section
                        
            except Exception as e:
                # Fallback to solid color if there's an issue
                color = [(200, 150, 100), (100, 120, 80), (60, 80, 40), GREEN][i]
                if i == 0:
                    cv2.rectangle(frame, (0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT//2), color, -1)
                elif i == 1:
                    cv2.rectangle(frame, (0, WINDOW_HEIGHT//4), (WINDOW_WIDTH, WINDOW_HEIGHT//2), color, -1)
                elif i == 2:
                    cv2.rectangle(frame, (0, WINDOW_HEIGHT//2), (WINDOW_WIDTH, 3*WINDOW_HEIGHT//4), color, -1)
                else:
                    cv2.rectangle(frame, (0, 3*WINDOW_HEIGHT//4), (WINDOW_WIDTH, WINDOW_HEIGHT), color, -1)
        
        self.draw_path(frame)
        return frame
