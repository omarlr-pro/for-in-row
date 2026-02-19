import json
from pathlib import Path

PERSIST_FILE = Path(__file__).resolve().parent.parent / "player_state.json"

PERSIST_KEYS = [
    "board",
    "turn",
    "winner",
    "history",
    "result_recorded",
    "mode",
    "level",
    "best_of",
    "score_p1",
    "score_p2",
    "score_draws",
    "player1_name",
    "player2_name",
    "bot_name",
    "move_log",
    "sound_enabled",
    "sound_drop",
    "sound_win",
    "sound_draw",
    "mute",
]


def _read_all_states():
    if not PERSIST_FILE.exists():
        return {}
    try:
        return json.loads(PERSIST_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _write_all_states(data):
    temp = PERSIST_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(PERSIST_FILE)


def load_profile_state(profile_id):
    states = _read_all_states()
    return states.get(profile_id, {})


def save_profile_state(profile_id, session_state):
    states = _read_all_states()
    payload = {}
    for key in PERSIST_KEYS:
        if key in session_state:
            payload[key] = session_state[key]
    states[profile_id] = payload
    _write_all_states(states)
