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
        self.shooting_speed = 200  # Shooting speed in milliseconds
        self.last_shot_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[pygame.K_d]:
            self.rect.x +=   self.speed
            if self.rect.right > width:
                self.rect.right = width
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            if self.rect.top < 0:
                self.rect.top = 0   
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            if self.rect.bottom > height:
                self.rect.bottom = height

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shooting_speed:
            self.last_shot_time = current_time  # Update the last shot time
            self.shoot()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 'player')
        all_sprites.add(bullet)
        player_bullets.add(bullet)  

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
        self.size = random.randint(20,50)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(brown)  # Brown stone
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 /2
        # pygame.draw.circle(self.image,red,self.rect.center,self.radius) #Debug rendering
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
stones = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for _ in range(8):
    stone = Stone()
    all_sprites.add(stone)
    stones.add(stone)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # elif event.key == pygame.K_SPACE:
            #     player.shoot()  # Player shoots a bullet

    all_sprites.update()  # Update all sprites
    stone_playerbullet_hit = pygame.sprite.groupcollide(stones, player_bullets, True, True)  # Check for collisions between stones and player bullets
    if stone_playerbullet_hit:
        for _ in stone_playerbullet_hit:
            stone = Stone()
            all_sprites.add(stone)
            stones.add(stone)

    palyer_stone_hit = pygame.sprite.spritecollide(player, stones, False)  # Check for collisions between player and stones
    if palyer_stone_hit:
        # disable the stone
        stone = palyer_stone_hit[0]
        stone.kill()


    screen.fill(black)  # Clear screen with black
    all_sprites.draw(screen)  # Draw all sprites
    pygame.display.flip()  # Update the display
    clock.tick(frame_per_seconds)  # Maintain 60 FPS


# Clean up and exit
pygame.mixer.quit()
pygame.quit()
