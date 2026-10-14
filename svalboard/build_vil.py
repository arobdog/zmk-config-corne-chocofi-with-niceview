#!/usr/bin/env python3
"""Builds colemak-dhm.vil for the Svalboard from the layer tables below."""

import json
from pathlib import Path

BASE, NUM, NAV, QWERTY, BOARD, MOUSE = 0, 1, 2, 3, 14, 15
LAYER_COUNT = 16

# Matrix rows: 0 left thumb, 1-4 left index..pinky, 5 right thumb, 6-9 right index..pinky.
LEFT_FINGER_ROWS = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}
RIGHT_FINGER_ROWS = {"R1": 6, "R2": 7, "R3": 8, "R4": 9}
THUMB_ROWS = {"LT": 0, "RT": 5}

FINGER_COLS = {"s": 0, "c": 2, "n": 3, "ds": 5}
LEFT_SIDE_COLS = {"inner": 1, "outer": 4}
RIGHT_SIDE_COLS = {"inner": 4, "outer": 1}
THUMB_COLS = {"knuckle": 0, "nail": 1, "down": 2, "pad": 3, "up": 4, "dd": 5}

NO, TRNS = "KC_NO", "KC_TRNS"


def finger_cols(name):
    side = LEFT_SIDE_COLS if name.startswith("L") else RIGHT_SIDE_COLS
    return {**FINGER_COLS, **side}


def build_layer(keys, fill):
    rows = [[fill] * 6 for _ in range(10)]
    for cluster, directions in keys.items():
        if cluster in THUMB_ROWS:
            row, cols = THUMB_ROWS[cluster], THUMB_COLS
        else:
            row = {**LEFT_FINGER_ROWS, **RIGHT_FINGER_ROWS}[cluster]
            cols = finger_cols(cluster)
        for direction, keycode in directions.items():
            rows[row][cols[direction]] = keycode
    return rows


