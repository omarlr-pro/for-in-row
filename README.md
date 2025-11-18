# Connect Four AI (Puissance 4) – Advanced Pygame Edition

A beautifully crafted Connect Four game built with Python and Pygame, featuring **intelligent AI opponent**, real-time probability analysis, smooth gameplay, colorful graphics, and immersive sound effects.

Experience the classic challenge enhanced with AI — can you outsmart the computer and align 4 discs before it does?

## ✨ Features

### 🎮 Game Modes
- **Player vs AI (PVE)** – Challenge an intelligent computer opponent with advanced strategic thinking
- **Player vs Player (PVP)** – Classic two-player mode for local multiplayer

### 🤖 Advanced AI System
- **Deep Strategic Analysis** – AI looks 2 moves ahead to predict and counter your strategy
- **Real-time Probability Display** – See win percentages for each column at the top of the board
- **Smart Decision Making**:
  - Detects and takes winning moves instantly
  - Never misses blocking your winning attempts
  - Creates double-threat scenarios to trap you
  - Prevents you from setting up multiple winning opportunities
  - Prioritizes center column control for strategic advantage

### 🎨 Visual Features
- **Dynamic Graphics** – Colorful board with smooth animations powered by Pygame
- **Color-Coded Probabilities**:
  - 🟢 **Green (70%+)** – Excellent move
  - 🟡 **Yellow (40-69%)** – Decent move
  - 🔴 **Red (<40%)** – Risky move
- **Semi-transparent Backgrounds** – Clear probability display without cluttering the board
- **Modern UI** – Clean layout with victory messages

### 🔊 Sound Integration
- **Background Music** – Plays continuously during gameplay
- **Victory Sound Effects** – Celebratory audio when a player wins
- **Graceful Fallback** – Game continues smoothly even if audio files are missing

### 🎯 Game Intelligence
- **Win Detection** – Automatic checks for horizontal, vertical, and diagonal wins
- **Strategic Evaluation** – Scores positions based on:
  - Center column dominance
  - Offensive opportunities (3-in-a-row, 2-in-a-row)
  - Defensive necessities (blocking opponent threats)
  - Future threat prevention

## 📦 Installation

Follow these steps to play the game locally:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/connect-four-ai-pygame.git
cd connect-four-ai-pygame
```

### 2. Install Requirements
Make sure you have Python 3.8+ installed, then install Pygame:
```bash
pip install pygame
```

### 3. Prepare the Assets (Optional)
Create a folder named `assets/` in the project directory and place these files inside:
```
assets/
 ├── background.mp3    # Background music
 └── win_sound.mp3     # Sound effect when a player wins
```
**Note:** The game will work without audio files — it automatically detects and continues if they're missing.

## 🚀 Running the Game

Simply run:
```bash
python connect_four_ai.py
```

Then click inside the game window and start playing against the AI!

## 🎮 How to Play

### Controls
- **Left-click** on any column to drop your piece
- Watch the **probability percentages** at the top to make strategic decisions
- The probabilities update in real-time showing your chances for each move

### Game Flow
- **Player 1 (Red/Human)** always goes first
- **Player 2 (Yellow/AI)** responds strategically after a brief delay
- First player to connect four discs in a row (horizontally, vertically, or diagonally) wins
- Victory message displays at the top with sound effects

### Strategy Tips
- 🎯 Pay attention to the probability percentages — higher is better!
- 🛡️ Block the AI when you see it creating threats
- ⚔️ Try to create "double threats" where you have two ways to win
- 🏰 Control the center columns for maximum flexibility

## ⚙️ Configuration

You can customize the game by editing these constants at the top of the file:

```python
# Switch between game modes
GAME_MODE = "PVE"  # "PVE" for Player vs AI, "PVP" for Player vs Player

