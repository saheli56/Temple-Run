"""
Enhanced UI Module for Temple Run
"""

import cv2
import numpy as np
import pygame
from config.game_config import *

class GameUI:
    def __init__(self):
        self.font_large = cv2.FONT_HERSHEY_SIMPLEX
        self.font_medium = cv2.FONT_HERSHEY_SIMPLEX
        self.font_small = cv2.FONT_HERSHEY_SIMPLEX
        
        # Initialize pygame fonts for better text rendering
        pygame.font.init()
        self.pygame_font_large = pygame.font.Font(None, 48)
        self.pygame_font_medium = pygame.font.Font(None, 36)
        self.pygame_font_small = pygame.font.Font(None, 24)
        
        # UI elements positions
        self.score_pos = (20, 50)
        self.coins_pos = (20, 90)
        self.speed_pos = (20, 130)
        
    def draw_text_opencv(self, frame, text, position, font=None, scale=1, color=WHITE, thickness=2):
        """Draw text using OpenCV"""
        if font is None:
            font = self.font_medium
        cv2.putText(frame, text, position, font, scale, color, thickness)
        return frame
    
    def draw_text_pygame(self, surface, text, position, font=None, color=WHITE, background=None):
        """Draw text using Pygame (better quality)"""
        if font is None:
            font = self.pygame_font_medium
            
        text_surface = font.render(text, True, color, background)
        surface.blit(text_surface, position)
        return surface
    
    def draw_game_hud(self, frame, score, coins, speed_multiplier, lives=3, sound_muted=False, gesture_control=False):
        """Draw the main game HUD with sound and gesture control status"""
        # Score
        score_text = f"Score: {score:,}"
        self.draw_text_opencv(frame, score_text, self.score_pos, scale=0.8, thickness=2)
        
        # Coins
        coins_text = f"Coins: {coins}"
        self.draw_text_opencv(frame, coins_text, self.coins_pos, scale=0.7, color=YELLOW, thickness=2)
        
        # Speed
        speed_text = f"Speed: {speed_multiplier:.1f}x"
        speed_color = GREEN if speed_multiplier <= 2.0 else ORANGE if speed_multiplier <= 3.0 else RED
        self.draw_text_opencv(frame, speed_text, self.speed_pos, scale=0.6, color=speed_color, thickness=2)
        
        # Lives (hearts)
        heart_x = WINDOW_WIDTH - 150
        for i in range(lives):
            cv2.circle(frame, (heart_x + i * 30, 40), 10, RED, -1)
        
        # Sound status indicator
        if sound_muted:
            sound_text = "🔇 MUTED"
            sound_color = RED
        else:
            sound_text = "🔊"
            sound_color = GREEN
        
        self.draw_text_opencv(frame, sound_text, (WINDOW_WIDTH - 200, 80), 
                            scale=0.5, color=sound_color, thickness=2)
        
        # Gesture control status indicator
        if gesture_control:
            gesture_text = "🤲 GESTURE"
            gesture_color = GREEN
        else:
            gesture_text = "⌨️ KEYBOARD"
            gesture_color = BLUE
        
        self.draw_text_opencv(frame, gesture_text, (WINDOW_WIDTH - 220, 120), 
                            scale=0.5, color=gesture_color, thickness=2)
        
        # Controls hint
        if gesture_control:
            controls_text = "G: Toggle Control | P: Pause | M: Mute | Q: Quit"
        else:
            controls_text = "SPACE: Jump | G: Gesture | P: Pause | M: Mute | Q: Quit"
        self.draw_text_opencv(frame, controls_text, (20, WINDOW_HEIGHT - 30), 
                            scale=0.4, color=WHITE, thickness=1)
        
        return frame
    
    def draw_heart(self, frame, position, size):
        """Draw a heart shape for lives"""
        x, y = position
        # Simple heart approximation using circles and triangle
        cv2.circle(frame, (x - size//4, y), size//3, RED, -1)
        cv2.circle(frame, (x + size//4, y), size//3, RED, -1)
        
        # Triangle for bottom of heart
        points = np.array([[x - size//2, y + size//4], 
                          [x + size//2, y + size//4], 
                          [x, y + size]], np.int32)
        cv2.fillPoly(frame, [points], RED)
        
        return frame
    
    def draw_game_over_screen(self, surface, final_score, high_score, coins):
        """Draw enhanced game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        surface.blit(overlay, (0, 0))
        
        # Game Over title with shadow effect
        title_text = "GAME OVER"
        title_color = (255, 50, 50)  # Bright red
        shadow_color = (100, 0, 0)   # Dark red
        
        # Draw shadow
        title_shadow = self.pygame_font_large.render(title_text, True, shadow_color)
        title_rect_shadow = title_shadow.get_rect(center=(WINDOW_WIDTH//2 + 3, WINDOW_HEIGHT//2 - 97))
        surface.blit(title_shadow, title_rect_shadow)
        
        # Draw main title
        title_surface = self.pygame_font_large.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        surface.blit(title_surface, title_rect)
        
        # Final score
        score_text = f"Final Score: {final_score:,}"
        score_surface = self.pygame_font_medium.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40))
        surface.blit(score_surface, score_rect)
        
        # High score
        if final_score > high_score:
            high_score_text = "NEW HIGH SCORE!"
            high_score_color = YELLOW
        else:
            high_score_text = f"High Score: {high_score:,}"
            high_score_color = WHITE
            
        high_score_surface = self.pygame_font_medium.render(high_score_text, True, high_score_color)
        high_score_rect = high_score_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        surface.blit(high_score_surface, high_score_rect)
        
        # Coins collected
        coins_text = f"Coins Collected: {coins}"
        coins_surface = self.pygame_font_small.render(coins_text, True, YELLOW)
        coins_rect = coins_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
        surface.blit(coins_surface, coins_rect)
        
        # Instructions
        restart_text = "Press 'S' to Restart"
        restart_surface = self.pygame_font_medium.render(restart_text, True, GREEN)
        restart_rect = restart_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80))
        surface.blit(restart_surface, restart_rect)
        
        quit_text = "Press 'Q' to Quit"
        quit_surface = self.pygame_font_medium.render(quit_text, True, WHITE)
        quit_rect = quit_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 120))
        surface.blit(quit_surface, quit_rect)
        
        return surface
    
    def draw_start_screen(self, surface):
        """Draw game start/menu screen"""
        # Background gradient effect
        for y in range(WINDOW_HEIGHT):
            color_intensity = int(50 + (y / WINDOW_HEIGHT) * 100)
            pygame.draw.line(surface, (0, 0, color_intensity), (0, y), (WINDOW_WIDTH, y))
        
        # Title
        title_text = "TEMPLE RUN CV"
        title_surface = self.pygame_font_large.render(title_text, True, YELLOW)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        surface.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Enhanced Edition"
        subtitle_surface = self.pygame_font_medium.render(subtitle_text, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60))
        surface.blit(subtitle_surface, subtitle_rect)
        
        # Instructions
        instructions = [
            "Press SPACE to Jump",
            "Collect Coins for Points",
            "Avoid Obstacles",
            "",
            "Press SPACE to Start"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction:  # Skip empty strings
                color = GREEN if "Start" in instruction else WHITE
                inst_surface = self.pygame_font_small.render(instruction, True, color)
                inst_rect = inst_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + i * 30))
                surface.blit(inst_surface, inst_rect)
        
        return surface
    
    def draw_pause_screen(self, surface):
        """Draw pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        surface.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = "PAUSED"
        pause_surface = self.pygame_font_large.render(pause_text, True, WHITE)
        pause_rect = pause_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        surface.blit(pause_surface, pause_rect)
        
        # Resume instruction
        resume_text = "Press 'P' to Resume"
        resume_surface = self.pygame_font_medium.render(resume_text, True, WHITE)
        resume_rect = resume_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        surface.blit(resume_surface, resume_rect)
        
        return surface
