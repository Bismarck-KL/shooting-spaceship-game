# Spaceship Game

## Overview

The Spaceship Game is a 2D arcade-style game developed using Pygame, featuring multiple game modes including single-player, cooperative PvE, and PvP gameplay. Players control spaceships to navigate through falling stones, shoot bullets, and compete or cooperate depending on the chosen mode. The game features vibrant visual effects, particle systems, and interactive gameplay mechanics.

## Features

- Multiple game modes (Single Player, Co-op PvE, and PvP)
- Dynamic spaceship controls with particle trail effects
- Automatic shooting system with custom bullet trajectories
- Protective shield system
- Health system with visual damage feedback
- Collision detection and explosion animations
- Randomized falling stones with rotation effects
- Animated star background
- Score tracking system
- Interactive game menu

## Controls

- **WASD Keys**: Move **Player 1**’s spaceship.
- **Arrow Keys**: Move **Player 2**’s spaceship.
- **Escape Key**: Exit the application.
- **Spacebar**: Restart the game after a game over.
- **Backspace**: Return to the game menu after a game over.


## Requirements

- Python 3.x
- Required libraries:
  - `pygame`

## Installation

1. Clone the repository or download the source code:

   ```sh
   git clone https://github.com/Bismarck-KL/shooting-spaceship-game.git
   cd shooting-spaceship-game
    ```

2. Install the required libraries:

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

  1. Ensure you are in the project directory with the virtual environment activated.
  2. Run the application:
     ```sh
     python start.py
     ```
  3. Use the following controls:
     - Arrow Keys: Control the spaceship movenment.
     - Space Key: Retry ater the game end.
     - Escape Key: Exit the application.

## File Structure

    shooting-spaceship-game/
    ├── start.py                # Main menu and game mode selection
    ├── main.py                 # Single player and PvE gameplay implementation
    ├── pvp.py                 # PvP mode gameplay implementation
    ├── color.py               # Color definitions
    ├── game_image_loader.py   # Asset loading utilities
    ├── loading_screen.py      # Loading screen implementation
    ├── requirements.txt       # Python dependencies
    ├── assets/               # Game resources
        ├── images/           # Sprite and visual assets
            ├── expl/        # Explosion animation frames
            ├── rock3.png    # Stone sprites
            ├── rock6.png    # Stone sprites
            ├── spaceship.png # Player spaceship sprite
        ├── sfx/            # Sound effect assets

## Dependencies

  Make sure to install the following dependencies using pip:
    * pygame

  You can install them by running:
  ```sh
  pip install pygame
  ```

## Acknowledgments

- **Images and Assets**: Some images and background assets were sourced are used under their respective licenses.
    - https://www.vecteezy.com/vector-art/49433251-pixel-art-space-rocket-illustration
    - https://www.vecteezy.com/png/56280614-pixel-art-space-ship-element-icon-isolated
- **Tutorials**: This project was developed following tutorials from YouTube, particularly those by [GrandmaCan -我阿嬤都會](https://youtu.be/61eX0bFAsYs?si=k2UWQ6V_wNKaspwT). 

Special thanks to them for their helpful guidance.


