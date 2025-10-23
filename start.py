import pygame
import sys
import subprocess
from utils.color import blue, btn_hover_color, white, btn_active_color

# Constants
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

# Initialize Pygame
pygame.init()

# Create the centered window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game Start Menu")


# Button class
class Button:
    def __init__(self, text, x, y):
        self.font = pygame.font.Font(None, 36)
        self.text = text
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.color = blue  # Default color
        self.hover_color = btn_hover_color  # Lighter blue when hovered
        self.text_color = white
        self.is_hovered = False

    def draw(self, surface):
        # Check if mouse is hovering over button
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color = self.hover_color if self.is_hovered else self.color
        
        # Draw button with a slight 3D effect
        pygame.draw.rect(surface, color, self.rect)
        if self.is_hovered:
            # Draw highlight when hovered
            pygame.draw.rect(surface, white, self.rect, 2)
        else:
            # Draw regular border
            pygame.draw.rect(surface, btn_active_color, self.rect, 2)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        if self.is_hovered:
            # Move text slightly when hovered to give a "pressed" effect
            text_rect.y += 1
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Calculate center position for buttons
button_x = (WIDTH - BUTTON_WIDTH) // 2  # Center horizontally
button_start_y = HEIGHT // 2 - 100       # Start buttons from middle of screen

# Create buttons
single_player_btn = Button("Single Player", button_x, button_start_y)
muiltiple_player_pve_btn = Button("Multiplayer PvE", button_x, button_start_y + 70)
muiltiple_player_pvp_btn = Button("Multiplayer PvP", button_x, button_start_y + 140)
quit_btn = Button("Quit", button_x, button_start_y + 210)

# Create title font
title_font = pygame.font.Font(None, 74)
title_text = "Space Shooter"

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if single_player_btn.is_clicked(event.pos):
                subprocess.Popen(["python", "main.py", "single_player_pve"])  # Start main game script
                running = False  # Close current script
            elif muiltiple_player_pve_btn.is_clicked(event.pos):
                subprocess.Popen(["python", "main.py", "multiple_player_pve"])  # Start main game script
                running = False  # Close current script
            elif muiltiple_player_pvp_btn.is_clicked(event.pos):
                subprocess.Popen(["python", "pvp.py", "multiple_player_pvp"])  # Start main game script
                running = False  # Close current script
            elif quit_btn.is_clicked(event.pos):
                running = False


    # Clear screen with a dark background
    screen.fill((0, 0, 20))  # Very dark blue
    
    # Draw title
    title_surface = title_font.render(title_text, True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(WIDTH // 2, button_start_y - 80))
    screen.blit(title_surface, title_rect)
    
    # Draw buttons
    single_player_btn.draw(screen)
    muiltiple_player_pve_btn.draw(screen)
    muiltiple_player_pvp_btn.draw(screen)
    quit_btn.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # Cap at 60 FPS

pygame.quit()
sys.exit()