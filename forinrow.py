import time
import uuid

import streamlit as st

from connect4.ai import pick_ai_move
from connect4.logic import (
    COLUMN_COUNT,
    PLAYER_1,
    PLAYER_2,
    board_is_full,
    create_board,
    drop_piece,
    find_winning_columns,
    get_next_open_row,
    is_valid_location,
    winning_move,
)
from connect4.persistence import load_profile_state, save_profile_state
from connect4.ui import render_board, render_sound_player


MODE_LOCAL = "Friend (Local 2 Players)"
MODE_BOT = "Vs Bot"


def get_or_create_profile_id():
    pid = st.query_params.get("pid")
    if isinstance(pid, list):
        pid = pid[0]

    if not pid:
        pid = uuid.uuid4().hex[:12]
        st.query_params["pid"] = pid

    return pid


def load_profile_once(profile_id):
    if st.session_state.get("_loaded_profile") == profile_id:
        return

    saved = load_profile_state(profile_id)
    for key, value in saved.items():
        st.session_state[key] = value

    st.session_state._loaded_profile = profile_id


def persist_profile(profile_id):
    save_profile_state(profile_id, st.session_state)


def setup_sound_defaults():
    st.session_state.setdefault("sound_enabled", True)
    st.session_state.setdefault("sound_drop", True)
    st.session_state.setdefault("sound_win", True)
    st.session_state.setdefault("sound_draw", True)
    st.session_state.setdefault("mute", False)
    st.session_state.setdefault("sound_event", "none")
    st.session_state.setdefault("sound_nonce", 0)


def set_sound_event(event_name):
    if not st.session_state.get("sound_enabled", True):
        return

    if event_name == "drop" and not st.session_state.get("sound_drop", True):
        return
    if event_name == "win" and not st.session_state.get("sound_win", True):
        return
    if event_name == "draw" and not st.session_state.get("sound_draw", True):
        return

    st.session_state.sound_event = event_name
    st.session_state.sound_nonce = st.session_state.get("sound_nonce", 0) + 1


def reset_game(mode, level):
    st.session_state.board = create_board()
    st.session_state.turn = PLAYER_1
    st.session_state.winner = 0
    st.session_state.history = []
    st.session_state.move_log = []
    st.session_state.result_recorded = False
    st.session_state.mode = mode
    st.session_state.level = level


def reset_match(mode, level, best_of):
    reset_game(mode, level)
    st.session_state.best_of = best_of
    st.session_state.score_p1 = 0
    st.session_state.score_p2 = 0
    st.session_state.score_draws = 0


def ensure_state(mode, level):
    if "board" not in st.session_state:
        reset_match(mode, level, best_of=3)
        return

    st.session_state.setdefault("best_of", 3)
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("move_log", [])
    st.session_state.setdefault("result_recorded", False)
    st.session_state.setdefault("bot_name", "Bot")

    if st.session_state.mode != mode or st.session_state.level != level:
        reset_match(mode, level, st.session_state.best_of)


def ensure_match_state(best_of):
    st.session_state.setdefault("best_of", best_of)
    st.session_state.setdefault("score_p1", 0)
    st.session_state.setdefault("score_p2", 0)
    st.session_state.setdefault("score_draws", 0)

    if st.session_state.best_of != best_of:
        st.session_state.best_of = best_of
        st.session_state.score_p1 = 0
        st.session_state.score_p2 = 0
        st.session_state.score_draws = 0
        reset_game(st.session_state.mode, st.session_state.level)


def push_history_snapshot():
    st.session_state.history.append(
        {
            "board": [row[:] for row in st.session_state.board],
            "turn": st.session_state.turn,
            "winner": st.session_state.winner,
            "result_recorded": st.session_state.result_recorded,
        }
    )


def animate_drop(col, row, piece, board_placeholder):
    for anim_row in range(5, row - 1, -1):
        render_board(st.session_state.board, falling=(col, anim_row, piece), target=board_placeholder)
        time.sleep(0.03)


def wins_required():
    return st.session_state.best_of // 2 + 1


