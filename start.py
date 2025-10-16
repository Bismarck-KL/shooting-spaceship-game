import pygame
import sys
import subprocess

# Constants
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game Start Menu")


# Button class
class Button:
    def __init__(self, text, x, y):
        self.font = pygame.font.Font(None, 36)
        self.text = text
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 128, 255), self.rect)  # Button color
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
single_player_btn = Button("Single Player", 300, 250)
muiltiple_player_pve_btn = Button("Multiplayer PvE", 300, 320)
quit_btn = Button("Quit", 300, 390)

# Main loop
running = True
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
            elif quit_btn.is_clicked(event.pos):
                running = False

    # Draw everything
    single_player_btn.draw(screen)
    muiltiple_player_pve_btn.draw(screen)
    quit_btn.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()