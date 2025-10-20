import pygame 
import random
import os
import sys
import subprocess

# Import colors and images
from color import *
from game_image_loader import load_assets

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spaceship Game - PvP Mode")
clock = pygame.time.Clock()
running = True

frame_per_seconds = 60

# Initialize pygame
pygame.init()

# Load images
spaceship_img, spaceship_img_2, stone_img, expl_anim = load_assets()

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
    def __init__(self, x, y, player_id):
        super().__init__()
        self.image = pygame.Surface((3, 5))  # Small particle size
        self.image.fill((255, 165, 0))  # Orange color for the fire effect
        self.rect = self.image.get_rect(center=(x, y))
        
        # Set a random velocity
        if player_id == 0:
            self.velocity_x = random.uniform(-1, -2)  # Move left
        else:
            self.velocity_x = random.uniform(1, 2)  # Move right

        self.velocity_y = random.uniform(-1, 1)  # Move down

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
    def __init__(self, spaceship_img, width, height, player_id, speed=4, shooting_speed=800):
        super().__init__()

        # Load and scale the spaceship image
        self.image = pygame.transform.scale(spaceship_img, (50, 50))
        if player_id == 0:
            self.image.set_colorkey(white)  # Set white as the transparent color
        else:
            self.image.set_colorkey(black)  # Set black as the transparent color

        # Set the initial position of the spaceship as the bottom center of the screen
        self.rect = self.image.get_rect()
        if player_id == 0:  # Player 1
            self.rect.center = (width // 4, height // 2)    
            # rotate the image -90 degree
            self.image = pygame.transform.rotate(self.image, -90)
        else:  # multiplayer mode       
            self.rect.center = (3 * width // 4, height // 2)
            # rotate the image 90 degree
            self.image = pygame.transform.rotate(self.image, 90)

        # Player attributes
        self.player_id = player_id
        self.speed = speed
        self.shooting_speed = shooting_speed  # Shooting speed in milliseconds
        self.last_shot_time = 0
        self.health_point = 3
        
        # Flashing attributes
        self.flashing = False  # Track if flashing is active
        self.flash_start_time = 0  # Track when the flash started

        self.shield = None
        # self.activate_shield()

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

        if self.player_id == 0:  # Player 1 controls
            if keys[pygame.K_a]:  # Move left
                self.rect.x -= self.speed
                if self.rect.left < 0:
                    self.rect.left = 0
            if keys[pygame.K_d]:  # Move right
                self.rect.x += self.speed
                if self.rect.right > width/3:
                    self.rect.right = width/3
            if keys[pygame.K_w]:  # Move up
                self.rect.y -= self.speed
                if self.rect.top < 0:
                    self.rect.top = 0
            if keys[pygame.K_s]:  # Move down
                self.rect.y += self.speed
                if self.rect.bottom > height:
                    self.rect.bottom = height
        else:  # Player 2 controls
            if keys[pygame.K_LEFT]:  # Move left
                self.rect.x -= self.speed
                if self.rect.left < width*2/3:
                    self.rect.left = width*2/3
            if keys[pygame.K_RIGHT]:  # Move right
                self.rect.x += self.speed
                if self.rect.right > width:
                    self.rect.right = width
            if keys[pygame.K_UP]:  # Move up
                self.rect.y -= self.speed
                if self.rect.top < 0:
                    self.rect.top = 0
            if keys[pygame.K_DOWN]:  # Move down
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
                    if self.player_id == 0:
                        self.image.fill((white))  # Flash white
                    else:
                        self.image.fill((black))  # Flash black
                else:
                    self.reset_image()  # Reset to original
            else:
                self.flashing = False  # Stop flashing
                self.reset_image()  # Ensure it resets to original

    def reset_image(self):
        """Reset the player image to the original."""
        if self.player_id == 0:
            self.image = pygame.transform.scale(spaceship_img, (50, 50))  # Reset to original size
            self.image.set_colorkey(white)  # Reset transparency
            # rotate the image -90 degree
            self.image = pygame.transform.rotate(self.image, -90)
        else:
            self.image = pygame.transform.scale(spaceship_img_2, (50, 50))  # Reset to original size
            self.image.set_colorkey(black)  # Reset transparency
            # rotate the image 90 degree
            self.image = pygame.transform.rotate(self.image, 90)

    def shoot(self):
        """Shoot a bullet."""

        bullet = Bullet(self.rect.right if self.player_id == 0 else self.rect.left, self.rect.centery, 'player',self.player_id)
        all_sprites.add(bullet)
        player_bullets.add(bullet)

    def set_health_point(self, point):
        """Update health points."""
        global game_status
        self.health_point += point
        if self.health_point <= 0:
            self.health_point = 0
            self.kill()
        # check_health()

    def flash_white(self):
        """Trigger white flash effect."""
        self.flashing = True
        self.flash_start_time = pygame.time.get_ticks()

    def generate_particles(self):
        """Generate particles at the tail of the spaceship."""
        if random.randint(0, 2) == 0:  # Adjust frequency of particle 
            if self.player_id == 0:
                particle = Particle(self.rect.left, self.rect.centery,self.player_id)
            else:
                particle = Particle(self.rect.right, self.rect.centery,self.player_id)
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

# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

# Stone class 
class Stone(pygame.sprite.Sprite):
    def reset_position(self):
        # some stones may appear partially off-screen
        self.rect.x = random.uniform(width/3, width*2/3 - self.size) 
        self.rect.y = random.randint(-100, height + 100)
        self.speedy = random.randint(-6,6)
        #  Ensure the stone is moving downwards if speedy is 0
        if self.speedy ==0:
            self.speedy = 1  
    def __init__(self):
        super().__init__()
        self.image_ori = random.choice(stone_img)
        self.image_ori.set_colorkey(black)
        self.image = self.image_ori.copy()
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
        self.size = random.randint(20,30)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 /2
        # pygame.draw.circle(self.image,red,self.rect.center,self.radius) #Debug rendering
        self.reset_position()    

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.top > height or self.rect.bottom < 0:
            self.reset_position() 


    def rotate(self):   
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, type, player_id):
        super().__init__()
        self.image = pygame.Surface((5, 10))

        self.player_id = player_id
        if type == 'player':

            self.image.fill(yellow if player_id == 0 else blue)  # Yellow bullet for player
            self.speedy = 0
            self.speedx = 10 if player_id == 0 else -10


        else:    
            self.image.fill(red)  # Red bullet for enemy
            self.speedy = 5

        self.type = type
        self.rect = self.image.get_rect()
        # rotate the image 90 degree if it is a player bullet
        if type == 'player':
            self.image = pygame.transform.rotate(self.image, 90)
            
        self.rect.center = (x, y)

    def update(self):
        self.rect.y += self.speedy if hasattr(self, 'speedy') else 0
        self.rect.x += self.speedx if hasattr(self, 'speedx') else 0
        if self.rect.bottom < 0 or self.rect.top > height:
            self.kill()  # Remove the bullet if it goes off-screen

# Create sprite groups
all_sprites = pygame.sprite.Group()
stones = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
player_shield = pygame.sprite.Group()
players_group = pygame.sprite.Group()
player_1 = Player(spaceship_img, width, height, 0)
players_group.add(player_1)
player_2 = Player(spaceship_img_2, width, height, 1)
players_group.add(player_2)
all_sprites.add(players_group)
 
for _ in range(8):
    stone = Stone()
    all_sprites.add(stone)
    stones.add(stone)

game_status = "Playing"


# Font setup
game_font = pygame.font.Font(None, 24) 
def draw_game_ui():
    global game_status

    player_health_text  = game_font.render(f"{player_1.health_point}", True, white)
    player_health_rect = player_health_text.get_rect(topleft = (20, 20))
    pygame.draw.rect(screen, white, player_health_rect.inflate(20, 10), 2)
    screen.blit(player_health_text, player_health_rect)

    player_2_health_text  = game_font.render(f"{player_2.health_point}", True, white)
    player_2_health_rect = player_2_health_text.get_rect(topleft = (width-30,20))
    pygame.draw.rect(screen, white, player_2_health_rect.inflate(20, 10), 2)
    screen.blit(player_2_health_text, player_2_health_rect)

def draw_report_ui():

    # First line
    try_again_text1 = game_font.render("Press space to try again", True, white)
    try_again_rect1 = try_again_text1.get_rect()
    try_again_rect1.centerx = width // 2
    try_again_rect1.centery = height // 2 - 15  # Offset up a bit
    
    # Second line
    try_again_text2 = game_font.render("Backspace to return to menu", True, white)
    try_again_rect2 = try_again_text2.get_rect()
    try_again_rect2.centerx = width // 2
    try_again_rect2.centery = height // 2 + 15  # Offset down a bit
    
    # Draw both lines
    screen.blit(try_again_text1, try_again_rect1)
    screen.blit(try_again_text2, try_again_rect2)

def try_again():

    global game_status, game_score, player_1, player_2, stones, player_bullets, players_group

    # Remove old stones
    for stone in stones:
        stone.kill()  # Remove stone from all groups
    # Remove old bullets
    for bullet in player_bullets:
        bullet.kill()  # Remove bullet from all groups
    stones.empty()
    player_bullets.empty()
    if not player_1 == None:
        player_1.kill()

    if not player_2 == None:
        player_2.kill()

    stones = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    players_group = pygame.sprite.Group()
    player_1 = Player(spaceship_img, width, height, 0)
    players_group.add(player_1)
    player_2 = Player(spaceship_img, width, height, 1)
    players_group.add(player_2)
    all_sprites.add(players_group)
    for _ in range(8):
        stone = Stone()
        all_sprites.add(stone)
        stones.add(stone)

    game_status = "Playing"


while running:

    # print(game_status)
    # print(game_status)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_status == "End":
                if event.key == pygame.K_SPACE:
                    try_again()
                elif event.key == pygame.K_BACKSPACE:
                    subprocess.Popen(["python", "start.py"])  # Start main game script
                    running = False  # Close current script
                    
    screen.fill(black)  # Clear screen with black

    match game_status:
        case "Playing":
            draw_star()
            all_sprites.update()  # Update all sprites
            stone_playerbullet_hit = pygame.sprite.groupcollide(stones, player_bullets, False, False)  # Check for collisions between stones and player bullets
            if stone_playerbullet_hit:
                for stone in stone_playerbullet_hit:
                    # show explosion
                    expl = Explosion(stone.rect.center, 'sm')
                    all_sprites.add(expl)
                    # add score with the stone size
                    
                    stone.reset_position()

            player_stone_hit = pygame.sprite.groupcollide(stones, players_group, False, False)
            if player_stone_hit:
                for stone,players in player_stone_hit.items():
                    stone.reset_position()
                    # show explosion
                    expl = Explosion(stone.rect.center, 'lg')
                    all_sprites.add(expl)
                    for player in players:
                        player.set_health_point(-1)
                        player.flash_white()   

            shield_stone_hit = pygame.sprite.groupcollide(stones, player_shield, False,False)
            if shield_stone_hit:
                for stone,shields in shield_stone_hit.items():
                    # show explosion
                    expl = Explosion(stone.rect.center, 'sm')
                    all_sprites.add(expl)
                    stone.reset_position()
                    for shield in shields:
                        shield.player.deactivate_shield()

            player_bullet_hit = pygame.sprite.groupcollide(player_bullets, players_group, False, False)
            if player_bullet_hit:
                for bullet,players in player_bullet_hit.items():
                    for player in players:
                        if not (bullet.player_id == player.player_id):  # only hit the other player
                            # show explosion
                            expl = Explosion(bullet.rect.center, 'sm')
                            all_sprites.add(expl)
                            bullet.kill()
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
