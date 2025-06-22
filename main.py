"""
Temple Run CV - Main Game Loop
"""

import cv2
import numpy as np
import time
import pygame
from config.game_config import *
from modules.player import Player
from modules.obstacle import ObstacleManager
from utils.game_utils import init_pygame_mixer, draw_score, create_background

def reset_game():
    """Reset the game state"""
    player = Player()
    obstacle_manager = ObstacleManager()
    score = 0
    game_over = False
    return player, obstacle_manager, score, game_over

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    
    # Initialize game objects and state
    player, obstacle_manager, score, game_over = reset_game()
    last_time = time.time()
    
    # Create background
    background = create_background()
      # Initialize Pygame mixer for sound (to be implemented)
    mixer = init_pygame_mixer()
    
    running = True
    while running:
        # Calculate delta time
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
          # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_s and game_over:
                    # Reset the game when 'S' is pressed and game is over
                    player, obstacle_manager, score, game_over = reset_game()
          # Update game objects if not game over
        if not game_over:
            player.update()
            obstacle_manager.update(dt)
            
            # Check collisions
            if obstacle_manager.check_collision(player.get_bounds()):
                game_over = True
            
            # Update score
            score += dt * 10
              # Draw game objects
            screen.fill(BLACK)  # Clear screen
            frame = background.copy()
            frame = player.draw(frame)
            frame = obstacle_manager.draw(frame)
            frame = draw_score(frame, int(score))
            
            # Convert OpenCV frame to Pygame surface and display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (0, 0))
            
            # Draw game over message if needed (after the frame is displayed)
            if game_over:
                # Draw semi-transparent overlay
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(128)
                screen.blit(overlay, (0, 0))
                
                # Draw "GAME OVER" text
                font_large = pygame.font.Font(None, 72)
                text_game_over = font_large.render("GAME OVER", True, RED)
                text_rect = text_game_over.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
                screen.blit(text_game_over, text_rect)
                
                # Draw score
                font_score = pygame.font.Font(None, 48)
                score_text = font_score.render(f"Final Score: {int(score)}", True, WHITE)
                score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
                screen.blit(score_text, score_rect)
                  # Draw instructions
                font_small = pygame.font.Font(None, 36)
                instruction1 = font_small.render("Press 'S' to restart", True, WHITE)
                inst_rect1 = instruction1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
                screen.blit(instruction1, inst_rect1)
                
                instruction2 = font_small.render("Press 'Q' to quit", True, WHITE)
                inst_rect2 = instruction2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
                screen.blit(instruction2, inst_rect2)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()
