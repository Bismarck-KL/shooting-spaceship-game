import pygame 
import random

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
brown = (139, 69, 19)  # Brown
red = (255, 0, 0)  # Red
yellow = (255, 255, 0)  # Yellow

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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 'player')
        all_sprites.add(bullet)

# Stone class 
class Stone(pygame.sprite.Sprite):
    def reset_position(self):
        # some stones may appear partially off-screen
        self.rect.x = random.randint(-100, width - self.rect.width+100) 
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1,6)
        self.speedx = random.randint(-2, 2)

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(brown)  # Brown stone
        self.rect = self.image.get_rect()
        self.reset_position()    

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height:
            self.reset_position() 

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        if type == 'player':
            self.image.fill(yellow)  # Yellow bullet for player
            self.speedy = -10
        else:    
            self.image.fill(red)  # Red bullet for enemy
            self.speedy = 5

        self.type = type
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.top > height:
            self.kill()  # Remove the bullet if it goes off-screen
        

# Create sprite groups
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for _ in range(8):
    stone = Stone()
    all_sprites.add(stone)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                player.shoot()  # Player shoots a bullet

    all_sprites.update()  # Update all sprites

    screen.fill(black)  # Clear screen with black
    all_sprites.draw(screen)  # Draw all sprites
    pygame.display.flip()  # Update the display
    clock.tick(frame_per_seconds)  # Maintain 60 FPS


# Clean up and exit
pygame.mixer.quit()
pygame.quit()