# Toggle probability display
SHOW_PROBABILITIES = True  # Set to False to hide win percentages
```

## 🧠 AI Technical Details

### Strategic Analysis System
The AI uses a sophisticated evaluation system:

1. **Immediate Win Detection** – Always takes a winning move (100% priority)
2. **Critical Blocking** – Never misses blocking your winning attempts (95% priority)
3. **Threat Analysis** – Looks ahead to detect:
   - Double threats (multiple ways to win)
   - Single threats (one way to win next turn)
   - Opponent's potential threats after AI's move
4. **Position Evaluation** – Scores based on:
   - Center column control (×6 multiplier)
   - 3-in-a-row with space (50 points)
   - 2-in-a-row with spaces (10 points)
   - Blocking opponent's 3-in-a-row (−80 points penalty if missed)

### Probability Calculation
For each possible move, the AI:
- Simulates the move on a temporary board
- Evaluates all winning patterns (horizontal, vertical, diagonal)
- Calculates opponent's counter-threats
- Combines offensive and defensive scores
- Converts to a 0-100% probability scale
- Applies bonuses for creating threats and penalties for allowing opponent threats

### Decision Making
- 95% of the time: Picks the absolute best move
- 5% of the time: Picks 2nd best move for unpredictability
- Always deterministic for critical moves (winning or blocking)

## 📁 File Structure

```
connect-four-ai-pygame/
│
├── assets/
│   ├── background.mp3    # Optional background music
│   └── win_sound.mp3     # Optional victory sound
│
├── connect_four_ai.py    # Main game file with AI
└── README.md             # This documentation
```

## 🎯 Game Logic Overview

### Board Representation
- 2D array: 6 rows × 7 columns
- Values: 0 (empty), 1 (Player 1/Red), 2 (Player 2/Yellow)

### Core Functions
- `create_board()` – Initializes empty game board
- `draw_board()` – Renders board, pieces, and probabilities
- `drop_piece()` – Places piece at specified position
- `is_valid_location()` – Checks if column has space
- `get_next_open_row()` – Finds lowest available row in column
- `winning_move()` – Checks all four directions for 4-in-a-row
- `calculate_move_probabilities()` – AI's strategic analysis engine
- `count_windows()` – Evaluates position strength
- `evaluate_window()` – Scores individual 4-position sequences
- `ai_move()` – Selects best move based on probabilities

### Win Detection Algorithm
Checks all possible 4-in-a-row patterns:
- **Horizontal** – Scans each row left to right
- **Vertical** – Scans each column bottom to top  
- **Positive Diagonal (/)** – Scans bottom-left to top-right
- **Negative Diagonal (\\)** – Scans top-left to bottom-right

## 🔮 Future Improvements

Potential features for future versions:

### Gameplay Enhancements
- [ ] Animated piece drop with physics
- [ ] Undo/Redo moves
- [ ] Move history display
- [ ] Timer for each move
- [ ] Different board sizes (8×8, 9×9)

### AI Improvements
- [ ] Multiple difficulty levels (Easy, Medium, Hard, Expert)
- [ ] Minimax algorithm with alpha-beta pruning
- [ ] Monte Carlo Tree Search (MCTS)
- [ ] Neural network-based AI
- [ ] Learning AI that improves over time

### UI/UX Features
- [ ] Main menu with options
- [ ] Settings panel (sound volume, difficulty, colors)
- [ ] Restart button during game
- [ ] Save/Load game state
- [ ] Statistics tracking (wins, losses, draws)
- [ ] Leaderboard system
- [ ] Theme customization

### Multiplayer
- [ ] Online multiplayer via sockets
- [ ] Local network play
- [ ] Tournament mode
- [ ] Spectator mode

## 💻 Technical Stack

This project demonstrates:
- **Game Loop Architecture** – Continuous update and render cycle
- **Event-Driven Programming** – Mouse click handling
- **AI/ML Concepts** – Heuristic evaluation, lookahead search
- **Graphics Rendering** – Pygame drawing and animation
- **Audio Integration** – Music and sound effects
- **Modular Code Structure** – Clean, maintainable functions
- **Algorithm Implementation** – Win detection, pattern matching
- **Real-time Calculations** – Probability updates at 30 FPS

## 📋 Requirements

- **Python** 3.8 or higher
- **Pygame** library (latest version)

Install dependencies:
```bash
pip install pygame
```

## 📄 License

This project is open-source under the MIT License. Feel free to use, modify, and share it with proper attribution.

## 👨‍💻 Author

**Omar Laraje**  
Data Science & Software Engineering Student  
Rabat, Morocco

Connect with me:
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your Profile](https://linkedin.com/in/your-profile)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 

To contribute:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Built with **Python** and **Pygame**
- Inspired by the classic **Connect Four** board game (Puissance 4)
- AI algorithms based on game theory and heuristic search principles
- Special thanks to the Pygame community for excellent documentation

## 🎓 Educational Value

This project is perfect for learning:
- Game development fundamentals
- AI and decision-making algorithms
- Python programming best practices
- Event handling and user interaction
- Graphics and audio in games
- Strategic thinking and game theory

---

**🎮 Enjoy the game and see if you can beat the AI! May the best player win! 🏆**

*Challenge yourself against intelligent AI • Strategic probability analysis • Beautiful graphics • Immersive sound*
