import pygame 
import random
import os

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()
running = True

frame_per_seconds = 60

# Initialize pygame
pygame.init()

# image
try:
    spaceship_img = pygame.image.load(os.path.join("assets/images/","spaceship.png")).convert()
except pygame.error as e:
    print(f"Error loading spaceship image file: {e}")

stone_img = [None, None]
try:
    stone_img[0] = pygame.image.load(os.path.join("assets/images/","rock3.png")).convert()
    stone_img[1] = pygame.image.load(os.path.join("assets/images/","rock6.png")).convert()
except pygame.error as e:
    print(f"Error loading stone image file: {e}")   

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


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((3, 5))  # Small particle size
        self.image.fill((255, 165, 0))  # Orange color for the fire effect
        self.rect = self.image.get_rect(center=(x, y))
        
        # Set a random velocity
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(1, 2)  # Move down
        self.lifetime = 20  # Lifetime in frames

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.lifetime -= 1

        # Fade out effect
        if self.lifetime <= 0:
            self.kill()  # Remove the particle when its lifetime is over

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, spaceship_img, width, height, speed=4, shooting_speed=200):
        super().__init__()

        # Load and scale the spaceship image
        self.image = pygame.transform.scale(spaceship_img, (50, 50))
        self.image.set_colorkey((255, 255, 255))  # Set white as the transparent color
        
        self.rect = self.image.get_rect(center=(width // 2, height // 2))
        
        # Player attributes
        self.speed = speed
        self.shooting_speed = shooting_speed  # Shooting speed in milliseconds
        self.last_shot_time = 0
        self.health_point = 3
        
        # Flashing attributes
        self.flashing = False  # Track if flashing is active
        self.flash_start_time = 0  # Track when the flash started

        self.shield = None
        self.activate_shield()

        self.particles = pygame.sprite.Group()

    def update(self):
        """Update player state."""
        global screen

        self.handle_movement()
        self.handle_shooting()
        self.handle_flashing()
        self.generate_particles()  # Generate particles
        self.particles.update()  # Update particles
        self.particles.draw(screen)

    def handle_movement(self):
        """Handle player movement based on key presses."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Move left
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[pygame.K_d]:  # Move right
            self.rect.x += self.speed
            if self.rect.right > width:
                self.rect.right = width
        if keys[pygame.K_w]:  # Move up
            self.rect.y -= self.speed
            if self.rect.top < 0:
                self.rect.top = 0
        if keys[pygame.K_s]:  # Move down
            self.rect.y += self.speed
            if self.rect.bottom > height:
                self.rect.bottom = height

    def handle_shooting(self):
        """Handle shooting mechanics."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shooting_speed:
            self.last_shot_time = current_time  # Update the last shot time
            self.shoot()

    def handle_flashing(self):
        """Handle flashing effect when hit."""
        current_time = pygame.time.get_ticks()
        if self.flashing:
            if current_time - self.flash_start_time < 750:  # Flashing duration
                if (current_time // 100) % 2 == 0:  # Flash every 100 ms
                    self.image.fill((255, 255, 255))  # Flash white
                else:
                    self.reset_image()  # Reset to original
            else:
                self.flashing = False  # Stop flashing
                self.reset_image()  # Ensure it resets to original

    def reset_image(self):
        """Reset the player image to the original."""
        self.image = pygame.transform.scale(spaceship_img, (50, 50))  # Reset to original size
        self.image.set_colorkey((255, 255, 255))  # Reset transparency

    def shoot(self):
        """Shoot a bullet."""
        bullet = Bullet(self.rect.centerx, self.rect.top, 'player')
        all_sprites.add(bullet)
        player_bullets.add(bullet)

    def set_health_point(self, point):
        """Update health points."""
        global game_status
        self.health_point += point
        if self.health_point <= 0:
            game_status = "End"

    def flash_white(self):
        """Trigger white flash effect."""
        self.flashing = True
        self.flash_start_time = pygame.time.get_ticks()

    def generate_particles(self):
        """Generate particles at the tail of the spaceship."""
        if random.randint(0, 2) == 0:  # Adjust frequency of particle generation
            particle = Particle(self.rect.centerx, self.rect.bottom)
            self.particles.add(particle)

    def activate_shield(self):
        """Activate a shield around the player."""
        if self.shield == None:
            self.shield = Shield(self)
            all_sprites.add(self.shield)
            player_shield.add(self.shield)

    def deactivate_shield(self):
        """Deactivate a shield around the player."""
        if not self.shield == None:
            all_sprites.remove(self.shield)
            player_shield.remove(self.shield)
            self.shield = None

# Shiled class
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
player_shield = pygame.sprite.Group()
player = Player(spaceship_img, width, height)
all_sprites.add(player)
for _ in range(8):
    stone = Stone()
    all_sprites.add(stone)
    stones.add(stone)

game_status = "Playing"
game_score = 0


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

    try_again_text = game_font.render("Press space to try again",True,white)
    try_again_rect = try_again_text.get_rect()
    try_again_rect.center = (width // 2, height // 2)
    screen.blit(try_again_text, try_again_rect)

def try_again():

    global game_status, game_score, player, stones, player_bullets

    # Remove old stones
    for stone in stones:
        stone.kill()  # Remove stone from all groups
    # Remove old bullets
    for bullet in player_bullets:
        bullet.kill()  # Remove bullet from all groups
    stones.empty()
    player_bullets.empty()
    player.kill()
    

    stones = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    player = Player(spaceship_img, width, height)
    all_sprites.add(player)
    for _ in range(8):
        stone = Stone()
        all_sprites.add(stone)
        stones.add(stone)

    game_status = "Playing"
    game_score = 0



while running:

    # print(game_status)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                if game_status == "End":
                    try_again()

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
            shield_stone_hit = pygame.sprite.groupcollide(stones, player_shield, False,False)
            if shield_stone_hit:
                for stone in shield_stone_hit:
                    # stone = shield_stone_hit[0]
                    stone.reset_position()
                    player.deactivate_shield()

            
            all_sprites.draw(screen)  # Draw all sprites
            draw_game_ui()
        case "End":
            draw_report_ui()

    pygame.display.flip()  # Update the display
    clock.tick(frame_per_seconds)  # Maintain 60 FPS


# Clean up and exit
pygame.mixer.quit()
pygame.quit()
