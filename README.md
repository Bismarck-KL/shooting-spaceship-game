# Spaceship Game

A small 2D arcade-style spaceship game built with Pygame. Dodge and destroy falling stones, collect power-ups, and play solo or against a friend.

## Quick summary

- Languages: Python 3
- Main library: pygame
- Game modes: Single-player PvE (default), Co-op/Multiple-player PvE, and PvP
- Entry point / menu: `start.py` — run this to pick a mode and start the game

## Features

- Single-player PvE and local 2-player modes (co-op PvE and PvP).
- Automatic shooting by players with configurable shoot rate and power-ups.
- Particle effects for ships and animated star background.
- Shields, health, and visual feedback when players are hit.
- Explosions and sound effects for shooting, shield, and destruction.
- Random power-up drops from destroyed stones.

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

1. Install Python 3.8+ (3.10/3.11 recommended).
2. (Optional) Create and activate a virtual environment.

On Windows PowerShell:

```powershell
python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the game

From the project directory run the menu script (recommended):

```powershell
python start.py
```

The `main.py` script also accepts a command-line argument to choose a mode. Example:

```powershell
python main.py multiple_player_pve
```

## Project structure (important files)

- `start.py`              — minimal menu / launcher
- `main.py`               — single-player and co-op PvE gameplay
- `pvp.py`                — local PvP gameplay
- `game_image_loader.py`  — loads images used by the game
- `game_sound_loader.py`  — plays short sfx used in the game
- `color.py`              — color constants
- `stone.py`              — falling stone (enemy) implementation
- `skill.py`              — power-up items (heal, shield, speed, shoot-speed)
- `explosion.py`          — explosion animation sprites
- `star_background.py`    — animated starfield background
- `assets/images/`        — image assets (spaceship, rocks, explosion frames)
- `assets/sounds/`        — sound effects (shoot, explode, power-up, shield)

## Dependencies

The required dependency is listed in `requirements.txt`:

- pygame

Install with:

```powershell
pip install -r requirements.txt
```

## Known issues and notes

- Controls and behavior are local-only (no network multiplayer).
- The game uses automatic shooting; there is no manual fire button.
- On some systems pygame may require additional system packages (e.g., SDL). If you see audio or display errors, ensure your Python and pygame install are compatible with your OS.
- If `start.py` is not launching on your system, run the desired mode (`main.py` or `pvp.py`) directly.

## Assets and attribution

Assets are included in the `assets/` folder. Some images and tutorial guidance were adapted from online resources and tutorials. See these references used during development:

- Tutorial (inspiration/source): GrandmaCan - 我阿嬤都會 (YouTube) — https://youtu.be/61eX0bFAsYs
- Vector / pixel assets used under their respective licenses from vecteezy and other free asset sites. Check the `assets/` files for original filenames and metadata.

If you are the owner of any of the assets and want them removed or credited differently, open an issue or contact the repo owner.

## Contributing

Small fixes, bug reports, and PRs are welcome. If you open a PR, please:

- Keep changes focused (one feature / fix per PR).
- Run and verify the game runs locally.
- Add a brief description of the change in the PR message.

## License

This project does not include a license file. If you want to release it under an open-source license, add a `LICENSE` file at the repository root.

## Troubleshooting

- Pygame import errors: verify `pip show pygame` and your active Python interpreter.
- Display or audio issues: try upgrading/downgrading pygame to a compatible version for your platform.
- If the game window opens but remains black or crashes, check the terminal output for Python exceptions and share them when opening an issue.

---

Made for learning and small local multiplayer fun. Have ideas or found bugs? Create an issue or submit a PR.