def is_match_over():
    return st.session_state.score_p1 >= wins_required() or st.session_state.score_p2 >= wins_required()


def player_name(piece):
    if piece == PLAYER_1:
        return st.session_state.player1_name
    if st.session_state.mode == MODE_LOCAL:
        return st.session_state.player2_name
    return st.session_state.bot_name


def apply_move(col, board_placeholder=None, with_animation=True):
    if st.session_state.winner != 0 or is_match_over():
        return False

    board = st.session_state.board
    turn = st.session_state.turn

    if not is_valid_location(board, col):
        st.warning("This column is full.")
        return False

    row = get_next_open_row(board, col)
    if row is None:
        st.warning("This column is full.")
        return False

    push_history_snapshot()

    if with_animation and board_placeholder is not None:
        animate_drop(col, row, turn, board_placeholder)

    drop_piece(board, row, col, turn)

    st.session_state.move_log.append(
        {
            "move": len(st.session_state.move_log) + 1,
            "player": player_name(turn),
            "piece": "🔴" if turn == PLAYER_1 else "🟡",
            "column": col + 1,
            "row": row + 1,
        }
    )

    set_sound_event("drop")

    if winning_move(board, turn):
        st.session_state.winner = turn
        set_sound_event("win")
        return True

    if board_is_full(board):
        st.session_state.winner = -1
        set_sound_event("draw")
        return True

    st.session_state.turn = PLAYER_2 if turn == PLAYER_1 else PLAYER_1
    return True


def undo_last_move_local():
    if st.session_state.mode != MODE_LOCAL:
        st.info("Undo is only available in local friend mode.")
        return

    if not st.session_state.history or st.session_state.winner != 0:
        st.info("No move to undo right now.")
        return

    snapshot = st.session_state.history.pop()
    st.session_state.board = [row[:] for row in snapshot["board"]]
    st.session_state.turn = snapshot["turn"]
    st.session_state.winner = snapshot["winner"]
    st.session_state.result_recorded = snapshot["result_recorded"]

    if st.session_state.move_log:
        st.session_state.move_log.pop()


def undo_last_cycle_vs_bot():
    if st.session_state.mode != MODE_BOT:
        st.info("This undo is only for Vs Bot mode.")
        return

    if st.session_state.winner != 0:
        st.info("Undo after round finish is disabled. Start a new round.")
        return

    if len(st.session_state.history) < 2:
        st.info("No bot cycle to undo yet.")
        return

    snapshot = None
    for _ in range(2):
        snapshot = st.session_state.history.pop()

    if snapshot is None:
        return

    st.session_state.board = [row[:] for row in snapshot["board"]]
    st.session_state.turn = snapshot["turn"]
    st.session_state.winner = snapshot["winner"]
    st.session_state.result_recorded = snapshot["result_recorded"]

    if st.session_state.move_log:
        st.session_state.move_log.pop()
    if st.session_state.move_log:
        st.session_state.move_log.pop()


def record_round_result():
    if st.session_state.winner == 0 or st.session_state.result_recorded:
        return

    if st.session_state.winner == PLAYER_1:
        st.session_state.score_p1 += 1
    elif st.session_state.winner == PLAYER_2:
        st.session_state.score_p2 += 1
    else:
        st.session_state.score_draws += 1

    st.session_state.result_recorded = True


def maybe_play_ai(board_placeholder):
    if st.session_state.mode != MODE_BOT:
        return

    if st.session_state.winner != 0 or is_match_over() or st.session_state.turn != PLAYER_2:
        return

    col = pick_ai_move(st.session_state.board, st.session_state.level)
    if col is None:
        st.session_state.winner = -1
        set_sound_event("draw")
        return

    apply_move(col, board_placeholder=board_placeholder, with_animation=True)


def winner_text():
    if st.session_state.winner == PLAYER_1:
        return f"{st.session_state.player1_name} (🔴) wins!"
    if st.session_state.winner == PLAYER_2:
        return f"{player_name(PLAYER_2)} (🟡) wins!"
    if st.session_state.winner == -1:
        return "Draw game."
    return ""


