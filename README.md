# Connect Four (Puissance 4) – Pygame Edition

A beautifully crafted Connect Four game built with Python and Pygame, featuring smooth gameplay, colorful graphics, and immersive sound effects.

Experience the classic two-player challenge — align 4 discs of your color before your opponent does!

## Features

- **Classic Gameplay** – Two players take turns dropping discs into the board
- **Dynamic Graphics** – Colorful board and smooth animations powered by Pygame
- **Sound Integration** – Background music and victory sound effects enhance the experience
- **Win Detection** – Automatic checks for horizontal, vertical, and diagonal wins
- **Modern UI** – Clean layout with a clear "Player X wins!" message at the top



## Installation

Follow these steps to play the game locally:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/connect-four-pygame.git
cd connect-four-pygame
```

### 2. Install Requirements

Make sure you have Python 3.8+ installed, then install Pygame:

```bash
pip install pygame
```

### 3. Prepare the Assets

Create a folder named `assets/` in the project directory and place these files inside:

```
assets/
 ├── background.mp3    # Background music
 └── win_sound.mp3     # Sound effect when a player wins
```

You can use any `.mp3` files you like — just make sure they're named correctly.

## Running the Game

Simply run:

```bash
python connect_four.py
```

Then click inside the game window and start playing!

### How to Play

- Left-click to drop your piece in a column
- The game alternates turns between Player 1 (Red) and Player 2 (Yellow)
- First player to connect four discs in a row wins

## Game Logic Overview

Here's how it works behind the scenes:

- The board is represented as a 2D array (6 rows × 7 columns)
- Each click determines the column, and the program finds the next open row
- `winning_move()` checks all directions:
  - Horizontal
  - Vertical
  - Positive diagonal (\)
  - Negative diagonal (/)
- When a player wins:
  - Background music stops
  - Victory sound plays
  - "Player X wins!" is displayed

## File Structure

```
connect-four-pygame/
│
├── assets/
│   ├── background.mp3
│   └── win_sound.mp3
│
├── connect_four.py     # Main game file
└── README.md           # Documentation
```

## Future Improvements

Potential features that could be added:

- AI Mode (play against the computer using minimax or alpha-beta pruning)
- Animated piece drop
- Score saving system
- Main menu and restart button
- Replay functionality
- Difficulty levels for AI opponent

## Technical Details

This project demonstrates:

- Game loop logic
- Event handling
- Graphics rendering
- Sound integration
- Modular code structure
- Win condition algorithms

## Requirements

- Python 3.8 or higher
- Pygame library

## License

This project is open-source under the MIT License. Feel free to use, modify, and share it with proper attribution.

## Author

**Omar Laraje**  
Data Science & Software Engineering Student  
Rabat, Morocco

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## Acknowledgments

- Built with Python and Pygame
- Inspired by the classic Connect Four board game

---

**Enjoy the game and may the best player win!**
