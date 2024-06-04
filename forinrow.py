import pygame
import sys

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
FONT = pygame.font.SysFont("monospace", 75)

# Initialize mixer for music and sound
pygame.mixer.init()

# Load audio files from the assets folder
pygame.mixer.music.load('assets/background.mp3')
win_sound = pygame.mixer.Sound('assets/win_sound.mp3')

# Create the game board
def create_board():
    board = [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
    return board

# Draw the board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
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

# Game variables
board = create_board()
game_over = False
turn = 0

# Create the screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")
draw_board(board)

def display_winner(player):
    label = FONT.render(f"Player {player} wins!", 1, RED if player == 1 else YELLOW)
    screen.blit(label, (40, 10))
    pygame.display.update()
    pygame.time.wait(3000)

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            col = int(posx // SQUARESIZE)

            if is_valid_location(board, col):
                # Start playing background music on the first click
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)

                row = get_next_open_row(board, col)
                if turn == 0:
                    drop_piece(board, row, col, 1)
                    if winning_move(board, 1):
                        draw_board(board)
                        pygame.mixer.music.stop()
                        win_sound.play()
                        display_winner(1)
                        game_over = True
                else:
                    drop_piece(board, row, col, 2)
                    if winning_move(board, 2):
                        draw_board(board)
                        pygame.mixer.music.stop()
                        win_sound.play()
                        display_winner(2)
                        game_over = True

                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)
