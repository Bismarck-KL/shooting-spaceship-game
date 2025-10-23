import pygame

class Enemy(pygame.sprite.Sprite):
    """Base class for all enemy types"""
    def __init__(self, screen_width, screen_height, score_callback=None):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score_callback = score_callback
        self.health_point = 1
        self.score = 10
        self.speed_x = 0
        self.speed_y = 0
        self.direction = 1

    def update(self):
        """Base update method - movement and boundary checking"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
    def update_health_point(self, hp):
        self.health_point += hp
        if self.health_point <= 0:
            if self.score_callback:
                self.score_callback(self.score)
            self.kill()  # Remove the enemy if health is 0 or less
