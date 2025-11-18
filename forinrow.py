import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont("monospace", 75)
SMALL_FONT = pygame.font.SysFont("monospace", 20)

# Game mode: "PVP" for Player vs Player, "PVE" for Player vs AI
GAME_MODE = "PVE"  # Change to "PVP" for two players
SHOW_PROBABILITIES = True  # Set to True to show win probabilities

# Initialize mixer for music and sound
pygame.mixer.init()

# Load audio files from the assets folder (with error handling)
try:
    pygame.mixer.music.load('assets/background.mp3')
    win_sound = pygame.mixer.Sound('assets/win_sound.mp3')
    audio_enabled = True
except:
    audio_enabled = False
    print("Audio files not found. Continuing without sound.")

# Create the game board
def create_board():
    board = [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
    return board

# Draw the board
def draw_board(board, probabilities=None):
    # Clear the entire screen first
    screen.fill(BLACK)
    
    # Draw the blue board with holes
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    # Draw the pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    # Draw probabilities if enabled - in the top BLACK area, clearly visible
    if SHOW_PROBABILITIES and probabilities:
        for col, prob in enumerate(probabilities):
            if prob is not None:
                # Draw a semi-transparent background rectangle for better visibility
                rect_x = col * SQUARESIZE + 10
                rect_y = 20
                rect_width = SQUARESIZE - 20
                rect_height = 40
                
                # Draw background rectangle
                s = pygame.Surface((rect_width, rect_height))
                s.set_alpha(180)
                s.fill((50, 50, 50))
                screen.blit(s, (rect_x, rect_y))
                
                # Draw probability percentage with color coding
                if prob >= 70:
                    color = GREEN
                elif prob >= 40:
                    color = YELLOW
                else:
                    color = RED
                
                prob_text = SMALL_FONT.render(f"{int(prob)}%", 1, color)
                text_rect = prob_text.get_rect(center=(col*SQUARESIZE + SQUARESIZE//2, 40))
                screen.blit(prob_text, text_rect)
    
    pygame.display.update()

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def count_windows(board, piece):
    """Count favorable windows (sequences of 4 positions) for a piece"""
    score = 0
    opponent_piece = 1 if piece == 2 else 2
    
    # Score center column - VERY important strategically
    center_array = [board[r][COLUMN_COUNT//2] for r in range(ROW_COUNT)]
    center_count = center_array.count(piece)
    score += center_count * 6  # Doubled importance

    # Score horizontal
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT-3):
            window = [board[r][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            window = [board[r+i][c] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score positive diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative diagonal
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT-3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    """Evaluate a window of 4 positions"""
    score = 0
    opponent_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 1000  # Massively increased
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 50  # Much stronger offensive
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 10

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 80  # Much stronger defensive penalty
    elif window.count(opponent_piece) == 2 and window.count(0) == 2:
        score -= 5

    return score

def calculate_move_probabilities(board, piece):
    """Calculate win probability for each possible move with deep analysis"""
    probabilities = []
    opponent_piece = 1 if piece == 2 else 2
    
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            # Simulate the move
            temp_board = [row[:] for row in board]
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, piece)
            
            # Check for immediate win - HIGHEST PRIORITY
            if winning_move(temp_board, piece):
                probabilities.append(100.0)
                continue
            
            # Check if opponent can win on their next turn (MUST BLOCK)
            opponent_can_win = False
            opponent_winning_col = -1
            for c in range(COLUMN_COUNT):
                if is_valid_location(board, c):
                    test_board = [row[:] for row in board]
                    r = get_next_open_row(test_board, c)
                    drop_piece(test_board, r, c, opponent_piece)
                    if winning_move(test_board, opponent_piece):
                        opponent_can_win = True
                        opponent_winning_col = c
                        break
            
            # If opponent can win and this move doesn't block, very bad move
            if opponent_can_win:
                if col == opponent_winning_col:
                    probabilities.append(95.0)  # MUST block
                    continue
                else:
                    probabilities.append(5.0)  # Don't play elsewhere
                    continue
            
            # Look ahead: after AI's move, can opponent create a winning threat?
            opponent_threats = 0
            for c in range(COLUMN_COUNT):
                if is_valid_location(temp_board, c):
                    test_board = [row[:] for row in temp_board]
                    r = get_next_open_row(test_board, c)
                    drop_piece(test_board, r, c, opponent_piece)
                    
                    # Count how many ways opponent could win after that
                    opponent_wins = 0
                    for c2 in range(COLUMN_COUNT):
                        if is_valid_location(test_board, c2):
                            test_board2 = [row[:] for row in test_board]
                            r2 = get_next_open_row(test_board2, c2)
                            drop_piece(test_board2, r2, c2, opponent_piece)
                            if winning_move(test_board2, opponent_piece):
                                opponent_wins += 1
                    
                    if opponent_wins > 1:  # Double threat - very dangerous
                        opponent_threats += 10
                    elif opponent_wins == 1:
                        opponent_threats += 3
            
            # Calculate strategic score
            score = count_windows(temp_board, piece)
            opponent_score = count_windows(temp_board, opponent_piece)
            
            # Penalize moves that give opponent threats
            score -= opponent_threats * 20
            
            # Convert to probability (0-100)
            if score <= 0:
                probability = 10.0
            else:
                total = score + opponent_score + 10
                probability = (score / total) * 100
            
            # Bonus for creating multiple winning threats
            ai_threats = 0
            for c in range(COLUMN_COUNT):
                if is_valid_location(temp_board, c):
                    test_board = [row[:] for row in temp_board]
                    r = get_next_open_row(test_board, c)
                    drop_piece(test_board, r, c, piece)
                    if winning_move(test_board, piece):
                        ai_threats += 1
            
            if ai_threats >= 2:  # We create double threat - very good!
                probability = min(98.0, probability + 40)
            elif ai_threats == 1:
                probability = min(90.0, probability + 20)
            
            probabilities.append(max(10.0, min(99.0, probability)))
        else:
            probabilities.append(None)
    
    return probabilities

def ai_move(board):
    """AI makes a move based on deep strategic analysis"""
    probabilities = calculate_move_probabilities(board, 2)
    
    # Find valid columns
    valid_columns = [col for col in range(COLUMN_COUNT) if probabilities[col] is not None]
    
    if not valid_columns:
        return None
    
    # Get the best probability
    best_prob = max(probabilities[col] for col in valid_columns)
    
    # ALWAYS take winning moves (100%) or critical blocks (95%)
    if best_prob >= 95:
        best_cols = [col for col in valid_columns if probabilities[col] >= 95]
        return best_cols[0]  # Take the first one (deterministic for must-win/must-block)
    
    # For strategic moves, pick the absolute best 95% of the time
    sorted_cols = sorted(valid_columns, key=lambda col: probabilities[col], reverse=True)
    
    if random.random() < 0.95:
        return sorted_cols[0]  # Best move
    else:
        # Occasionally pick 2nd best for unpredictability
        return sorted_cols[min(1, len(sorted_cols)-1)]

# Game variables
board = create_board()
game_over = False
turn = 0

# Create the screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption(f"Connect Four - {'Player vs AI' if GAME_MODE == 'PVE' else 'Player vs Player'}")
draw_board(board)

def display_winner(player):
    label = FONT.render(f"Player {player} wins!", 1, RED if player == 1 else YELLOW)
    screen.blit(label, (40, 10))
    pygame.display.update()
    pygame.time.wait(3000)

# Main game loop
clock = pygame.time.Clock()

while not game_over:
    # Calculate probabilities for current player at the start of each frame
    if not game_over:
        current_player = 1 if turn == 0 else 2
        probabilities = calculate_move_probabilities(board, current_player)
        draw_board(board, probabilities)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Human player's turn (Player 1 or both players in PVP mode)
        if event.type == pygame.MOUSEBUTTONDOWN and (turn == 0 or GAME_MODE == "PVP"):
            posx = event.pos[0]
            col = int(posx // SQUARESIZE)

            if is_valid_location(board, col):
                # Start playing background music on the first click
                if audio_enabled and not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)

                row = get_next_open_row(board, col)
                current_player = 1 if turn == 0 else 2
                drop_piece(board, row, col, current_player)
                
                if winning_move(board, current_player):
                    draw_board(board)
                    if audio_enabled:
                        pygame.mixer.music.stop()
                        win_sound.play()
                    display_winner(current_player)
                    game_over = True

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)
    
    # AI's turn (only in PVE mode when it's Player 2's turn)
    if GAME_MODE == "PVE" and turn == 1 and not game_over:
        pygame.time.wait(500)  # Short delay for better UX
        
        col = ai_move(board)
        if col is not None and is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            
            if winning_move(board, 2):
                draw_board(board)
                if audio_enabled:
                    pygame.mixer.music.stop()
                    win_sound.play()
                display_winner(2)
                game_over = True
            
            turn += 1
            turn = turn % 2
            
            if game_over:
                pygame.time.wait(3000)
    
    clock.tick(30)  # 30 FPS