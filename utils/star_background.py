import pygame
import random
from utils.color import star_color

def init_star_particles(width, height, num_particles=20):
    """Initialize star particles with given screen dimensions"""
    return [(random.randint(0, width), random.randint(-height, 0), random_star_speed()) 
            for _ in range(num_particles)]

def draw_star(star_particles, screen, width, height):


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


def random_star_speed():
    return random.uniform(1, 30)
