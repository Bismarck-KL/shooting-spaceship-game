# Spaceship Game

## Overview

The Spaceship Game is a 2D arcade-style game developed using Pygame, where players control a spaceship and navigate through falling stones while shooting bullets to score points. The game features a vibrant visual experience with particle effects and a simple UI displaying health and score.

## Features

- Control a spaceship using keyboard inputs.
- Shoot bullets to destroy falling stones.
- Health system that decreases upon collision with stones.
- Restart functionality to try again after game over.
- Randomized falling stones and background stars.

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
    ├── start.py                # Start manu application file
    ├── main.py                 # Main application file
    ├── loading_screen.py       # Loading screen file
    ├── requirements.txt        # Python dependencies
    ├── assets/                 # Asset folder
        ├── image               # Image folder
        ├── sfx                 # Sound effect folder

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
- **Tutorials**: This project was developed following tutorials from YouTube, particularly those by [GrandmaCan -我阿嬤都會](https://youtu.be/61eX0bFAsYs?si=k2UWQ6V_wNKaspwT). 

Special thanks to them for their helpful guidance.