def current_turn_text():
    if st.session_state.turn == PLAYER_1:
        return f"{st.session_state.player1_name} (🔴)"
    return f"{player_name(PLAYER_2)} (🟡)"


def parse_keyboard_column(raw_value):
    if not raw_value:
        return None
    value = raw_value.strip()
    if not value.isdigit():
        return None
    col = int(value)
    if 1 <= col <= COLUMN_COUNT:
        return col - 1
    return None


def render_threat_hints():
    if st.session_state.winner != 0 or is_match_over():
        return

    board = st.session_state.board
    current_piece = st.session_state.turn
    opponent_piece = PLAYER_2 if current_piece == PLAYER_1 else PLAYER_1

    winning_now = [col + 1 for col in find_winning_columns(board, current_piece)]
    must_block = [col + 1 for col in find_winning_columns(board, opponent_piece)]

    if winning_now:
        st.success(f"Winning move available now: columns {winning_now}")
    if must_block:
        st.warning(f"Danger! Opponent can win next turn in columns {must_block}")


def render_move_log():
    logs = st.session_state.get("move_log", [])
    with st.expander("Move Log", expanded=False):
        if not logs:
            st.write("No moves yet.")
            return

        for entry in logs[-12:]:
            st.write(
                f"{entry['move']}. {entry['player']} {entry['piece']} → column {entry['column']} (row {entry['row']})"
            )


