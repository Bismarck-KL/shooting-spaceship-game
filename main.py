import pygame 
import random

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()
running = True

frame_per_seconds = 60

# Game data
game_status = "Pending"
game_score = 0

# Initialize pygame
pygame.init()

# Colors
white = (255,255,255)
black = (0, 0, 0)  # Black
green = (0, 255, 0)  # Green
brown = (139, 69, 19)  # Brown
red = (255, 0, 0)  # Red
yellow = (255, 255, 0)  # Yellow
star_color = (128,128,128)

def random_star_speed():
    return random.uniform(1, 30)

# Initialize water particles with actual speeds
star_particles = [(random.randint(0, width), random.randint(-height, 0), random_star_speed()) for _ in range(20)]  # (x, y, speed)

def draw_star():
    global star_particles
    for i, (x, y, speed) in enumerate(star_particles):
        y += speed  # Move down by the speed
        if y > height:  # If the star goes off the screen
            y = random.randint(-height, 0)  # Reset to a new position at the top
            x = random.randint(0, width)  # Randomize the x position
            speed = random_star_speed()  # Randomize speed
        star_particles[i] = (x, y, speed)  # Update the particle position and speed

    # Draw the stars on the screen
    for x, y, _ in star_particles:
        pygame.draw.circle(screen, star_color, (int(x), int(y)), random.randint(1, 3))  # For radius, using a small random size

# Player class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.original_color = green
        self.image.fill(self.original_color)  # Green spaceship
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.speed = 4
        self.shooting_speed = 200  # Shooting speed in milliseconds
        self.last_shot_time = 0
        self.health_point = 3
        self.flashing = False  # Track if flashing is active
        self.flash_start_time = 0  # Track when the flash started

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

        # Handle flashing effect
        if self.flashing:
            if current_time - self.flash_start_time < 750:
                if (current_time // 5) % 2 == 0: 
                    self.image.fill((255, 255, 255))  # Flash white
                else:
                    self.image.fill(self.original_color)  # Back to original color
            else:
                self.flashing = False  # Stop flashing
                self.image.fill(self.original_color)  # Ensure it resets to original color

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 'player')
        all_sprites.add(bullet)
        player_bullets.add(bullet)  

    def set_health_point(self,point):
        global game_status
        self.health_point+=point
        if self.health_point <=0:
            game_status = "End"

    def flash_white(self):
        self.flashing = True
        self.flash_start_time = pygame.time.get_ticks()

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
        self.size = random.randint(20,100)
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

# Font setup
game_font = pygame.font.Font(None, 24) 
def draw_game_ui():
    global game_status

    player_health_text  = game_font.render(f"{player.health_point}", True, white)
    player_health_rect = player_health_text.get_rect(topleft = (20, 20))
    pygame.draw.rect(screen, white, player_health_rect.inflate(20, 10), 2)
    screen.blit(player_health_text, player_health_rect)

    score_text = game_font.render(f"{game_score:.2f}", True, white)
    score_rect = score_text.get_rect()
    score_rect.centerx = width // 2  # Center horizontally
    score_rect.top = 20
    pygame.draw.rect(screen, white, score_rect.inflate(20, 10), 2)
    screen.blit(score_text, score_rect)


    stone_text  = game_font.render(f"{len(stones):.2f}", True, white)
    stone_rect = stone_text.get_rect()
    stone_rect.topright = (width - 20, 20)   
    pygame.draw.rect(screen, red, stone_rect.inflate(20, 10), 2)
    screen.blit(stone_text, stone_rect)

def draw_report_ui():
    # To-Do draw report
    score_text = game_font.render(f"{game_score:.2f}", True, white)
    score_rect = score_text.get_rect()
    score_rect.centerx = width // 2  # Center horizontally
    score_rect.top = 20
    pygame.draw.rect(screen, white, score_rect.inflate(20, 10), 2)
    screen.blit(score_text, score_rect)


game_status = "Playing"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(black)  # Clear screen with black

    match game_status:
        case "Playing":
            draw_star()
            all_sprites.update()  # Update all sprites
            stone_playerbullet_hit = pygame.sprite.groupcollide(stones, player_bullets, False, False)  # Check for collisions between stones and player bullets
            if stone_playerbullet_hit:
                for stone in stone_playerbullet_hit:
                    # add score with the stone size
                    game_score += stone.radius
                    stone.reset_position()
            player_stone_hit = pygame.sprite.spritecollide(player, stones, False)  # Check for collisions between player and stones
            if player_stone_hit:
                # disable the stone
                stone = player_stone_hit[0]
                stone.reset_position()
                player.set_health_point(-1)
                player.flash_white()

            all_sprites.draw(screen)  # Draw all sprites
            draw_game_ui()
        case "End":
            draw_report_ui()

    pygame.display.flip()  # Update the display
    clock.tick(frame_per_seconds)  # Maintain 60 FPS


# Clean up and exit
pygame.mixer.quit()
pygame.quit()
