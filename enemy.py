import  pygame
from color import gray, black, white
import random
from game_image_loader import enemy_img_loader

enemy_images = enemy_img_loader()

# Enemy types
enemy_types = {
    'basic': { 'size': (50, 50), 'health_point': 3, 'speed': 2, 'image': enemy_images[0], 'score': 20},
    'fast': {'size': (50, 50), 'health_point': 1, 'speed': 4, 'image': enemy_images[1], 'score': 20},
    'strong': {'size': (100, 100), 'health_point': 10, 'speed': 1, 'image': enemy_images[2], 'score': 50}
}

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, enemy_type, score_callback=None):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.score = enemy_types[enemy_type]['score']
        self.score_callback = score_callback

        self.image = pygame.transform.scale(enemy_types[enemy_type]['image'], enemy_types[enemy_type]['size'])
        self.image.set_colorkey(white)
        self.image = pygame.transform.rotate(self.image, 180)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = random.randrange(-50, -40)
        self.speedy = enemy_types[enemy_type]['speed']
        self.health_point = enemy_types[enemy_type]['health_point']

    def update(self):
        # move downwards
        self.rect.y += self.speedy
        if self.rect.top > self.screen_height:
            # reset position to top
            self.rect.y = random.randrange(-50, -40)
            self.rect.x = random.randrange(0, self.screen_width - self.rect.width)

    def update_health_point(self, hp):
        self.health_point += hp
        if self.health_point <= 0:
            self.score_callback(self.score)
            self.kill()  # Remove the enemy if health is 0 or less
