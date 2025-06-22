"""
Simplified Enhanced Background with Working Parallax System
"""

import cv2
import numpy as np
import os
import math
from config.game_config import *

class ParallaxBackground:
    def __init__(self):
        # Environmental effects
        self.fog_alpha = 0.1
        self.sunlight_intensity = 0.3
        self.wind_offset = 0
        self.time_offset = 0
        
        # Initialize layers
        self.layers = []
        self.initialize_layers()
        
    def initialize_layers(self):
        """Initialize multiple parallax layers for temple/jungle environment"""
        layer_configs = [
            {'name': 'sky', 'speed': 0.2, 'height_ratio': 0.4, 'color': (180, 150, 120)},
            {'name': 'mountains', 'speed': 0.5, 'height_ratio': 0.3, 'color': (120, 100, 80)},
            {'name': 'temples', 'speed': 1.0, 'height_ratio': 0.4, 'color': (100, 90, 80)},
            {'name': 'jungle', 'speed': 2.0, 'height_ratio': 0.5, 'color': (40, 100, 40)},
            {'name': 'trees', 'speed': 4.0, 'height_ratio': 0.6, 'color': (30, 60, 30)},
            {'name': 'ground', 'speed': 6.0, 'height_ratio': 0.3, 'color': (20, 80, 20)}
        ]
        
        for i, config in enumerate(layer_configs):
            layer_image = self.create_simple_layer(i, config)
            self.layers.append({
                'image': layer_image,
                'x_offset': 0,
                'speed': config['speed'],
                'width': layer_image.shape[1],
                'name': config['name'],
                'height_ratio': config['height_ratio']
            })
    
    def create_simple_layer(self, layer_index, config):
        """Create simple but effective background layers"""
        width = WINDOW_WIDTH * 3  # Wide for seamless scrolling
        height = int(WINDOW_HEIGHT * config['height_ratio'])
        base_color = config['color']
        
        # Create base layer
        layer = np.full((height, width, 3), base_color, dtype=np.uint8)
        
        if config['name'] == 'sky':
            # Gradient sky
            for y in range(height):
                ratio = y / height
                color = (int(base_color[0] + 50 * ratio), 
                        int(base_color[1] + 30 * ratio), 
                        int(base_color[2] + 10 * ratio))
                layer[y, :] = color
            
            # Add simple clouds
            for i in range(8):
                cloud_x = (i * width // 6) % width
                cloud_y = int(height * 0.3)
                cv2.ellipse(layer, (cloud_x, cloud_y), (60, 20), 0, 0, 360, (255, 255, 255), -1)
        
        elif config['name'] == 'mountains':
            # Create mountain silhouettes
            points = []
            for x in range(0, width + 200, 150):
                peak_height = int(height * (0.3 + 0.4 * math.sin(x * 0.01)))
                points.extend([(x, height), (x + 75, height - peak_height), (x + 150, height)])
            
            if len(points) >= 3:
                mountain_points = np.array(points, dtype=np.int32)
                cv2.fillPoly(layer, [mountain_points], (90, 80, 70))
        
        elif config['name'] == 'temples':
            # Add temple structures
            for i in range(4):
                temple_x = i * width // 3
                temple_width = 80 + i * 15
                temple_height = int(height * 0.7)
                
                # Main structure
                cv2.rectangle(layer, 
                             (temple_x, height - temple_height), 
                             (temple_x + temple_width, height),
                             (80, 70, 60), -1)
                
                # Add simple details
                cv2.rectangle(layer, 
                             (temple_x + 10, height - temple_height + 20), 
                             (temple_x + temple_width - 10, height - 10),
                             (50, 50, 50), -1)
        
        elif config['name'] == 'jungle':
            # Create jungle canopy texture
            for x in range(0, width, 40):
                for y in range(0, height, 30):
                    # Vary colors slightly
                    color_var = np.random.randint(-20, 20, 3)
                    tree_color = np.clip(np.array(base_color) + color_var, 0, 255)
                    
                    radius = np.random.randint(15, 25)
                    cv2.circle(layer, (x, y), radius, (int(tree_color[0]), int(tree_color[1]), int(tree_color[2])), -1)
        
        elif config['name'] == 'trees':
            # Create tree trunks
            for i in range(15):
                trunk_x = (i * width // 10) % width
                trunk_width = 8
                cv2.rectangle(layer, 
                             (trunk_x, 0), 
                             (trunk_x + trunk_width, height),
                             (25, 15, 10), -1)
        
        else:  # ground
            # Add grass texture
            for x in range(0, width, 3):
                grass_height = np.random.randint(3, height // 3)
                grass_color = (20 + np.random.randint(0, 15), 
                              60 + np.random.randint(0, 30), 
                              20 + np.random.randint(0, 15))
                cv2.line(layer, (x, height), (x, height - grass_height), grass_color, 1)
        
        return layer
    
    def update(self, dt):
        """Update background scrolling and animations"""
        self.time_offset += dt
        self.wind_offset = math.sin(self.time_offset * 0.5) * 2
        
        for layer in self.layers:
            # Apply wind effect to vegetation layers
            wind_factor = 1.0
            if 'trees' in layer['name'] or 'ground' in layer['name']:
                wind_factor = 1.0 + self.wind_offset * 0.05
            
            # Update scrolling with wind effect
            layer['x_offset'] = (layer['x_offset'] + layer['speed'] * wind_factor) % layer['width']
    
    def draw_enhanced_path(self, frame):
        """Draw enhanced 3D temple path"""
        height, width = frame.shape[:2]
        path_start_y = height // 2
        
        # Path configuration for temple run effect
        path_top_width = width * 0.08
        path_bottom_width = width * 0.85
        
        for y in range(path_start_y, height):
            progress = (y - path_start_y) / (height - path_start_y)
            current_width = path_top_width + (path_bottom_width - path_top_width) * progress
            
            # Calculate path edges
            center_x = width // 2
            left_edge = int(center_x - current_width / 2)
            right_edge = int(center_x + current_width / 2)
            
            # Stone path color with depth shading
            base_intensity = 100 + int(80 * progress)
            path_color = (base_intensity - 20, base_intensity - 10, base_intensity)
            
            # Draw main path
            if left_edge >= 0 and right_edge < width:
                cv2.line(frame, (left_edge, y), (right_edge, y), path_color, 1)
            
            # Add stone block texture
            if y % 20 == 0 and current_width > 30:
                block_color = (base_intensity - 40, base_intensity - 30, base_intensity - 20)
                cv2.line(frame, (left_edge, y), (right_edge, y), block_color, 1)
            
            # Add path edges
            edge_color = (60, 50, 40)
            if left_edge > 0:
                cv2.circle(frame, (left_edge, y), 1, edge_color, -1)
            if right_edge < width:
                cv2.circle(frame, (right_edge, y), 1, edge_color, -1)
        
        return frame
    
    def draw(self, frame):
        """Draw all background layers with enhanced parallax effect"""
        # Clear frame
        frame.fill(0)
        
        # Draw layers from back to front
        for i, layer in enumerate(self.layers):
            layer_img = layer['image']
            x_offset = int(layer['x_offset'])
            
            # Calculate vertical position based on layer type
            layer_height = layer_img.shape[0]
            if layer['name'] == 'sky':
                y_pos = 0
            elif layer['name'] == 'mountains':
                y_pos = int(WINDOW_HEIGHT * 0.2)
            elif layer['name'] == 'temples':
                y_pos = int(WINDOW_HEIGHT * 0.3)
            elif layer['name'] == 'jungle':
                y_pos = int(WINDOW_HEIGHT * 0.25)
            elif layer['name'] == 'trees':
                y_pos = int(WINDOW_HEIGHT * 0.4)
            else:  # ground
                y_pos = WINDOW_HEIGHT - layer_height
            
            # Ensure y_pos is valid
            if y_pos + layer_height > WINDOW_HEIGHT:
                y_pos = WINDOW_HEIGHT - layer_height
            if y_pos < 0:
                y_pos = 0
            
            try:
                # Draw seamless scrolling layer
                self.draw_layer_section(frame, layer_img, x_offset, y_pos)
            except Exception as e:
                # Fallback to solid color
                fallback_colors = [
                    (180, 150, 120),  # sky
                    (120, 100, 80),   # mountains
                    (100, 90, 80),    # temples
                    (40, 100, 40),    # jungle
                    (30, 60, 30),     # trees
                    (20, 80, 20)      # ground
                ]
                color = fallback_colors[min(i, len(fallback_colors) - 1)]
                cv2.rectangle(frame, (0, y_pos), (WINDOW_WIDTH, y_pos + layer_height), color, -1)
        
        # Draw the enhanced temple path
        frame = self.draw_enhanced_path(frame)
        
        return frame
    
    def draw_layer_section(self, frame, layer_img, x_offset, y_pos):
        """Draw a section of a layer with seamless wrapping"""
        layer_height, layer_width = layer_img.shape[:2]
        frame_height, frame_width = frame.shape[:2]
        
        # Ensure we don't exceed frame boundaries
        draw_height = min(layer_height, frame_height - y_pos)
        if draw_height <= 0:
            return
        
        # First section
        section_width = min(frame_width, layer_width - x_offset)
        if section_width > 0:
            src_section = layer_img[:draw_height, x_offset:x_offset + section_width]
            frame[y_pos:y_pos + draw_height, :section_width] = src_section
        
        # Wrap-around section if needed
        if section_width < frame_width:
            remaining_width = frame_width - section_width
            wrap_width = min(remaining_width, layer_width)
            if wrap_width > 0:
                wrap_section = layer_img[:draw_height, :wrap_width]
                frame[y_pos:y_pos + draw_height, section_width:section_width + wrap_width] = wrap_section
