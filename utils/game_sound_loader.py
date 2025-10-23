import pygame
import os

# load the sound files
def load_sound(file_path):
    try:
        sound = pygame.mixer.Sound(file_path)
        return sound
    except pygame.error as e:
        print(f"Unable to load sound file: {file_path}")
        raise SystemExit(e)

# Preload sound effects

shoot_sound = load_sound(os.path.join('assets/sounds', 'shoot.wav'))
explosion_sound = load_sound(os.path.join('assets/sounds', 'expl0.wav'))
powerup_sound = load_sound(os.path.join('assets/sounds', 'pow0.wav'))
shield_sound = load_sound(os.path.join('assets/sounds', 'shield.wav'))

def play_shoot_sound():
    shoot_sound.play()

def play_explosion_sound(): 
    explosion_sound.play()  

def play_powerup_sound():
    powerup_sound.play()    

def play_shield_sound():    
    shield_sound.play()

# background_music_path = os.path.join('assets/sounds', 'background_music.mp3')       

# def play_background_music():
#     try:
#         pygame.mixer.music.load(background_music_path)
#         pygame.mixer.music.set_volume(0.5)
#         pygame.mixer.music.play(-1)  # Loop indefinitely
#     except pygame.error as e:
#         print(f"Unable to load background music: {background_music_path}")
#         raise SystemExit(e)

# def stop_background_music():
#     pygame.mixer.music.stop()       

