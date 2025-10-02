import pygame 

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()
running = True

frame_per_seconds = 60

# Initialize pygame
pygame.init()

# Colors
black = (0, 0, 0)  # Black
green = (0, 255, 0)  # Green


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(green)  # Green spaceship
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.speed = 4

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[pygame.K_RIGHT]:
            self.rect.x +=   self.speed
            if self.rect.right > width:
                self.rect.right = width
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            if self.rect.top < 0:
                self.rect.top = 0   
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            if self.rect.bottom > height:
                self.rect.bottom = height

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    all_sprites.update()  # Update all sprites

    screen.fill(black)  # Clear screen with black
    all_sprites.draw(screen)  # Draw all sprites
    pygame.display.flip()  # Update the display
    clock.tick(frame_per_seconds)  # Maintain 60 FPS


# Clean up and exit
pygame.mixer.quit()
pygame.quit()
