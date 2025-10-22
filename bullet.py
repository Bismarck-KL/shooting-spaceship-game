import pygame
from color import red, yellow

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,screen_width,screen_height,type, player_id):
        super().__init__()
        self.player_id = player_id
        self.image = pygame.Surface((5, 10))
        if type == 'player':
            self.image.fill(yellow)  # Yellow bullet for player
            self.speedy = -10
        else:    
            self.image.fill(red)  # Red bullet for enemy
            self.speedy = 5

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.type = type
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.top > self.screen_height:
            self.kill()  # Remove the bullet if it goes off-screen
