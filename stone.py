# Class of stone objects
import pygame
import random   
from color import black    

# Stone class 
class Stone(pygame.sprite.Sprite):
    def reset_position(self):
        # some stones may appear partially off-screen
        self.rect.x = random.randint(-100, self.screen_width - self.rect.width+100) 
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1,6)
        self.speedx = random.randint(-2, 2)
    def __init__(self,stone_img,screen_width,screen_height):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height  
        self.image_ori = random.choice(stone_img)
        self.image_ori.set_colorkey(black)
        self.image = self.image_ori.copy()
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
        self.size = random.randint(20,100)
        # self.image = pygame.Surface((self.size, self.size))
        # self.image.fill(brown)  # Brown stone
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 /2
        # pygame.draw.circle(self.image,red,self.rect.center,self.radius) #Debug rendering
        self.reset_position()    

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > self.screen_height:
            self.reset_position() 

    def rotate(self):   
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
