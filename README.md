# Connect Four – Streamlit Edition

This project is a Streamlit app with two play modes:

- Local 2-player (you and your friend on the same screen)
- You vs Bot (with difficulty levels)

## Features

- Streamlit web interface
- Local friend mode (2 players)
- Bot mode with `Easy`, `Medium`, `Hard`, `Hard+` (deeper search with time cap)
- Player name inputs
- Score tracker with `Best of 3` / `Best of 5`
- Undo last move (local friend mode)
- Undo in Vs Bot (reverts your move + bot reply)
- Smoother piece-drop animation
- Keyboard controls (`1..7` then Enter)
- Lightweight profile persistence (auto-save game and settings)
- Move log and threat hints (winning columns + danger columns)
- Win + draw detection (horizontal, vertical, diagonal)
- `New Round` and `Reset Match` controls

## Requirements

- Python 3.8+
- Streamlit

## Installation

From your project folder:

```bash
pip install streamlit
```

## Run

```bash
streamlit run forinrow.py
```

## Modes

### 1) Friend (Local 2 Players)

- Both players use the same app screen.
- Player 1 is `🔴`, Player 2 is `🟡`.
- You can set both player names.
- You can undo the last move.

### 2) Vs Bot

- You are `🔴`, bot is `🟡`.
- Choose difficulty in sidebar:
  - `Easy`: random moves
  - `Medium`: strong heuristic
  - `Hard`: minimax strategy
  - `Hard+`: deeper minimax with time cap for stronger play

## Match System

- Choose `Best of 3` or `Best of 5` in the sidebar.
- The first player to reach required wins takes the match.
- Draw rounds are tracked separately.

## Controls

- Mouse: choose a column and click `Drop Piece`
- Keyboard: type `1..7` then press Enter
- Undo (local mode): revert one move
- Undo (Vs Bot): revert one full cycle (you + bot)

## Files

- `forinrow.py`: Main Streamlit app
- `connect4/logic.py`: Board rules and win detection
- `connect4/ai.py`: Bot logic and difficulty levels
- `connect4/ui.py`: Board rendering UI + sound player
- `connect4/persistence.py`: Auto-save / restore profile state
