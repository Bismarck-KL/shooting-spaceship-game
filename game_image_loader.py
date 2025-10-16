import pygame
import os
from color import black

pygame.init()

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

    # Load stone images
    stone_img = [None, None]
    try:
        stone_img[0] = pygame.image.load(os.path.join("assets/images/", "rock3.png")).convert()
        stone_img[1] = pygame.image.load(os.path.join("assets/images/", "rock6.png")).convert()
    except pygame.error as e:
        print(f"Error loading stone image file: {e}")
    
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

    return spaceship_img, spaceship_img_2, stone_img, expl_anim
