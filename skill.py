#  skill class, create after player destroy the stone, and feature different skills to help player
import pygame
from color import green, red, blue, yellow
import random
import os
# Skill types
SKILL_TYPES = { 
    'heal': {'color': green }, #add one helth point
    'speed_boost': {'color': blue}, #increase speed
    'shoot_speed_boost': {'color': yellow}, #increase shooting speed
    'shield': {'color': red} #temporary invincibility
}

class Skill(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height,start_position_x,start_position_y, game_mode_id,player_id):
        super().__init__()
        self.game_mode_id = game_mode_id
        self.player_id = player_id
        self.screen_width = screen_width
        self.screen_height = screen_height
        skill_type = random.choice(list(SKILL_TYPES.keys()))
        self.skill_type = skill_type
        self.color = SKILL_TYPES[skill_type]['color']
        self.radius = 10
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = start_position_x
        self.rect.y = start_position_y
        self.speedy = random.randint(1, 4)

    def update(self):

        if self.game_mode_id <2 :  # PvE mode
            self.rect.y += self.speedy
            if self.rect.top > self.screen_height:
                self.kill()  # Remove the skill if it goes off the screen
        else:  # PvP mode
            if self.player_id == 1:
                self.rect.y += self.speedy
                if self.rect.top > self.screen_height:
                    self.kill()  # Remove the skill if it goes off the screen
            else:
                self.rect.y -= self.speedy
                if self.rect.bottom < 0:
                    self.kill()  # Remove the skill if it goes off the screen