layers = {
    BASE: (NO, {
        "L4": dict(c="LGUI_T(KC_A)", n="KC_Q", s="KC_Z"),
        "L3": dict(c="LALT_T(KC_R)", n="KC_W", s="KC_X", inner="KC_V", outer="KC_ESCAPE"),
        "L2": dict(c="LCTL_T(KC_S)", n="KC_F", s="KC_C", inner="KC_B"),
        "L1": dict(c="LSFT_T(KC_T)", n="KC_P", s="KC_D", inner="KC_G", outer="KC_MINUS"),
        "R1": dict(c="RSFT_T(KC_N)", n="KC_L", s="KC_H", inner="KC_M", outer="KC_UNDS"),
        "R2": dict(c="RCTL_T(KC_E)", n="KC_U", s="KC_COMMA", inner="KC_J", outer="KC_SCOLON"),
        "R3": dict(c="RALT_T(KC_I)", n="KC_Y", s="KC_DOT", inner="KC_K", outer=f"MO({BOARD})"),
        "R4": dict(c="RGUI_T(KC_O)", n="KC_QUOTE", s="KC_SLASH"),
        "LT": dict(down=f"LT({NUM},KC_TAB)", pad=f"LT({NAV},KC_SPACE)", nail="KC_LSHIFT",
                   knuckle="M0", up=f"TO({BASE})"),
        "RT": dict(down=f"LT({NUM},KC_BSPACE)", pad=f"LT({NAV},KC_ENTER)",
                   knuckle="KC_ESCAPE", up="QK_REPEAT_KEY"),
    }),
    NUM: (NO, {
        "L4": dict(n="KC_EXLM", c="KC_HASH", s="KC_PERC", outer="KC_LGUI"),
        "L3": dict(n="KC_AT", c="KC_DLR", s="KC_CIRC", outer="KC_LALT", inner="KC_TILD"),
        "L2": dict(n="KC_LCBR", c="KC_LPRN", s="KC_LBRACKET", outer="KC_LCTRL", inner="KC_PIPE"),
        "L1": dict(n="KC_RCBR", c="KC_RPRN", s="KC_RBRACKET", outer="KC_LSHIFT", inner="KC_GRAVE"),
        "R1": dict(n="KC_7", c="KC_4", s="KC_1", inner="KC_MINUS"),
        "R2": dict(n="KC_8", c="KC_5", s="KC_2", inner="KC_PLUS"),
        "R3": dict(n="KC_9", c="KC_6", s="KC_3", outer="KC_DOT", inner="KC_EQUAL"),
        "R4": dict(n="KC_ASTR", c="KC_COLN", s="KC_BSLASH"),
        "LT": dict(down="LCTL(KC_BSPACE)", pad="KC_SPACE", nail=TRNS, up=TRNS, dd="KC_LGUI"),
        "RT": dict(down="KC_DELETE", pad="KC_ENTER", nail="KC_0", knuckle=TRNS),
    }),
    NAV: (NO, {
        "L4": dict(n="KC_F1", c="LGUI_T(KC_F5)", s="KC_F9"),
        "L3": dict(n="KC_F2", c="LALT_T(KC_F6)", s="KC_F10", inner="KC_PSCREEN"),
        "L2": dict(n="KC_F3", c="LCTL_T(KC_F7)", s="KC_F11", inner="M1"),
        "L1": dict(n="KC_F4", c="LSFT_T(KC_F8)", s="KC_F12", inner="TD(0)"),
        "R1": dict(n="LSFT(KC_MPRV)", c="KC_LEFT", s="LALT(KC_H)", inner="KC_MPLY"),
        "R2": dict(n="KC_VOLD", c="KC_DOWN", s="LALT(KC_TAB)"),
        "R3": dict(n="KC_VOLU", c="KC_UP"),
        "R4": dict(n="LSFT(KC_MNXT)", c="KC_RIGHT", s="LALT(KC_L)"),
        "LT": dict(pad=f"TO({QWERTY})", nail=TRNS, up=TRNS),
        "RT": dict(down=TRNS, pad=f"TO({QWERTY})", knuckle=TRNS),
    }),
    QWERTY: (TRNS, {
        "L4": dict(c="KC_A", n="KC_Q", s="KC_Z"),
        "L3": dict(c="KC_S", n="KC_W", s="KC_X", inner="KC_B"),
        "L2": dict(c="KC_D", n="KC_E", s="KC_C", inner="KC_T"),
        "L1": dict(c="KC_F", n="KC_R", s="KC_V", inner="KC_G"),
        "R1": dict(c="KC_J", n="KC_U", s="KC_M", inner="KC_H"),
        "R2": dict(c="KC_K", n="KC_I", s="KC_COMMA", inner="KC_Y"),
        "R3": dict(c="KC_L", n="KC_O", s="KC_DOT", inner="KC_N"),
        "R4": dict(c="KC_SCOLON", n="KC_P", s="KC_SLASH"),
        "LT": dict(knuckle=f"TO({BASE})"),
    }),
    BOARD: (TRNS, {
        "L4": dict(n="SV_RECALIBRATE_POINTER", s="SV_MH_CHANGE_TIMEOUTS"),
        "L3": dict(n="SV_LEFT_DPI_INC", c="SV_LEFT_SCROLL_TOGGLE", s="SV_LEFT_DPI_DEC"),
        "L2": dict(n="SV_RIGHT_DPI_INC", c="SV_RIGHT_SCROLL_TOGGLE", s="SV_RIGHT_DPI_DEC"),
        "L1": dict(c="SV_OUTPUT_STATUS", n="SV_TOGGLE_AUTOMOUSE"),
    }),
    # Clicks live on thumb keys a word never starts with, so typing straight after pointing isn't eaten.
    MOUSE: (TRNS, {
        "LT": dict(knuckle="SV_SNIPER_3"),
        "RT": dict(up="KC_BTN1", knuckle="KC_BTN2"),
    }),
}

