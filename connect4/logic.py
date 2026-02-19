ROW_COUNT = 6
COLUMN_COUNT = 7
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2


def create_board():
    return [[EMPTY for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == EMPTY


def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]


def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == EMPTY:
            return row
    return None


def board_is_full(board):
    return all(board[ROW_COUNT - 1][col] != EMPTY for col in range(COLUMN_COUNT))


def find_winning_columns(board, piece):
    winning_cols = []
    for col in get_valid_locations(board):
        row = get_next_open_row(board, col)
        if row is None:
            continue
        temp_board = [r[:] for r in board]
        drop_piece(temp_board, row, col, piece)
        if winning_move(temp_board, piece):
            winning_cols.append(col)
    return winning_cols


def winning_move(board, piece):
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if (
                board[row][col] == piece
                and board[row][col + 1] == piece
                and board[row][col + 2] == piece
                and board[row][col + 3] == piece
            ):
                return True

    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if (
                board[row][col] == piece
                and board[row + 1][col] == piece
                and board[row + 2][col] == piece
                and board[row + 3][col] == piece
            ):
                return True

    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT - 3):
            if (
                board[row][col] == piece
                and board[row + 1][col + 1] == piece
                and board[row + 2][col + 2] == piece
                and board[row + 3][col + 3] == piece
            ):
                return True

    for col in range(COLUMN_COUNT - 3):
        for row in range(3, ROW_COUNT):
            if (
                board[row][col] == piece
                and board[row - 1][col + 1] == piece
                and board[row - 2][col + 2] == piece
                and board[row - 3][col + 3] == piece
            ):
                return True

    return False
