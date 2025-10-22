import pygame

# Shield class
class Shield(pygame.sprite.Sprite):
    def __init__(self, player):
        """Initialize the Shield instance."""
        super().__init__()
        self.radius = 50
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0, 95), (self.radius, self.radius), self.radius)  # Draw the circle
        self.rect = self.image.get_rect(center=player.rect.center)  # Set initial position to match the player
        self.player = player  # Reference to the player


    def update(self):
        """Update the shield's position to follow the player."""
        self.rect.center = self.player.rect.center  # Keep the shield centered on the player
