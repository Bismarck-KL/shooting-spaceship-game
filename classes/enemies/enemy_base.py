import pygame
import random
from utils.color import orange

class Enemy(pygame.sprite.Sprite):
    """Base class for all enemy types"""
    def __init__(self, screen_width, screen_height, score_callback=None, screen=None):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score_callback = score_callback
        self.health_point = 1
        self.score = 10
        self.speed_x = 0
        self.speed_y = 0
        self.direction = 1
        self.screen = screen
        self.particles = pygame.sprite.Group()

    def update(self):
        """Base update method - Updates position and particles"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Handle particle effects
        self.generate_particles()
        self.particles.update()
        if self.screen:  # Only draw if screen is provided
            self.particles.draw(self.screen)

    def generate_particles(self):
        """Generate particles with enemy-specific effects"""
        if not self.screen:  # Skip particle generation if no screen
            return
            
        if random.randint(0, 4) == 0:  # Adjust frequency of particle generation
            # Get enemy type from class name
            enemy_type = 'normal'
            class_name = self.__class__.__name__.lower()
            if 'fast' in class_name:
                enemy_type = 'fast'
            elif 'tank' in class_name:
                enemy_type = 'tank'

            particle = Particle(
                random.randint(self.rect.left, self.rect.right),
                self.rect.top + random.randint(0, 10),
                enemy_type
            )
            self.particles.add(particle)

    def update_health_point(self, hp):
        self.health_point += hp
        if self.health_point <= 0:
            if self.score_callback:
                self.score_callback(self.score)
            self.kill()  # Remove the enemy if health is 0 or less


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='normal'):
        super().__init__()
        
        # Adjust particle size based on enemy type
        if enemy_type == 'tank':
            self.image = pygame.Surface((4, 6))  # Larger particles for tank
        elif enemy_type == 'fast':
            self.image = pygame.Surface((2, 4))  # Thinner particles for fast
        else:
            self.image = pygame.Surface((3, 5))  # Normal size
        
        self.image.fill(orange)  # Orange for normal enemies

        self.rect = self.image.get_rect(center=(x, y))
        
        # Adjust particle behavior based on enemy type
        if enemy_type == 'fast':
            self.velocity_x = random.uniform(-2, 2)
            self.velocity_y = random.uniform(0.5, 1.5)
        elif enemy_type == 'tank':
            self.velocity_x = random.uniform(-0.5, 0.5)
            self.velocity_y = random.uniform(0.2, 0.8)
        else:
            self.velocity_x = random.uniform(-1, 1)
            self.velocity_y = random.uniform(0.5, 1.5)
            
        self.lifetime = 20  # Lifetime in frames

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.lifetime -= 1

        # Fade out effect
        if self.lifetime <= 0:
            self.kill()  # Remove the particle when its lifetime is over
