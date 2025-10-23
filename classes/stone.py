# Class of stone objects
import pygame
import random   
from utils.color import black    
from utils.game_image_loader import stone_img_loader
import os

# Load images
stone_img = stone_img_loader()

# Stone class 
class Stone(pygame.sprite.Sprite):

    def reset_position(self):

        self.size = random.randint(20,100)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 /2

        # some stones may appear partially off-screen
        self.rect.x = random.randint(-100, self.screen_width - self.rect.width+100) 
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1,6)
        self.speedx = random.randint(-2, 2)

    def reset_pvp_position(self):

        self.rect.x = random.randint(int(self.screen_width/3) , int(self.screen_width*2/3) - int(self.rect.width)) 
        self.rect.y = random.randint(-100, self.screen_height + 100)
        self.speedy = random.randint(-6,6)
        #  Ensure the stone is moving downwards if speedy is 0
        if self.speedy ==0:
            self.speedy = 1  

    def __init__(self,screen_width,screen_height,game_mode_id):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Create the stone image
        self.image_ori = random.choice(stone_img)
        if self.image_ori is None:
            raise RuntimeError("Stone image not properly loaded")
            
        self.image_ori.set_colorkey(black)
        self.image = self.image_ori.copy()
        
        # Initialize stone properties
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
        self.game_mode_id = game_mode_id
        self.size = random.randint(20, 30)
        
        # Get the rectangle for the stone
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        
        # Set initial position based on game mode
        if game_mode_id < 2:  # PVE mode
            self.reset_position()    
        else:                 # PVP mode
            self.reset_pvp_position()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.game_mode_id <2:  # PVE mode
            self.rect.x += self.speedx
            if self.rect.top > self.screen_height:
                self.reset_position()
        else:                    # PVP mode
            if self.rect.top > self.screen_height or self.rect.bottom < 0:
                self.reset_pvp_position()

    def rotate(self):   
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
