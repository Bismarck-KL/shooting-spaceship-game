import pygame
import os
from color import black

pygame.init()
# Set up a temporary display mode for image loading
pygame.display.set_mode((1, 1), pygame.NOFRAME)

def load_assets():
    # Load spaceship image
    try:
        spaceship_img = pygame.image.load(os.path.join("assets/images/", "spaceship.png")).convert()
    except pygame.error as e:
        print(f"Error loading spaceship image file: {e}")
        spaceship_img = None  # Set to None if loading fails

    # Load spaceship image
    try:
        spaceship_img_2 = pygame.image.load(os.path.join("assets/images/", "spaceship_2.png")).convert()
    except pygame.error as e:
        print(f"Error loading spaceship image file: {e}")
        spaceship_img_2 = None  # Set to None if loading fails


    return spaceship_img, spaceship_img_2

# load explosion images
def explosion_img_loader():
    # Explosion animation
    expl_anim = {}
    expl_anim['lg'] = []
    expl_anim['sm'] = []
    try:
        for i in range(9):
            expl_img = pygame.image.load(os.path.join("assets/images/expl", f"expl{i}.png")).convert()
            expl_img.set_colorkey(black)
            expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
            expl_anim['sm'].append(pygame.transform.scale(expl_img, (45, 45)))
    except pygame.error as e:
        print(f"Error loading explosion image file: {e}")

    return expl_anim



def stone_img_loader():

    # Load stone images
    stone_img = [None, None]  
    try:
        # Load each stone image separately to identify which one fails
        stone_img[0] = pygame.image.load(os.path.join("assets/images/", "rock3.png")).convert()
        # print("Successfully loaded rock3.png")
        stone_img[1] = pygame.image.load(os.path.join("assets/images/", "rock6.png")).convert()
        # print("Successfully loaded rock6.png")
        
        # Check if both images loaded successfully
        if stone_img[0] is not None and stone_img[1] is not None:
            return stone_img
        else:
            raise pygame.error("One or more stone images failed to load")
            
    except pygame.error as e:
        print(f"Error loading stone image file: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Checking if files exist:")
        print(f"rock3.png exists: {os.path.exists(os.path.join('assets/images/', 'rock3.png'))}")
        print(f"rock6.png exists: {os.path.exists(os.path.join('assets/images/', 'rock6.png'))}")
        raise  # Re-raise the exception to prevent the game from continuing with invalid images