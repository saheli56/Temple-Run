"""
Enhanced Parallax Background with High-Resolution Temple/Jungle Environment
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
          # Temple/jungle colors (BGR format for OpenCV)
        self.jungle_palette = {
            'sky': (235, 206, 135),      # Sky blue (BGR)
            'distant_mountains': (120, 131, 139),  # Gray-brown mountains (BGR)
            'jungle_canopy': (34, 139, 34),  # Forest green (BGR)
            'temple_stone': (96, 116, 139),  # Sandy brown (BGR)
            'path': (95, 130, 160),      # Brown path (BGR)
            'fog': (220, 220, 220),      # White fog (BGR)
            'sunlight': (186, 223, 255)  # Warm sunlight (BGR)
        }
        
        # Initialize layers after setting up palette
        self.layers = []
        self.initialize_layers()
        
    def initialize_layers(self):
        """Initialize multiple parallax layers for temple/jungle environment"""
        layer_configs = [
            {'name': 'sky', 'speed': 0.2, 'height_ratio': 0.4},
            {'name': 'distant_mountains', 'speed': 0.5, 'height_ratio': 0.3},
            {'name': 'temple_ruins', 'speed': 1.0, 'height_ratio': 0.4},
            {'name': 'jungle_canopy', 'speed': 2.0, 'height_ratio': 0.5},
            {'name': 'foreground_trees', 'speed': 4.0, 'height_ratio': 0.6},
            {'name': 'ground_vegetation', 'speed': 6.0, 'height_ratio': 0.3}
        ]
        
        for i, config in enumerate(layer_configs):
            layer_image = self.load_layer_image(i) or self.create_detailed_layer(i, config)
            self.layers.append({
                'image': layer_image,
                'x_offset': 0,
                'speed': config['speed'],
                'width': layer_image.shape[1],
                'name': config['name'],
                'height_ratio': config['height_ratio']
            })
    
    def load_layer_image(self, layer_index):
        """Load high-quality image for a specific layer"""
        backgrounds_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'backgrounds')
        layer_files = [
            f'temple_layer_{layer_index}.png',
            f'jungle_layer_{layer_index}.png',
            f'layer_{layer_index}.png',
            f'layer_{layer_index}.jpg'
        ]
        
        for filename in layer_files:
            path = os.path.join(backgrounds_dir, filename)
            if os.path.exists(path):
                try:
                    image = cv2.imread(path)
                    if image is not None:
                        # Resize to appropriate dimensions
                        target_width = WINDOW_WIDTH * 3  # Wide for seamless scrolling
                        target_height = int(WINDOW_HEIGHT * 0.8)  # Appropriate height
                        return cv2.resize(image, (target_width, target_height))
                except Exception as e:
                    print(f"Warning: Could not load background image {filename}: {e}")
        return None
    
    def create_detailed_layer(self, layer_index, config):
        """Create detailed procedural background layers"""
        width = WINDOW_WIDTH * 3  # Wide for seamless scrolling
        height = int(WINDOW_HEIGHT * config['height_ratio'])
        layer = np.zeros((height, width, 3), dtype=np.uint8)
        
        if config['name'] == 'sky':
            return self.create_sky_layer(width, height)
        elif config['name'] == 'distant_mountains':
            return self.create_mountain_layer(width, height)
        elif config['name'] == 'temple_ruins':
            return self.create_temple_layer(width, height)
        elif config['name'] == 'jungle_canopy':
            return self.create_jungle_canopy_layer(width, height)
        elif config['name'] == 'foreground_trees':
            return self.create_foreground_trees_layer(width, height)
        elif config['name'] == 'ground_vegetation':
            return self.create_ground_vegetation_layer(width, height)
        
        return layer
    
    def create_sky_layer(self, width, height):
        """Create animated sky with clouds and sunlight"""
        layer = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Gradient sky
        for y in range(height):
            ratio = y / height
            sky_color = np.array(self.jungle_palette['sky'])
            horizon_color = np.array([255, 248, 220])  # Light horizon
            color = sky_color * (1 - ratio) + horizon_color * ratio
            layer[y, :] = color.astype(np.uint8)
        
        # Add clouds
        for i in range(8):
            cloud_x = (i * width // 6) % width
            cloud_y = int(height * 0.2 + np.sin(i) * height * 0.1)
            self.draw_cloud(layer, cloud_x, cloud_y, 40 + i * 5)
        
        # Add sun rays
        sun_x, sun_y = width // 4, height // 4
        self.draw_sun_rays(layer, sun_x, sun_y)
        
        return layer
    
    def create_mountain_layer(self, width, height):
        """Create distant mountain silhouettes"""
        layer = np.full((height, width, 3), self.jungle_palette['distant_mountains'], dtype=np.uint8)
        
        # Create mountain peaks
        points = []
        for x in range(0, width + 200, 150):
            peak_height = int(height * (0.3 + 0.4 * np.sin(x * 0.01)))
            points.extend([(x, height), (x + 75, height - peak_height), (x + 150, height)])
        
        if len(points) >= 3:
            mountain_points = np.array(points, dtype=np.int32)
            cv2.fillPoly(layer, [mountain_points], self.jungle_palette['distant_mountains'])
            
            # Add atmospheric perspective
            fog_overlay = np.full_like(layer, self.jungle_palette['fog'], dtype=np.uint8)
            layer = cv2.addWeighted(layer, 0.7, fog_overlay, 0.3, 0)
        
        return layer
    
    def create_temple_layer(self, width, height):
        """Create ancient temple ruins"""
        layer = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create temple structures
        for i in range(4):
            temple_x = i * width // 3
            temple_width = 100 + i * 20
            temple_height = int(height * (0.6 + 0.2 * np.sin(i)))
            
            # Main structure
            cv2.rectangle(layer, 
                         (temple_x, height - temple_height), 
                         (temple_x + temple_width, height),
                         self.jungle_palette['temple_stone'], -1)
            
            # Add temple details
            self.add_temple_details(layer, temple_x, height - temple_height, temple_width, temple_height)
        
        # Add vines and overgrowth
        self.add_temple_overgrowth(layer, width, height)
        
        return layer
    
    def create_jungle_canopy_layer(self, width, height):
        """Create dense jungle canopy"""
        layer = np.full((height, width, 3), self.jungle_palette['jungle_canopy'], dtype=np.uint8)
        
        # Create tree canopy texture
        for x in range(0, width, 30):
            for y in range(0, height, 25):
                # Vary tree colors
                tree_color = np.array(self.jungle_palette['jungle_canopy'])
                variation = np.random.randint(-30, 30, 3)
                tree_color = np.clip(tree_color + variation, 0, 255)
                
                # Draw tree cluster
                radius = np.random.randint(15, 25)
                cv2.circle(layer, (x + np.random.randint(-10, 10), y), radius, tuple(tree_color.astype(int)), -1)
        
        # Add light filtering through canopy
        self.add_canopy_lighting(layer, width, height)
        
        return layer
    
    def create_foreground_trees_layer(self, width, height):
        """Create foreground tree trunks and branches"""
        layer = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create tree trunks
        for i in range(12):
            trunk_x = (i * width // 8) % width
            trunk_width = np.random.randint(8, 15)
            trunk_color = (40, 25, 15)  # Dark brown
            
            # Draw trunk
            cv2.rectangle(layer, 
                         (trunk_x, 0), 
                         (trunk_x + trunk_width, height),
                         trunk_color, -1)
            
            # Add bark texture
            for y in range(0, height, 20):
                cv2.line(layer, (trunk_x, y), (trunk_x + trunk_width, y + 5), (60, 40, 25), 2)
        
        return layer
    
    def create_ground_vegetation_layer(self, width, height):
        """Create ground-level vegetation and details"""
        layer = np.full((height, width, 3), (20, 60, 20), dtype=np.uint8)  # Dark green base
        
        # Add grass and small plants
        for x in range(0, width, 5):
            grass_height = np.random.randint(5, height // 2)
            grass_color = (30 + np.random.randint(-10, 20), 
                          80 + np.random.randint(-20, 20), 
                          30 + np.random.randint(-10, 10))
            
            # Draw grass blade
            cv2.line(layer, (x, height), (x + np.random.randint(-2, 2), height - grass_height), 
                    grass_color, 1)
          # Add small details like rocks and flowers
        for i in range(width // 50):
            detail_x = np.random.randint(0, width)
            detail_y = np.random.randint(height // 2, height)
            
            if np.random.random() < 0.3:  # Flower
                cv2.circle(layer, (int(detail_x), int(detail_y)), 3, (150, 100, 255), -1)  # BGR format
            else:  # Rock
                cv2.circle(layer, (int(detail_x), int(detail_y)), 5, (100, 100, 100), -1)
        
        return layer
    
    def draw_cloud(self, layer, x, y, size):
        """Draw a cloud on the layer"""
        cloud_color = (255, 255, 255)  # White in BGR
        # Main cloud body
        cv2.circle(layer, (int(x), int(y)), int(size), cloud_color, -1)
        cv2.circle(layer, (int(x + size//2), int(y)), int(size//2), cloud_color, -1)
        cv2.circle(layer, (int(x - size//2), int(y)), int(size//2), cloud_color, -1)
        cv2.circle(layer, (int(x), int(y - size//3)), int(size//3), cloud_color, -1)
    def draw_sun_rays(self, layer, sun_x, sun_y):
        """Draw sun rays"""
        ray_color = self.jungle_palette['sunlight']
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            end_x = int(sun_x + 100 * math.cos(rad))
            end_y = int(sun_y + 100 * math.sin(rad))
            cv2.line(layer, (int(sun_x), int(sun_y)), (end_x, end_y), ray_color, 2)
    
    def add_temple_details(self, layer, x, y, width, height):
        """Add details to temple structures"""
        # Add pillars
        pillar_width = width // 6
        for i in range(3):
            pillar_x = x + i * width // 3 + pillar_width
            cv2.rectangle(layer, (pillar_x, y), (pillar_x + pillar_width, y + height), 
                         (120, 100, 80), -1)
        
        # Add entrance
        entrance_width = width // 3
        entrance_height = height // 2
        entrance_x = x + width // 3
        entrance_y = y + height - entrance_height
        cv2.rectangle(layer, (entrance_x, entrance_y), 
                     (entrance_x + entrance_width, entrance_y + entrance_height),
                     (50, 50, 50), -1)
    
    def add_temple_overgrowth(self, layer, width, height):
        """Add vines and vegetation growing on temples"""
        vine_color = (34, 100, 34)  # Dark green
        for i in range(20):
            vine_x = np.random.randint(0, width)
            vine_length = np.random.randint(height // 4, height)
            
            # Draw vine
            for j in range(0, vine_length, 5):
                vine_y = height - j
                offset = int(10 * math.sin(j * 0.1))
                cv2.circle(layer, (vine_x + offset, vine_y), 2, vine_color, -1)
    
    def add_canopy_lighting(self, layer, width, height):
        """Add dappled light filtering through jungle canopy"""
        light_spots = np.random.randint(0, width, 30)
        for spot_x in light_spots:
            spot_y = np.random.randint(0, height)
            spot_size = np.random.randint(10, 30)
            
            # Create light spot with gradient
            light_overlay = np.zeros_like(layer)
            cv2.circle(light_overlay, (spot_x, spot_y), spot_size, (50, 50, 30), -1)
            layer = cv2.addWeighted(layer, 0.9, light_overlay, 0.1, 0)
    
    def update(self, dt):
        """Update background scrolling and animations"""
        self.time_offset += dt
        self.wind_offset = math.sin(self.time_offset * 0.5) * 2
        
        for layer in self.layers:
            # Apply wind effect to vegetation layers
            wind_factor = 1.0
            if 'vegetation' in layer['name'] or 'trees' in layer['name']:
                wind_factor = 1.0 + self.wind_offset * 0.1
            
            # Update scrolling with wind effect
            layer['x_offset'] = (layer['x_offset'] + layer['speed'] * wind_factor) % layer['width']
    
    def draw_atmospheric_effects(self, frame):
        """Add atmospheric effects like fog and lighting"""
        height, width = frame.shape[:2]
        
        # Add depth fog
        fog_overlay = np.full((height, width, 3), self.jungle_palette['fog'], dtype=np.uint8)
        
        # Apply fog gradient (more fog in distance)
        for y in range(height):
            fog_intensity = (y / height) * self.fog_alpha
            if fog_intensity > 0:
                frame[y] = cv2.addWeighted(frame[y], 1 - fog_intensity, 
                                         fog_overlay[y], fog_intensity, 0)
        
        # Add sunlight filtering
        sun_overlay = np.full((height, width, 3), self.jungle_palette['sunlight'], dtype=np.uint8)
        frame = cv2.addWeighted(frame, 1 - self.sunlight_intensity, 
                               sun_overlay, self.sunlight_intensity, 0)
        
        return frame
    
    def draw_enhanced_path(self, frame):
        """Draw enhanced 3D temple path with stone texture"""
        height, width = frame.shape[:2]
        path_start_y = height // 2
        
        # Path configuration for temple run effect
        path_top_width = width * 0.08
        path_bottom_width = width * 0.9
        
        for y in range(path_start_y, height):
            progress = (y - path_start_y) / (height - path_start_y)
            current_width = path_top_width + (path_bottom_width - path_top_width) * progress
            
            # Calculate path edges
            center_x = width // 2
            left_edge = int(center_x - current_width / 2)
            right_edge = int(center_x + current_width / 2)
            
            # Stone path color with depth shading
            base_intensity = 120 + int(100 * progress)
            path_color = (base_intensity - 20, base_intensity - 10, base_intensity)
            
            # Draw main path
            if left_edge >= 0 and right_edge < width:
                cv2.line(frame, (left_edge, y), (right_edge, y), path_color, 1)
            
            # Add stone block texture
            if y % 15 == 0:  # Stone block lines
                block_color = (base_intensity - 40, base_intensity - 30, base_intensity - 20)
                cv2.line(frame, (left_edge, y), (right_edge, y), block_color, 1)
            
            # Add path edges with ancient stone effect
            edge_color = (80, 70, 60)  # Dark stone edges
            if left_edge > 0:
                cv2.circle(frame, (left_edge, y), 2, edge_color, -1)
            if right_edge < width:
                cv2.circle(frame, (right_edge, y), 2, edge_color, -1)
            
            # Add center line occasionally
            if y % 30 == 0 and current_width > 50:
                cv2.line(frame, (center_x - 1, y), (center_x + 1, y), (150, 140, 130), 2)
        
        return frame
    
    def draw(self, frame):
        """Draw all background layers with enhanced parallax effect"""
        # Clear frame with sky color
        frame.fill(0)
        
        # Draw layers from back to front
        for i, layer in enumerate(self.layers):
            layer_img = layer['image']
            x_offset = int(layer['x_offset'])
            
            # Calculate vertical position based on layer type
            layer_height = layer_img.shape[0]
            if layer['name'] == 'sky':
                y_pos = 0
            elif layer['name'] == 'distant_mountains':
                y_pos = int(WINDOW_HEIGHT * 0.2)
            elif layer['name'] == 'temple_ruins':
                y_pos = int(WINDOW_HEIGHT * 0.3)
            elif layer['name'] == 'jungle_canopy':
                y_pos = int(WINDOW_HEIGHT * 0.25)
            elif layer['name'] == 'foreground_trees':
                y_pos = int(WINDOW_HEIGHT * 0.4)
            else:  # ground_vegetation
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
                    self.jungle_palette['sky'],
                    self.jungle_palette['distant_mountains'],
                    self.jungle_palette['temple_stone'],
                    self.jungle_palette['jungle_canopy'],
                    (40, 60, 40),  # Dark green for trees
                    (20, 60, 20)   # Ground vegetation
                ]
                color = fallback_colors[min(i, len(fallback_colors) - 1)]
                cv2.rectangle(frame, (0, y_pos), (WINDOW_WIDTH, y_pos + layer_height), color, -1)
        
        # Add atmospheric effects
        frame = self.draw_atmospheric_effects(frame)
        
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
        
        # Wrap-around section if needed        if section_width < frame_width:
            remaining_width = frame_width - section_width
            wrap_width = min(remaining_width, layer_width)
            if wrap_width > 0:
                wrap_section = layer_img[:draw_height, :wrap_width]
                frame[y_pos:y_pos + draw_height, section_width:section_width + wrap_width] = wrap_section
