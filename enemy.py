import  pygame
from color import gray, black, white
import random
from game_image_loader import enemy_img_loader

enemy_images = enemy_img_loader()

# Enemy types
enemy_types = {
    'basic': { 'size': (50, 50), 'health_point': 1, 'speed': 2, 'image': enemy_images[0]},
    'fast': {'size': (50, 50), 'health_point': 1, 'speed': 4, 'image': enemy_images[1]},
    'strong': {'size': (100, 100), 'health_point': 3, 'speed': 0.5, 'image': enemy_images[2]}
}

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, enemy_type):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = pygame.transform.scale(enemy_types[enemy_type]['image'], enemy_types[enemy_type]['size'])
        self.image.set_colorkey(white)
        self.image = pygame.transform.rotate(self.image, 180)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = enemy_types[enemy_type]['speed']
        self.health_point = enemy_types[enemy_type]['health_point']

    def update(self):
        # move downwards
        self.rect.y += self.speedy
        if self.rect.top > self.screen_height:
            self.kill()  # Remove the enemy if it goes off the screen

    def update_health_point(self, hp):
        self.health_point += hp
        if self.health_point <= 0:
            self.kill()  # Remove the enemy if health is 0 or less
