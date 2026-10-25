/* Copyright 2024 ~ 2026 @ Keychron (https://www.keychron.com)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include QMK_KEYBOARD_H
#include "keychron_common.h"
#ifdef VIA_ENABLE
#    include "dynamic_keymap.h"
#endif

// Stock layer indices 0-3 are required by Keychron's rear OS switch.
enum layers { MAC_BASE, MAC_FN, WIN_BASE, WIN_FN, LINUX_BASE, LINUX_FN };
enum custom_keycodes {
    LINUX_MODE = SAFE_RANGE, AC_SWITCH, UPDIR, WIN_SIG, SEL_WORD,
    LNX_TERM, LNX_COPY, LNX_OVERVIEW, LNX_APPS, LNX_PASTE, LIST_LONG,
};
#define FN_MAC MO(MAC_FN)
#define FN_WIN MO(WIN_FN)

// Circle, triangle and square occupy the original F13, F14 and F15 positions.
// clang-format off
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [MAC_BASE] = LAYOUT_ansi_101(
        KC_ESC, KC_BRID, KC_BRIU, KC_MCTRL, KC_LNPAD, UG_VALD, UG_VALU, KC_MPRV, KC_MPLY, KC_MNXT, KC_MUTE, KC_VOLD, KC_VOLU, KC_DEL, KC_F13, KC_F14, KC_F15, KC_MUTE,
        KC_GRV, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0, KC_MINS, KC_EQL, KC_BSPC, KC_PGUP, KC_NUM, KC_PSLS, KC_PAST, KC_PMNS,
        KC_TAB, KC_Q, KC_W, KC_E, KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_P, KC_LBRC, KC_RBRC, KC_BSLS, KC_PGDN, KC_P7, KC_P8, KC_P9,
        KC_CAPS, KC_A, KC_S, KC_D, KC_F, KC_G, KC_H, KC_J, KC_K, KC_L, KC_SCLN, KC_QUOT, KC_ENT, KC_HOME, KC_P4, KC_P5, KC_P6, KC_PPLS,
        KC_LSFT, KC_Z, KC_X, KC_C, KC_V, KC_B, KC_N, KC_M, KC_COMM, KC_DOT, KC_SLSH, KC_RSFT, KC_UP, KC_P1, KC_P2, KC_P3,
        KC_LCTL, KC_LOPTN, KC_LCMMD, KC_SPC, KC_RCMMD, FN_MAC, KC_RCTL, KC_LEFT, KC_DOWN, KC_RGHT, KC_P0, KC_PDOT, KC_PENT),

    [MAC_FN] = LAYOUT_ansi_101(
        _______, KC_F1, KC_F2, KC_F3, KC_F4, KC_F5, KC_F6, KC_F7, KC_F8, KC_F9, KC_F10, KC_F11, KC_F12, _______, _______, _______, _______, UG_TOGG,
        _______, BT_HST1, BT_HST2, BT_HST3, P2P4G, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        UG_TOGG, UG_NEXT, UG_VALU, UG_HUEU, UG_SATU, UG_SPDU, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, UG_PREV, UG_VALD, UG_HUED, UG_SATD, UG_SPDD, _______, _______, _______, _______, _______, _______, _______, KC_END, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, BAT_LVL, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, LINUX_MODE, _______, _______, _______, _______, _______, _______, _______, _______, _______),

    [WIN_BASE] = LAYOUT_ansi_101(
        KC_ESC, KC_F1, KC_F2, KC_F3, KC_F4, KC_F5, KC_F6, KC_F7, KC_F8, KC_F9, KC_F10, KC_F11, KC_F12, KC_DEL, _______, _______, _______, KC_MUTE,
        KC_GRV, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0, KC_MINS, KC_EQL, KC_BSPC, KC_PGUP, KC_NUM, KC_PSLS, KC_PAST, KC_PMNS,
        KC_TAB, KC_Q, KC_W, KC_E, KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_P, KC_LBRC, KC_RBRC, KC_BSLS, KC_PGDN, KC_P7, KC_P8, KC_P9,
        KC_CAPS, KC_A, KC_S, KC_D, KC_F, KC_G, KC_H, KC_J, KC_K, KC_L, KC_SCLN, KC_QUOT, KC_ENT, KC_HOME, KC_P4, KC_P5, KC_P6, KC_PPLS,
        KC_LSFT, KC_Z, KC_X, KC_C, KC_V, KC_B, KC_N, KC_M, KC_COMM, KC_DOT, KC_SLSH, KC_RSFT, KC_UP, KC_P1, KC_P2, KC_P3,
        KC_LCTL, KC_LWIN, KC_LALT, KC_SPC, KC_RALT, FN_WIN, KC_RCTL, KC_LEFT, KC_DOWN, KC_RGHT, KC_P0, KC_PDOT, KC_PENT),

    [WIN_FN] = LAYOUT_ansi_101(
        _______, KC_BRID, KC_BRIU, KC_TASK, KC_FILE, UG_VALD, UG_VALU, KC_MPRV, KC_MPLY, KC_MNXT, KC_MUTE, KC_VOLD, KC_VOLU, _______, _______, _______, _______, UG_TOGG,
        _______, BT_HST1, BT_HST2, BT_HST3, P2P4G, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        UG_TOGG, UG_NEXT, UG_VALU, UG_HUEU, UG_SATU, UG_SPDU, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, UG_PREV, UG_VALD, UG_HUED, UG_SATD, UG_SPDD, _______, _______, _______, _______, _______, _______, _______, KC_END, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, BAT_LVL, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, LINUX_MODE, _______, _______, _______, _______, _______, _______, _______, _______, _______),

    [LINUX_BASE] = LAYOUT_ansi_101(
        KC_ESC, KC_F1, KC_F2, KC_F3, KC_F4, KC_F5, KC_F6, KC_F7, KC_F8, KC_F9, KC_F10, KC_F11, KC_F12, KC_DEL, LNX_TERM, LNX_COPY, LNX_PASTE, KC_MUTE,
        KC_GRV, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0, KC_MINS, KC_EQL, KC_BSPC, KC_PGUP, KC_NUM, KC_PSLS, KC_PAST, KC_PMNS,
        KC_TAB, KC_Q, KC_W, KC_E, KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_P, KC_LBRC, KC_RBRC, KC_BSLS, KC_PGDN, KC_P7, KC_P8, KC_P9,
        KC_CAPS, KC_A, KC_S, KC_D, KC_F, KC_G, KC_H, KC_J, KC_K, KC_L, KC_SCLN, KC_QUOT, KC_ENT, KC_HOME, KC_P4, KC_P5, KC_P6, KC_PPLS,
        SC_LSPO, KC_Z, KC_X, KC_C, KC_V, KC_B, KC_N, KC_M, KC_COMM, KC_DOT, KC_SLSH, SC_RSPC, KC_UP, KC_P1, KC_P2, KC_P3,
        KC_LCTL, KC_LWIN, KC_LALT, KC_SPC, KC_RALT, MO(LINUX_FN), KC_RCTL, KC_LEFT, KC_DOWN, KC_RGHT, KC_P0, KC_PDOT, KC_PENT),

    [LINUX_FN] = LAYOUT_ansi_101(
        _______, KC_BRID, KC_BRIU, LNX_OVERVIEW, LNX_APPS, UG_VALD, UG_VALU, KC_MPRV, KC_MPLY, KC_MNXT, KC_MUTE, KC_VOLD, KC_VOLU, _______, SEL_WORD, _______, _______, UG_TOGG,
        _______, BT_HST1, BT_HST2, BT_HST3, P2P4G, _______, _______, _______, _______, _______, _______, _______, _______, _______, KC_HOME, _______, _______, _______, _______,
        UG_TOGG, UG_NEXT, UG_VALU, UG_HUEU, DM_REC1, UG_SPDU, _______, _______, _______, _______, DM_PLY1, _______, _______, _______, KC_END, UG_PREV, UG_NEXT, UG_SPDU,
        _______, AC_SWITCH, DM_RSTP, UPDIR, UG_SATD, UG_SPDD, _______, _______, _______, LIST_LONG, _______, _______, _______, KC_END, UG_VALD, UG_VALU, UG_SPDD, _______,
        _______, _______, _______, CW_TOGG, _______, BAT_LVL, _______, WIN_SIG, _______, _______, _______, _______, _______, UG_HUED, UG_HUEU, UG_SATU,
        _______, _______, _______, LINUX_MODE, _______, _______, _______, _______, _______, _______, _______, UG_SATD, _______),

};
// clang-format on

const uint16_t PROGMEM encoder_map[][NUM_ENCODERS][NUM_DIRECTIONS] = {
    [MAC_BASE]   = {ENCODER_CCW_CW(KC_VOLD, KC_VOLU)},
    [MAC_FN]     = {ENCODER_CCW_CW(UG_VALD, UG_VALU)},
    [WIN_BASE]   = {ENCODER_CCW_CW(KC_VOLD, KC_VOLU)},
    [WIN_FN]     = {ENCODER_CCW_CW(UG_VALD, UG_VALU)},
    [LINUX_BASE] = {ENCODER_CCW_CW(KC_VOLD, KC_VOLU)},
    [LINUX_FN]   = {ENCODER_CCW_CW(MS_WHLU, MS_WHLD)},
};

static bool linux_autocorrect = true;
static bool macro_recording = false;
static uint8_t standard_layer = MAC_BASE;
static uint8_t previous_rgb_mode;
static bool custom_rgb_active = false;
static bool explicit_mode_exit = false;
// The user's left butterfly key is the third bottom-row key: KC_LALT in
// this Linux map. Defer it until its partner is known, so clipboard chords
// do not leak Alt into the application or activate its menu on release.
static bool butterfly_held, butterfly_used, butterfly_forwarded;

static void reset_butterfly(void) {
    butterfly_held = butterfly_used = butterfly_forwarded = false;
}

static bool linux_mode(void) {
    return (default_layer_state & (1UL << LINUX_BASE)) != 0;
}

const key_override_t shift_delete = ko_make_with_layers(
    MOD_MASK_SHIFT, KC_BSPC, KC_DEL, (1UL << LINUX_BASE) | (1UL << LINUX_FN));
const key_override_t *key_overrides[] = { &shift_delete };

#include "select_word.c"

// Keep the core autocorrect engine enabled in RAM. Gate it here so stock layouts
// and explicit Linux text macros never acquire personal typing behaviour.
bool process_autocorrect_user(uint16_t *keycode, keyrecord_t *record,
                              uint8_t *buffer_size, uint8_t *mods) {
    if (!linux_mode() || !linux_autocorrect || *keycode >= SAFE_RANGE) {
        *buffer_size = 0;
        return false;
    }
    return process_autocorrect_default_handler(keycode, record, buffer_size, mods);
}

static void finish_recording(void) {
    if (macro_recording) dynamic_macro_stop_recording();
}

static void change_mode(void) {
    finish_recording();
    reset_butterfly();
    caps_word_off();
    clear_keyboard();
    layer_clear();
    if (linux_mode()) {
        explicit_mode_exit = true;
        default_layer_set(1UL << standard_layer);
        explicit_mode_exit = false;
        rgb_matrix_mode_noeeprom(previous_rgb_mode);
        custom_rgb_active = false;
    } else {
        standard_layer = get_highest_layer(default_layer_state);
        previous_rgb_mode = rgb_matrix_get_mode();
        custom_rgb_active = true;
        default_layer_set(1UL << LINUX_BASE);
        rgb_matrix_mode_noeeprom(RGB_MATRIX_TYPING_HEATMAP);
    }
}

void keyboard_post_init_user(void) {
    // Do not write the preference to EEPROM on every boot or mode change.
    keymap_config.autocorrect_enable = true;
#ifdef VIA_ENABLE
    if (dynamic_keymap_get_keycode(LINUX_FN, 3, 9) == KC_TRNS) {
        dynamic_keymap_set_keycode(LINUX_FN, 3, 9, LIST_LONG);
    }
    // Upgrade only our previous square binding if VIA retained the earlier map.
    // Leave other remaps and the function-row overview shortcut untouched.
    if (dynamic_keymap_get_keycode(LINUX_BASE, 0, 17) == LNX_OVERVIEW) {
        dynamic_keymap_set_keycode(LINUX_BASE, 0, 17, LNX_PASTE);
    }
#endif
}

layer_state_t default_layer_state_set_user(layer_state_t state) {
    // Keychron calls dip_switch_init() on wireless wake, forcing a fresh report
    // even when the physical OS switch has not moved. That is not a mode exit.
    // RAM survives this sleep path; no EEPROM writes or sleep-hook overrides
    // are needed. Explicit Fn+Space and an actual switch movement still exit.
    if (linux_mode() && !explicit_mode_exit && state == (1UL << standard_layer)) {
        return default_layer_state;
    }
    // Keychron reserves the DIP-switch user hook for factory tests. Observe
    // default-layer changes instead, including those made by the rear switch.
    if (!(state & (1UL << LINUX_BASE))) {
        if (custom_rgb_active) {
            finish_recording();
            reset_butterfly();
            caps_word_off();
            clear_keyboard();
            layer_clear();
            rgb_matrix_mode_noeeprom(previous_rgb_mode);
            custom_rgb_active = false;
        }
        standard_layer = get_highest_layer(state);
    }
    return state;
}

// Send literal text without held modifiers altering punctuation or letters.
static void literal_text(const char *text) {
    const uint8_t mods = get_mods(), weak = get_weak_mods(), oneshot = get_oneshot_mods();
    clear_mods(); clear_weak_mods(); clear_oneshot_mods();
    send_keyboard_report();
    send_string(text);
    set_mods(mods); set_weak_mods(weak); set_oneshot_mods(oneshot);
    send_keyboard_report();
}

static void clipboard_shortcut(bool copy) {
    const uint8_t mods = get_mods(), weak = get_weak_mods(), oneshot = get_oneshot_mods();
    clear_mods(); clear_weak_mods(); clear_oneshot_mods();
    send_keyboard_report();
    uint16_t code = copy ? KC_C : KC_V;
    tap_code16(butterfly_held ? LCTL(code) : LCTL(LSFT(code)));
    set_mods(mods); set_weak_mods(weak); set_oneshot_mods(oneshot);
    send_keyboard_report();
}

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    // Custom handlers consume these events before the core autocorrect pass.
    // Reset its actual buffer so corrections cannot span a macro or mode change.
    if (record->event.pressed && keycode >= SAFE_RANGE) {
        process_autocorrect(KC_ESC, record);
    }
    if (keycode == LINUX_MODE) {
        if (record->event.pressed) change_mode();
        return false;
    }
    if (!linux_mode()) return true;
    if (keycode == KC_LALT) {
        if (record->event.pressed) {
            butterfly_held = true;
            butterfly_used = butterfly_forwarded = false;
        } else {
            if (butterfly_forwarded) unregister_code(KC_LALT);
            else if (!butterfly_used) tap_code(KC_LALT);
            reset_butterfly();
        }
        return false;
    }
    if (record->event.pressed && butterfly_held) {
        butterfly_used = true;
        if (keycode != LNX_COPY && keycode != LNX_PASTE && keycode != KC_L && !butterfly_forwarded) {
            register_code(KC_LALT);
            butterfly_forwarded = true;
        }
    }
    if (keycode == KC_L && butterfly_held) {
        if (record->event.pressed) {
            process_autocorrect(KC_ESC, record);
            literal_text("ls -ltr\n");
        }
        return false;
    }
    if (!process_select_word(keycode, record, SEL_WORD)) return false;
    switch (keycode) {
        case AC_SWITCH:
            if (record->event.pressed) linux_autocorrect = !linux_autocorrect;
            return false;
        case UPDIR:
            if (record->event.pressed) literal_text("../");
            return false;
        case LIST_LONG:
            if (record->event.pressed) literal_text("ls -ltr\n");
            return false;
        case WIN_SIG:
            if (record->event.pressed) literal_text("Thanks,\nAlastair.\n");
            return false;
        case LNX_TERM:
            if (record->event.pressed) tap_code16(LCTL(LALT(KC_T)));
            return false;
        case LNX_COPY:
        case LNX_PASTE:
            if (record->event.pressed) clipboard_shortcut(keycode == LNX_COPY);
            return false;
        case LNX_OVERVIEW:
            if (record->event.pressed) tap_code(KC_LGUI);
            return false;
        case LNX_APPS:
            if (record->event.pressed) tap_code16(LGUI(KC_A));
            return false;
    }
    return true;
}

bool dynamic_macro_record_start_user(int8_t direction) {
    macro_recording = true;
    return true;
}
bool dynamic_macro_record_end_user(int8_t direction) {
    macro_recording = false;
    return true;
}
bool dynamic_macro_record_key_user(int8_t direction, keyrecord_t *record) {
    return true;
}
bool dynamic_macro_play_user(int8_t direction) { return true; }
bool dynamic_macro_valid_key_user(uint16_t keycode, keyrecord_t *record) {
    // Never record mode transitions; their replay could escape Linux mode.
    return linux_mode() && keycode != LINUX_MODE;
}

bool rgb_matrix_indicators_advanced_user(uint8_t led_min, uint8_t led_max) {
    if (!linux_mode()) return true;
    if (layer_state_is(LINUX_FN)) {
        for (uint8_t row = 0; row < MATRIX_ROWS; ++row) {
            for (uint8_t col = 0; col < MATRIX_COLS; ++col) {
                uint8_t led = g_led_config.matrix_co[row][col];
                if (led == NO_LED || led < led_min || led >= led_max) continue;
                uint16_t code = keymap_key_to_keycode(LINUX_FN, (keypos_t){col, row});
                if (code > KC_TRNS) rgb_matrix_set_color(led, 0, 160, 0);
                else rgb_matrix_set_color(led, 50, 50, 50);
            }
        }
    }
    // Keep the original Caps Lock warning while leaving Escape informative.
    if (host_keyboard_led_state().caps_lock) {
        for (uint8_t led = led_min; led < led_max; ++led) {
            rgb_matrix_set_color(led, 255, 0, 0);
        }
    }
    if (led_min == 0 && led_max > 0) {
        if (macro_recording) rgb_matrix_set_color(0, 255, 0, 0);
        else if (linux_autocorrect) rgb_matrix_set_color(0, 0, 180, 0);
        else rgb_matrix_set_color(0, 255, 100, 0);
    }
    return true;
}
