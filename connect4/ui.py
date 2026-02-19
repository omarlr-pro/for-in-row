import streamlit as st
import streamlit.components.v1 as components

from .logic import ROW_COUNT, COLUMN_COUNT


def render_board(board, falling=None, target=None):
    color_map = {0: "#f8fafc", 1: "#ef4444", 2: "#eab308"}
    rows_html = []

    for display_row in range(ROW_COUNT - 1, -1, -1):
        cells = []
        for col in range(COLUMN_COUNT):
            cell_value = board[display_row][col]
            if falling is not None:
                falling_col, falling_row, falling_piece = falling
                if col == falling_col and display_row == falling_row:
                    cell_value = falling_piece

            cells.append(f"<div class='cf-cell' style='background:{color_map[cell_value]};'></div>")
        rows_html.append(f"<div class='cf-row'>{''.join(cells)}</div>")

    labels = "".join([f"<div class='cf-col-label'>{idx}</div>" for idx in range(1, COLUMN_COUNT + 1)])

    container = target if target is not None else st
    container.markdown(
        f"""
        <style>
        .cf-wrap {{
            background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%);
            padding: 14px;
            border-radius: 16px;
            width: fit-content;
            margin: 0 auto;
            box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        }}
        .cf-header, .cf-row {{
            display: grid;
            grid-template-columns: repeat(7, 54px);
            gap: 8px;
            justify-content: center;
            margin-bottom: 8px;
        }}
        .cf-row:last-child {{ margin-bottom: 0; }}
        .cf-cell {{
            width: 54px;
            height: 54px;
            border-radius: 50%;
            border: 2px solid rgba(15,23,42,0.2);
        }}
        .cf-col-label {{
            text-align: center;
            color: white;
            font-weight: 700;
            font-size: 16px;
        }}
        </style>
        <div class='cf-wrap'>
            <div class='cf-header'>{labels}</div>
            {''.join(rows_html)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sound_player(event_name, nonce, muted):
        event = event_name or "none"
        components.html(
                f"""
                <script>
                    (function() {{
                        const eventName = {event!r};
                        const nonce = {int(nonce)};
                        const muted = {str(bool(muted)).lower()};

                        if (!window.__cfSound) {{
                            window.__cfSound = {{
                                lastNonce: -1,
                                ctx: null,
                            }};
                        }}

                        const state = window.__cfSound;
                        if (state.lastNonce === nonce) return;
                        state.lastNonce = nonce;
                        if (muted || eventName === "none") return;

                        try {{
                            if (!state.ctx) {{
                                state.ctx = new (window.AudioContext || window.webkitAudioContext)();
                            }}

                            const ctx = state.ctx;
                            if (ctx.state === "suspended") {{
                                ctx.resume();
                            }}

                            const tone = (freq, duration, type, volume, offset = 0) => {{
                                const osc = ctx.createOscillator();
                                const gain = ctx.createGain();
                                osc.type = type;
                                osc.frequency.value = freq;
                                gain.gain.value = volume;
                                osc.connect(gain);
                                gain.connect(ctx.destination);
                                const startAt = ctx.currentTime + offset;
                                const endAt = startAt + duration;
                                osc.start(startAt);
                                gain.gain.setValueAtTime(volume, startAt);
                                gain.gain.exponentialRampToValueAtTime(0.0001, endAt);
                                osc.stop(endAt);
                            }};

                            if (eventName === "drop") {{
                                tone(320, 0.08, "triangle", 0.06);
                            }} else if (eventName === "win") {{
                                tone(392, 0.12, "sine", 0.08, 0);
                                tone(523, 0.12, "sine", 0.08, 0.12);
                                tone(659, 0.18, "sine", 0.08, 0.24);
                            }} else if (eventName === "draw") {{
                                tone(220, 0.12, "sawtooth", 0.06, 0);
                                tone(196, 0.12, "sawtooth", 0.06, 0.12);
                                tone(174, 0.16, "sawtooth", 0.06, 0.24);
                            }}
                        }} catch (e) {{
                        }}
                    }})();
                </script>
                """,
                height=0,
        )