# Order matches customKeycodes in the Svalboard vial.json; Vial stores them as USER00, USER01, ...
SVALBOARD_KEYCODES = [
    "SV_LEFT_DPI_INC", "SV_LEFT_DPI_DEC", "SV_RIGHT_DPI_INC", "SV_RIGHT_DPI_DEC",
    "SV_LEFT_SCROLL_TOGGLE", "SV_RIGHT_SCROLL_TOGGLE", "SV_RECALIBRATE_POINTER",
    "SV_MH_CHANGE_TIMEOUTS", "SV_CAPS_WORD", "SV_AXIS_SCROLL_LOCK", "SV_TOGGLE_23_67",
    "SV_TOGGLE_45_67", "SV_SNIPER_2", "SV_SNIPER_3", "SV_SNIPER_5", "SV_SCROLL_HOLD",
    "SV_SCROLL_TOGGLE", "SV_OUTPUT_STATUS", "SV_TOGGLE_AUTOMOUSE", "SV_TURBO_SCAN",
]


def to_vial_name(keycode):
    if keycode in SVALBOARD_KEYCODES:
        return f"USER{SVALBOARD_KEYCODES.index(keycode):02}"
    return keycode


def build_keymap():
    keymap = []
    for index in range(LAYER_COUNT):
        fill, keys = layers.get(index, (TRNS, {}))
        rows = build_layer(keys, fill)
        keymap.append([[to_vial_name(k) for k in row] for row in rows])
    for layer in keymap:
        # Double-south keys stay off on every layer so a hard pull never types anything.
        for row in [*LEFT_FINGER_ROWS.values(), *RIGHT_FINGER_ROWS.values()]:
            layer[row][FINGER_COLS["ds"]] = NO
    return keymap


macros = [
    [["tap", "KC_ESCAPE"], ["text", ":w"], ["tap", "KC_ENTER"]],
    [["text", "a.robs100@gmail.com"]],
]

tap_dances = [
    ["LCTL(KC_C)", "LCTL(KC_V)", NO, NO, 200],
]

combos = [
    ["LSFT_T(KC_T)", "RSFT_T(KC_N)", NO, NO, "KC_ESCAPE"],
    ["KC_D", "KC_H", NO, NO, "KC_UNDS"],
    ["KC_P", "KC_L", NO, NO, "KC_MINUS"],
    ["LGUI_T(KC_A)", "RGUI_T(KC_O)", NO, NO, "QK_CAPS_WORD_TOGGLE"],
]

SETTING_IDS = {
    "combo_term": 2, "tapping_term": 7, "permissive_hold": 22, "hold_on_other_key_press": 23,
    "retro_tapping": 24, "quick_tap_term": 25, "chordal_hold": 26, "flow_tap_term": 27,
}

settings = {
    "combo_term": 50,
    "tapping_term": 200,
    "permissive_hold": 0,
    "hold_on_other_key_press": 0,
    "retro_tapping": 0,
    "quick_tap_term": 150,
    "chordal_hold": 0,
    "flow_tap_term": 125,
}

vil = {
    "version": 1,
    "uid": int.from_bytes(bytes([0x1B, 0x18, 0x7D, 0xF2, 0x21, 0xF6, 0x29, 0x48]), "little"),
    "layout": build_keymap(),
    "encoder_layout": [[] for _ in range(LAYER_COUNT)],
    "layout_options": 0,
    "macro": macros,
    "vial_protocol": 6,
    "via_protocol": 9,
    "tap_dance": tap_dances,
    "combo": combos,
    "key_override": [],
    "alt_repeat_key": [],
    "settings": {str(SETTING_IDS[name]): value for name, value in settings.items()},
}

if __name__ == "__main__":
    out = Path(__file__).with_name("colemak-dhm.vil")
    out.write_text(json.dumps(vil, indent=1) + "\n")
    print(f"wrote {out}")
