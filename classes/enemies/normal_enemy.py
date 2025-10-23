from .enemy_base import Enemy
import pygame
import random
from utils.color import white

from utils.game_image_loader import enemy_img_loader
enemy_images = enemy_img_loader()

class NormalEnemy(Enemy):
    """Slow but tough enemy that takes multiple hits to destroy"""
    def __init__(self, screen_width, screen_height, score_callback=None):
        super().__init__(screen_width, screen_height, score_callback)
        self.image = pygame.transform.scale(enemy_images[0], (50, 50))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(white)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = random.randrange(-50, -40)
        self.speedy = 2
        self.health_point = 3
        self.score = 20
        
    def update(self):
        """Move downwards slowly"""
        self.rect.y += self.speedy
        if self.rect.top > self.screen_height:
            # reset position to top
            self.rect.y = random.randrange(-50, -40)
            self.rect.x = random.randrange(0, self.screen_width - self.rect.width)
