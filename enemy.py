import  pygame
from color import gray, black
import random

# Enemy types
enemy_types = {
    'basic': {'color': gray, 'size': (40, 30), 'speed': 2},
    'fast': {'color': gray, 'size': (30, 20), 'speed': 4},
    'strong': {'color': gray, 'size': (50, 40), 'speed': 1}
}

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, enemy_type):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = pygame.Surface(enemy_types[enemy_type]['size'])
        self.image.fill(enemy_types[enemy_type]['color'])
        self.image.set_colorkey(black)
        pygame.draw.polygon(self.image, enemy_types[enemy_type]['color'], [(0, 30), (20, 0), (40, 30)])  # Simple triangle shape

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = enemy_types[enemy_type]['speed']

    def update(self):
        # move downwards
        self.rect.y += self.speedy
        if self.rect.top > self.screen_height:
            self.kill()  # Remove the enemy if it goes off the screen