def main():
    st.set_page_config(page_title="Connect Four", page_icon="🎮", layout="centered")

    profile_id = get_or_create_profile_id()
    load_profile_once(profile_id)
    setup_sound_defaults()

    st.title("🎮 Connect Four")
    st.caption(f"Profile ID: {profile_id} (saved automatically)")

    mode_default = st.session_state.get("mode", MODE_LOCAL)
    mode_options = [MODE_LOCAL, MODE_BOT]
    mode_index = mode_options.index(mode_default) if mode_default in mode_options else 0

    level_options = ["Easy", "Medium", "Hard", "Hard+"]
    level_default = st.session_state.get("level", "Medium")
    level_index = level_options.index(level_default) if level_default in level_options else 1

    best_default = st.session_state.get("best_of", 3)
    best_options = [3, 5]
    best_index = best_options.index(best_default) if best_default in best_options else 0

    with st.sidebar:
        st.subheader("Game Settings")
        mode = st.radio("Mode", options=mode_options, index=mode_index)

        player1_name = st.text_input("Player 1 Name", value=st.session_state.get("player1_name", "Player 1")).strip()
        if not player1_name:
            player1_name = "Player 1"

        player2_name = "Player 2"
        if mode == MODE_LOCAL:
            player2_name = st.text_input("Player 2 Name", value=st.session_state.get("player2_name", "Player 2")).strip()
            if not player2_name:
                player2_name = "Player 2"

        best_of = st.selectbox("Match Type", options=best_options, index=best_index, format_func=lambda value: f"Best of {value}")

        level = "Medium"
        if mode == MODE_BOT:
            level = st.selectbox("Bot Difficulty", options=level_options, index=level_index)

        st.subheader("Sound")
        sound_enabled = st.checkbox("Sound Enabled", value=st.session_state.get("sound_enabled", True))
        sound_drop = st.checkbox("Drop Sound", value=st.session_state.get("sound_drop", True))
        sound_win = st.checkbox("Win Sound", value=st.session_state.get("sound_win", True))
        sound_draw = st.checkbox("Draw Sound", value=st.session_state.get("sound_draw", True))
        mute = st.checkbox("Mute", value=st.session_state.get("mute", False))

        st.session_state.player1_name = player1_name
        st.session_state.player2_name = player2_name
        st.session_state.bot_name = "Bot"
        st.session_state.sound_enabled = sound_enabled
        st.session_state.sound_drop = sound_drop
        st.session_state.sound_win = sound_win
        st.session_state.sound_draw = sound_draw
        st.session_state.mute = mute

        if st.button("New Round", use_container_width=True):
            reset_game(mode, level)
            persist_profile(profile_id)
            st.rerun()

        if st.button("Reset Match", use_container_width=True):
            reset_match(mode, level, best_of)
            persist_profile(profile_id)
            st.rerun()

    ensure_state(mode, level)
    ensure_match_state(best_of)

    board_placeholder = st.empty()

    maybe_play_ai(board_placeholder)
    record_round_result()

    c1, c2, c3 = st.columns(3)
    c1.metric("Mode", "Local PvP" if mode == MODE_LOCAL else "Vs Bot")
    c2.metric("Level", "-" if mode == MODE_LOCAL else st.session_state.level)
    c3.metric("Turn", current_turn_text())

    p1_name = st.session_state.player1_name
    p2_name = st.session_state.player2_name if mode == MODE_LOCAL else st.session_state.bot_name
    wins_goal = wins_required()

    s1, s2, s3 = st.columns(3)
    s1.metric(f"{p1_name} (🔴)", st.session_state.score_p1)
    s2.metric(f"{p2_name} (🟡)", st.session_state.score_p2)
    s3.metric("Draws", st.session_state.score_draws)
    st.caption(f"Match: Best of {st.session_state.best_of} • First to {wins_goal} wins")

    render_board(st.session_state.board, target=board_placeholder)

    if is_match_over():
        champion = p1_name if st.session_state.score_p1 >= wins_goal else p2_name
        st.success(f"🏆 {champion} wins the match!")

    if st.session_state.winner != 0:
        if st.session_state.winner == -1:
            st.info(winner_text())
        else:
            st.success(winner_text())
    elif not is_match_over():
        st.write(f"Current turn: **{current_turn_text()}**")

    render_threat_hints()

    st.markdown("### Make your move")
    human_turn = st.session_state.turn == PLAYER_1 or mode == MODE_LOCAL
    controls_disabled = st.session_state.winner != 0 or not human_turn or is_match_over()

    with st.form("move_form", clear_on_submit=False):
        selected_col = st.select_slider("Choose column", options=list(range(1, COLUMN_COUNT + 1)), value=4)
        move_clicked = st.form_submit_button("Drop Piece", disabled=controls_disabled, use_container_width=True)

    if move_clicked:
        moved = apply_move(selected_col - 1, board_placeholder=board_placeholder, with_animation=True)
        if mode == MODE_BOT and st.session_state.winner == 0:
            maybe_play_ai(board_placeholder)
        record_round_result()
        if moved:
            persist_profile(profile_id)
            st.rerun()

    with st.form("keyboard_move_form", clear_on_submit=True):
        keyboard_input = st.text_input("Keyboard move (press 1..7 then Enter)", max_chars=1)
        key_move_clicked = st.form_submit_button("Play Keyboard Move", disabled=controls_disabled, use_container_width=True)

    if key_move_clicked:
        key_col = parse_keyboard_column(keyboard_input)
        if key_col is None:
            st.warning("Use a number from 1 to 7.")
        else:
            moved = apply_move(key_col, board_placeholder=board_placeholder, with_animation=True)
            if mode == MODE_BOT and st.session_state.winner == 0:
                maybe_play_ai(board_placeholder)
            record_round_result()
            if moved:
                persist_profile(profile_id)
                st.rerun()

    c_undo1, c_undo2 = st.columns(2)
    with c_undo1:
        if st.button("Undo Last Move (Local)", disabled=mode != MODE_LOCAL or not st.session_state.history or st.session_state.winner != 0):
            undo_last_move_local()
            persist_profile(profile_id)
            st.rerun()

    with c_undo2:
        if st.button("Undo Last Cycle (You + Bot)", disabled=mode != MODE_BOT or len(st.session_state.history) < 2 or st.session_state.winner != 0):
            undo_last_cycle_vs_bot()
            persist_profile(profile_id)
            st.rerun()

    render_move_log()

    render_sound_player(
        event_name=st.session_state.get("sound_event", "none"),
        nonce=st.session_state.get("sound_nonce", 0),
        muted=st.session_state.get("mute", False) or not st.session_state.get("sound_enabled", True),
    )

    persist_profile(profile_id)


if __name__ == "__main__":
    main()
