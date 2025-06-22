"""
Enhanced Temple Run CV - Advanced 3D-Style Game
"""

import cv2
import numpy as np
import time
import pygame
import sys
import os
from config.game_config import *
from modules.player import Player
from modules.obstacle import ObstacleManager
from modules.background_simple import ParallaxBackground
from modules.ui import GameUI
from utils.game_utils import *

# Try to import gesture control systems in order of preference
try:
    from modules.gesture_control import HandGestureController, MEDIAPIPE_AVAILABLE
    if not MEDIAPIPE_AVAILABLE:
        raise ImportError("MediaPipe not available")
    GESTURE_CONTROLLER_TYPE = "mediapipe"
    print("📢 Using MediaPipe gesture control")
except ImportError:
    try:
        from modules.opencv_gesture_control import OpenCVGestureController as HandGestureController
        MEDIAPIPE_AVAILABLE = False
        GESTURE_CONTROLLER_TYPE = "opencv"
        print("📢 Using OpenCV gesture control (phone camera support)")
    except ImportError:
        from modules.keyboard_gesture_control import KeyboardGestureController as HandGestureController
        MEDIAPIPE_AVAILABLE = False
        GESTURE_CONTROLLER_TYPE = "keyboard"
        print("📢 Using keyboard gesture simulation (fallback mode)")

class TempleRunGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = STATE_MENU
        self.reset_game()
        
        # Game components
        self.background = ParallaxBackground()
        self.ui = GameUI()
        
        # Gesture control
        self.gesture_controller = None
        self.gesture_control_enabled = False
        self.init_gesture_control()
        
        # Sound management
        self.sound_manager = sound_manager
        self.init_sounds()
          # Load high score
        self.high_score, self.total_coins_collected = load_high_score()
        
        # Camera effects
        self.camera_shake = 0
        self.screen_flash = 0
        
        # Performance tracking
        self.last_time = time.time()
        
    def init_sounds(self):
        """Initialize sound effects and background music"""
        print("🎵 Initializing sound system...")
        
        # Load sound effects
        sound_files = {
            'jump': os.path.join(SOUNDS_DIR, 'jump.wav'),
            'coin': os.path.join(SOUNDS_DIR, 'coin.wav'),
            'collision': os.path.join(SOUNDS_DIR, 'collision.wav'),
            'game_over': os.path.join(SOUNDS_DIR, 'gameover.wav'),
            'start': os.path.join(SOUNDS_DIR, 'start.wav')
        }
        
        for name, filepath in sound_files.items():
            self.sound_manager.load_sound(name, filepath)
            
        # Load and start background music
        music_file = os.path.join(SOUNDS_DIR, 'background_music.mp3')
        if os.path.exists(music_file):
            self.sound_manager.play_music(music_file, loop=-1, fade_in=2000)
        else:
            print("⚠ Warning: Background music file not found")
        
        print("✓ Sound system ready!")
    
    def init_gesture_control(self):
        """Initialize gesture control system"""
        if not ENABLE_GESTURE_CONTROL:
            print("⚠ Gesture control disabled in config")
            return
        
        try:
            print("🤲 Initializing gesture control system...")
            self.gesture_controller = HandGestureController()            # Determine camera source based on controller type
            camera_source = GESTURE_CAMERA_INDEX
            
            if GESTURE_CONTROLLER_TYPE == "opencv":
                # Check if IP webcam URL is configured
                ip_webcam_url = IP_WEBCAM_URL
                
                if not ip_webcam_url:
                    print("\n📱 OpenCV Gesture Control - Phone Camera Setup:")
                    print("1. Install 'IP Webcam' app on your phone")
                    print("2. Start the app and note the IP address shown")
                    print("3. Make sure phone and computer are on same WiFi network")
                    print("4. Example URL: http://192.168.1.100:8080")
                    
                    ip_webcam_url = input("Enter your phone's IP Webcam URL (or press Enter for default camera): ").strip()
                
                if ip_webcam_url and 'http' in ip_webcam_url:
                    camera_source = ip_webcam_url
                    print(f"📱 Using phone camera via IP Webcam: {ip_webcam_url}")
                else:
                    print("📷 Using default camera (no IP Webcam URL provided)")
                    camera_source = GESTURE_CAMERA_INDEX
            
            # Try to initialize camera
            if self.gesture_controller.initialize_camera(camera_source):
                self.gesture_control_enabled = True
                print("✓ Gesture control system ready!")
                print("💡 Press 'G' during gameplay to toggle gesture control")
                
                if GESTURE_CONTROLLER_TYPE == "opencv":
                    print("📱 Make sure your phone's IP Webcam app is running")
                    print("🤲 Use hand gestures: Fist=Jump, 1 Finger=Crouch, Open Hand=Idle")
                elif GESTURE_CONTROLLER_TYPE == "keyboard":
                    print("⌨️ Use keyboard gestures: F=Jump, I=Crouch, O=Idle")
            else:
                print("⚠ Gesture control disabled - camera not available")
                self.gesture_control_enabled = False
                self.gesture_controller = None
        except Exception as e:
            print(f"❌ Failed to initialize gesture control: {e}")
            self.gesture_control_enabled = False
            self.gesture_controller = None
    
    def reset_game(self):
        """Reset game state for new game"""
        self.player = Player()
        self.obstacle_manager = ObstacleManager()
        self.coins_collected = 0
        self.game_over = False
        self.camera_shake = 0
        self.screen_flash = 0
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = STATE_PLAYING
                        self.reset_game()
                        self.sound_manager.play_sound('start')
                
                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        if self.player.jump():
                            self.sound_manager.play_sound('jump', prevent_overlap=True)
                    elif event.key == pygame.K_g:
                        # Toggle gesture control
                        if self.gesture_controller:
                            self.gesture_control_enabled = not self.gesture_control_enabled
                            status = "enabled" if self.gesture_control_enabled else "disabled"
                            print(f"🤲 Gesture control {status}")
                            if GESTURE_CONTROLLER_TYPE == "keyboard":
                                print("💡 Use F=Fist(Jump), I=Index(Crouch), O=Open(Idle)")
                        else:
                            print("⚠ Gesture control not available")
                    elif event.key == pygame.K_f and self.gesture_control_enabled and GESTURE_CONTROLLER_TYPE == "keyboard":
                        # Keyboard gesture: Fist (Jump)
                        if hasattr(self.gesture_controller, 'set_gesture_from_key'):
                            self.gesture_controller.set_gesture_from_key('F')
                    elif event.key == pygame.K_i and self.gesture_control_enabled and GESTURE_CONTROLLER_TYPE == "keyboard":
                        # Keyboard gesture: Index finger (Crouch)
                        if hasattr(self.gesture_controller, 'set_gesture_from_key'):
                            self.gesture_controller.set_gesture_from_key('I')
                    elif event.key == pygame.K_o and self.gesture_control_enabled and GESTURE_CONTROLLER_TYPE == "keyboard":
                        # Keyboard gesture: Open palm (Idle)
                        if hasattr(self.gesture_controller, 'set_gesture_from_key'):
                            self.gesture_controller.set_gesture_from_key('O')
                    elif event.key == pygame.K_p:
                        self.state = STATE_PAUSED
                        self.sound_manager.pause_music()
                    elif event.key == pygame.K_m:
                        # Toggle mute for all audio
                        muted = self.sound_manager.toggle_all_mute()
                        print(f"🔇 Audio {'muted' if muted else 'unmuted'}")
                    elif event.key == pygame.K_q:
                        return False
                
                elif self.state == STATE_PAUSED:
                    if event.key == pygame.K_p:
                        self.state = STATE_PLAYING
                        self.sound_manager.resume_music()
                    elif event.key == pygame.K_m:
                        # Toggle mute for all audio
                        muted = self.sound_manager.toggle_all_mute()
                        print(f"🔇 Audio {'muted' if muted else 'unmuted'}")
                    elif event.key == pygame.K_q:
                        return False
                
                elif self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_s:
                        self.state = STATE_PLAYING
                        self.reset_game()
                        self.sound_manager.play_sound('start')
                    elif event.key == pygame.K_m:
                        # Toggle mute for all audio
                        muted = self.sound_manager.toggle_all_mute()
                        print(f"🔇 Audio {'muted' if muted else 'unmuted'}")
                    elif event.key == pygame.K_q:
                        return False
        
        return True
    
    def update_game(self, dt):
        """Update game logic"""
        if self.state == STATE_PLAYING and not self.game_over:
            # Process gesture control
            if self.gesture_control_enabled and self.gesture_controller:
                gesture_action = self.process_gesture_input()
                if gesture_action == "jump":
                    if self.player.jump():
                        self.sound_manager.play_sound('jump', prevent_overlap=True)
                elif gesture_action == "crouch":
                    # Add crouch functionality if needed
                    pass
            
            # Update game objects
            self.player.update(dt)
            self.obstacle_manager.update(dt)
            self.background.update(dt)
            
            # Check collisions
            if self.obstacle_manager.check_collision(self.player.get_bounds()):
                self.game_over = True
                self.state = STATE_GAME_OVER
                self.sound_manager.play_sound('collision', volume=0.8)
                self.sound_manager.play_sound('game_over', volume=0.6)
                
                # Add screen shake and flash effects
                self.camera_shake = CAMERA_SHAKE_INTENSITY
                self.screen_flash = 255
                self.player.add_screen_shake(CAMERA_SHAKE_INTENSITY)
                
                # Update high score
                current_score = self.obstacle_manager.get_score()
                if current_score > self.high_score:
                    self.high_score = current_score
                
                total_coins = self.total_coins_collected + self.coins_collected
                save_high_score(self.high_score, total_coins)
            
            # Check coin collection
            collected_coins = self.obstacle_manager.check_coin_collection(self.player.get_bounds())
            if collected_coins > 0:
                self.coins_collected += collected_coins
                self.sound_manager.play_sound('coin', volume=0.7, prevent_overlap=False)
        
        # Update camera effects
        if self.camera_shake > 0:
            self.camera_shake *= 0.9
            if self.camera_shake < 0.5:
                self.camera_shake = 0
        
        if self.screen_flash > 0:
            self.screen_flash *= 0.8
            if self.screen_flash < 5:
                self.screen_flash = 0
    
    def process_gesture_input(self):
        """Process gesture input and return action"""
        if not self.gesture_controller or not self.gesture_control_enabled:
            return None
        
        try:
            # Process camera frame and get gesture
            frame, gesture, confidence = self.gesture_controller.process_frame()
            
            # Get gesture action with cooldown
            action = self.gesture_controller.get_gesture_action()
            
            # Show camera feed in separate window if enabled
            if SHOW_CAMERA_FEED and frame is not None:
                # Resize frame for display
                display_frame = cv2.resize(frame, (GESTURE_CAMERA_WIDTH, GESTURE_CAMERA_HEIGHT))
                cv2.imshow("Gesture Control", display_frame)
                cv2.waitKey(1)  # Non-blocking window update
            
            return action
        except Exception as e:
            print(f"⚠ Gesture processing error: {e}")
            return None
    
    def render_game(self):
        """Render the game"""
        # Create frame
        frame = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
        
        if self.state == STATE_MENU:
            # Convert to pygame surface for menu
            pygame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            pygame_surface = self.ui.draw_start_screen(pygame_surface)
            self.screen.blit(pygame_surface, (0, 0))
        
        elif self.state == STATE_PLAYING or self.state == STATE_GAME_OVER:
            # Draw background
            frame = self.background.draw(frame)
            
            # Draw game objects
            if not self.game_over:
                frame = self.player.draw(frame)
            frame = self.obstacle_manager.draw(frame)
            
            # Draw HUD
            score = self.obstacle_manager.get_score()
            speed = self.obstacle_manager.speed_multiplier
            sound_muted = self.sound_manager.sound_muted or self.sound_manager.music_muted
            gesture_active = self.gesture_control_enabled and self.gesture_controller is not None
            frame = self.ui.draw_game_hud(frame, score, self.coins_collected, speed, 
                                        lives=3, sound_muted=sound_muted, gesture_control=gesture_active)
            
            # Apply camera shake
            if self.camera_shake > 0:
                frame = apply_screen_shake(frame, int(self.camera_shake))
            
            # Apply screen flash
            if self.screen_flash > 0:
                flash_overlay = np.full_like(frame, 255)
                alpha = self.screen_flash / 255.0
                frame = cv2.addWeighted(frame, 1 - alpha * 0.3, flash_overlay, alpha * 0.3, 0)
            
            # Convert to pygame surface
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
            self.screen.blit(frame_surface, (0, 0))
            
            # Draw game over screen
            if self.state == STATE_GAME_OVER:
                final_score = self.obstacle_manager.get_score()
                self.screen = self.ui.draw_game_over_screen(
                    self.screen, final_score, self.high_score, self.coins_collected
                )
        
        elif self.state == STATE_PAUSED:
            # Draw game with pause overlay
            frame = self.background.draw(frame)
            frame = self.player.draw(frame)
            frame = self.obstacle_manager.draw(frame)
            
            # Convert to pygame surface
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
            self.screen.blit(frame_surface, (0, 0))
            
            # Draw pause overlay
            self.screen = self.ui.draw_pause_screen(self.screen)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - self.last_time
            self.last_time = current_time
            
            # Handle events
            running = self.handle_events()
            
            # Update game
            self.update_game(dt)
            
            # Render
            self.render_game()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        # Cleanup
        if self.gesture_controller:
            self.gesture_controller.cleanup()
        pygame.quit()
        sys.exit()

def main():
    """Main function"""
    try:
        game = TempleRunGame()
        game.run()
    except Exception as e:
        print(f"Game error: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
