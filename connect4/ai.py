import math
import random
import time

from .logic import (
    ROW_COUNT,
    COLUMN_COUNT,
    EMPTY,
    PLAYER_1,
    PLAYER_2,
    drop_piece,
    get_next_open_row,
    get_valid_locations,
    is_valid_location,
    winning_move,
    board_is_full,
)


def evaluate_window(window, piece):
    score = 0
    opponent = PLAYER_1 if piece == PLAYER_2 else PLAYER_2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 8
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 3

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 9

    return score


def score_position(board, piece):
    score = 0

    center_col = COLUMN_COUNT // 2
    center_array = [board[row][center_col] for row in range(ROW_COUNT)]
    score += center_array.count(piece) * 4

    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            window = [board[row][col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_window(window, piece)

    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    for row in range(3, ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def copy_board(board):
    return [row[:] for row in board]


def immediate_win_or_block(board, piece):
    valid_cols = get_valid_locations(board)

    for col in valid_cols:
        row = get_next_open_row(board, col)
        temp = copy_board(board)
        drop_piece(temp, row, col, piece)
        if winning_move(temp, piece):
            return col

    opponent = PLAYER_1 if piece == PLAYER_2 else PLAYER_2
    for col in valid_cols:
        row = get_next_open_row(board, col)
        temp = copy_board(board)
        drop_piece(temp, row, col, opponent)
        if winning_move(temp, opponent):
            return col

    return None


def minimax(board, depth, alpha, beta, maximizing):
    valid_cols = get_valid_locations(board)
    terminal = winning_move(board, PLAYER_1) or winning_move(board, PLAYER_2) or board_is_full(board)

    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, PLAYER_2):
                return None, 10_000_000
            if winning_move(board, PLAYER_1):
                return None, -10_000_000
            return None, 0
        return None, score_position(board, PLAYER_2)

    if maximizing:
        value = -math.inf
        best_col = random.choice(valid_cols)
        for col in valid_cols:
            row = get_next_open_row(board, col)
            temp = copy_board(board)
            drop_piece(temp, row, col, PLAYER_2)
            _, new_score = minimax(temp, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    value = math.inf
    best_col = random.choice(valid_cols)
    for col in valid_cols:
        row = get_next_open_row(board, col)
        temp = copy_board(board)
        drop_piece(temp, row, col, PLAYER_1)
        _, new_score = minimax(temp, depth - 1, alpha, beta, True)
        if new_score < value:
            value = new_score
            best_col = col
        beta = min(beta, value)
        if alpha >= beta:
            break
    return best_col, value


class SearchTimeout(Exception):
    pass


def minimax_timed(board, depth, alpha, beta, maximizing, deadline):
    if time.perf_counter() >= deadline:
        raise SearchTimeout()

    valid_cols = get_valid_locations(board)
    terminal = winning_move(board, PLAYER_1) or winning_move(board, PLAYER_2) or board_is_full(board)

    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, PLAYER_2):
                return None, 10_000_000
            if winning_move(board, PLAYER_1):
                return None, -10_000_000
            return None, 0
        return None, score_position(board, PLAYER_2)

    if maximizing:
        value = -math.inf
        best_col = random.choice(valid_cols)
        for col in valid_cols:
            if time.perf_counter() >= deadline:
                raise SearchTimeout()
            row = get_next_open_row(board, col)
            temp = copy_board(board)
            drop_piece(temp, row, col, PLAYER_2)
            _, new_score = minimax_timed(temp, depth - 1, alpha, beta, False, deadline)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    value = math.inf
    best_col = random.choice(valid_cols)
    for col in valid_cols:
        if time.perf_counter() >= deadline:
            raise SearchTimeout()
        row = get_next_open_row(board, col)
        temp = copy_board(board)
        drop_piece(temp, row, col, PLAYER_1)
        _, new_score = minimax_timed(temp, depth - 1, alpha, beta, True, deadline)
        if new_score < value:
            value = new_score
            best_col = col
        beta = min(beta, value)
        if alpha >= beta:
            break
    return best_col, value


def pick_ai_move(board, level):
    valid_cols = get_valid_locations(board)
    if not valid_cols:
        return None

    forced = immediate_win_or_block(board, PLAYER_2)
    if forced is not None:
        return forced

    if level == "Easy":
        return random.choice(valid_cols)

    if level == "Medium":
        if random.random() < 0.25:
            return random.choice(valid_cols)

        best_score = -10**9
        best_cols = []
        for col in valid_cols:
            row = get_next_open_row(board, col)
            temp = copy_board(board)
            drop_piece(temp, row, col, PLAYER_2)
            score = score_position(temp, PLAYER_2)
            if score > best_score:
                best_score = score
                best_cols = [col]
            elif score == best_score:
                best_cols.append(col)
        return random.choice(best_cols)

    if level == "Hard":
        col, _ = minimax(board, depth=5, alpha=-math.inf, beta=math.inf, maximizing=True)
        if col is not None and is_valid_location(board, col):
            return col
        return random.choice(valid_cols)

    if level == "Hard+":
        deadline = time.perf_counter() + 1.15
        best_col = random.choice(valid_cols)

        for depth in [5, 6, 7, 8]:
            try:
                col, _ = minimax_timed(board, depth=depth, alpha=-math.inf, beta=math.inf, maximizing=True, deadline=deadline)
                if col is not None and is_valid_location(board, col):
                    best_col = col
            except SearchTimeout:
                break

        return best_col

    col, _ = minimax(board, depth=4, alpha=-math.inf, beta=math.inf, maximizing=True)
    if col is not None and is_valid_location(board, col):
        return col
    return random.choice(valid_cols)
