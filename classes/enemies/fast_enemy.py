from .enemy_base import Enemy
import pygame
import random
from utils.color import white
from utils.game_image_loader import enemy_img_loader
enemy_images = enemy_img_loader()


class FastEnemy(Enemy):
    """Fast-moving enemy that zigzags across the screen"""
    def __init__(self, screen_width, screen_height, score_callback=None, screen=None):
        # Call parent class constructor first
        super().__init__(screen_width, screen_height, score_callback, screen=screen)

        # Set up the enemy sprite
        self.image = pygame.transform.scale(enemy_images[1], (50, 50))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(white)

        # Set up position and movement
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = random.randrange(-50, -40)
        
        # Fast enemy specific attributes
        self.speed_y = 4  # Using speed_y from parent class
        self.speed_x = 2  # Using speed_x from parent class
        self.health_point = 1
        self.score = 20

    def update(self):
        """Move in a zigzag pattern and handle particles"""
        # Update position
        self.speed_y = 4  # Maintain speed
        self.speed_x = 2 * self.direction
        
        # Call parent update for basic movement and particles
        super().update()
        
        # Handle screen boundaries
        if self.rect.right >= self.screen_width or self.rect.left <= 0:
            self.direction *= -1
        
        if self.rect.top > self.screen_height:
            # back to top
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, self.screen_width - self.rect.width)