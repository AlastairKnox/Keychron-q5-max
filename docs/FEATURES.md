# Alastair’s Q5 Max — Custom Linux mode

Built for **Keychron Q5 Max ANSI with knob**, using Keychron’s official `2025q3` source at commit `2b493ff95f2665db719b1e95c91babb5036e72f3` (23 October 2026).

Both the manufacturer and personal firmware compile successfully. The keyboard has **not** been flashed. Your original uploaded source remains separate and unchanged.

## Everyday use

The keyboard starts in the normal Mac or Windows mode selected by the rear switch. Press **Fn+Space** to enter Custom Linux mode. Press it again to return to the standard mode you came from. Moving the rear OS switch also exits Custom Linux mode. Unplugging/restarting returns to the standard mode; Linux mode is deliberately not saved as the startup default.

Standard mode preserves the manufacturer’s keys and knob behaviour. Its only added shortcut is Fn+Space. Personal autocorrect, parentheses-on-Shift, macros and Shift+Backspace apply in Custom Linux mode.

### Linux shortcuts

| Control | Action |
|---|---|
| Fn+A | Toggle autocorrect; on initially after each keyboard restart |
| Tap left Shift | `(`; hold for normal Shift |
| Tap right Shift | `)`; hold for normal Shift |
| Period | Ordinary `.`; two taps give `..` |
| Shift+Backspace | Forward Delete |
| Fn+C | Caps Word: uppercase a word/identifier, then stop at a space |
| Fn+D | Type `../` once; repeat presses add more |
| Fn+L or left butterfly+L | Type `ls -ltr` and press Enter |
| Fn+M | Type `Thanks,` then `Alastair.` on the next line, followed by a newline |
| Knob clockwise / anticlockwise | Volume up / down |
| Press knob | Mute/unmute |
| Hold Fn and turn knob | Clockwise scroll down; anticlockwise scroll up |
| Fn+Page Up / Page Down | Home / End |
| Right Ctrl | Ordinary Ctrl; no double-tap layer switching |

The original 3,666-entry autocorrect dictionary is retained. It may correct code and paths: Fn+A turns it off when needed. The preference survives entering/leaving Linux mode during the same powered session, but starts on after restart. Try `abotu` followed by a space to check correction to `about`.

The old Teams greeting and period tap dance are removed.

### Your three symbol keys

These are the three top-row keys beside Delete, occupying the original F13/F14/F15 positions:

| Key | Action | Signal sent to Ubuntu |
|---|---|---|
| Circle (F13 position) | Open terminal | Ctrl+Alt+T |
| Triangle (F14 position) | Copy | Ctrl+Shift+C |
| Square (F15 position) | Paste | Ctrl+Shift+V |
| Fn+circle | Select word; repeat to extend; hold Shift for line selection | Windows/Linux editing shortcuts |

Desktop actions assume Ubuntu’s GNOME desktop and its usual bindings. No Ubuntu settings were changed. If a shortcut does not respond, check **Settings → Keyboard → View and Customize Shortcuts**. Terminal uses the configured terminal launcher, rather than a specific terminal application. Triangle and Square send Ctrl+Shift+C/V: these work in the user’s terminal and ChatGPT app, but other applications may assign them differently.

Hold the **left butterfly key immediately before Space** with Triangle/Square for **plain Ctrl+C / Ctrl+V**. Fn is not needed. From the left, the physical keys are Control, Option, Butterfly, Space. This third key is mapped to left Alt in the current Linux layout; its ordinary shortcuts (for example Alt+Tab) remain available. Its modifier press is deferred until the next key, so clipboard combinations do not also trigger an Alt menu.

The right butterfly key is unchanged. Fn+F3 still provides Activities/window overview; the dedicated Triangle/Square window actions have been replaced by clipboard actions.

### Function-row legends

F1–F12 type ordinary function keys in Custom Linux mode. Hold Fn for the pictured functions:

- F1/F2: standard screen-brightness events, left as-is; no monitor integration added.
- F3: Activities/window overview.
- F4: application grid (Super+A).
- F5/F6: keyboard backlight down/up.
- F7/F8/F9: previous track / play-pause / next track.
- F10/F11/F12: mute / volume down / volume up.

Media response depends on Ubuntu and the active player. These shortcuts still need a physical keyboard check.

### Record a temporary macro

1. Press **Fn+R**, then release both keys. Recording starts when R is released.
2. Perform the typing/editing sequence to record. It is also performed immediately.
3. Press **Fn+S** to stop.
4. Press **Fn+P**, then release, to replay in the currently focused application.

Escape glows red while recording. There is one exposed recording slot, with up to about 128 ordinary press/release pairs; modifiers and Fn combinations consume extra events. A new recording replaces the old one. Recordings disappear on restart. Nested playback is disabled. Exiting Linux mode stops an active recording. Avoid changing autocorrect settings between recording and playback if you want the same text transformations.

### Lighting

- Entering Linux mode selects the typing heatmap without saving over the previous standard-mode effect. Leaving restores that effect.
- Escape green: Linux autocorrect on.
- Escape amber: Linux autocorrect off.
- Escape red: macro recording.
- Holding Fn: assigned keys green, other keys grey; Escape retains its status colour.
- Caps Lock: the original all-red warning remains in Linux mode, except Escape continues showing status.

For lighting adjustments in Linux mode, hold Fn and use the numpad:

| Numpad keys | Adjustment |
|---|---|
| 7 / 8 | Previous / next effect |
| 4 / 5 | Brightness down / up |
| 9 / 6 | Effect speed up / down |
| 1 / 2 | Hue down / up |
| 3 / decimal | Saturation up / down |

Fn+Tab toggles lighting. Fn+B retains battery-level display; Fn+1/2/3/4 retain wireless host selection. No screen-brightness setup is required.

## Files

- `firmware/keychron_q5_max_ansi_encoder_alastair.bin`: personal firmware, including standard layouts and Custom Linux mode.
- `firmware/keychron_q5_max_ansi_encoder_keychron.bin`: separately built, unmodified manufacturer keymap at the same pinned source version. It has no Fn+Space personal mode.
- `keyboards/.../keymaps/alastair/`: all personal source files.
- `alastair-keymap.patch`: the same source as an additive patch; no manufacturer board files are edited.
- `build-manifest.json`: exact source version, dependency revisions and firmware checksums.
- `verification/`: build logs, test runner and results/limitations.

There are six internal layers: the stock Mac/Windows base+Fn pairs (0–3), and the personal Linux base+Fn pair (4–5). VIA is enabled, but the manufacturer’s four-layer Launcher/VIA screen may not expose the personal layers correctly. Use the supplied source to change personal bindings; do not assume the default remapping UI describes all six layers.

## Rebuild

With QMK’s Python tools, ARM compiler, newlib and dfu-suffix installed:

```sh
git clone --branch 2025q3 https://github.com/Keychron/qmk_firmware.git
cd qmk_firmware
git checkout 2b493ff95f2665db719b1e95c91babb5036e72f3
git submodule update --init --recursive
```

Copy this package’s `keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair` folder to the same location in the checkout, or apply `alastair-keymap.patch`. Then build, without flashing:

```sh
make keychron/q5_max/ansi_encoder:keychron
make keychron/q5_max/ansi_encoder:alastair
```

The build used QMK CLI 1.2.0 and ARM GCC 14.2.1. On this chat workspace the compiler and Python environment are under `work/`; no system packages were installed.

## Before the first flash

These firmware files are for the **ANSI Q5 Max with knob**, not the ISO/JIS Q5 Max, Q5, Q5 Pro or Q5 HE. Confirm the physical layout before flashing.

Export any VIA/Launcher mappings you want to keep. The six-layer layout uses a different saved-keymap arrangement, so initialise the keyboard’s saved settings for the new firmware rather than carrying old mappings across. The documented Escape-at-plug-in Bootmagic procedure clears saved settings as it enters the bootloader; back up first.

Use Cable mode and a USB cable. Keychron documents entering the bootloader by holding Escape while connecting USB, or using the reset button beneath the spacebar. No flashing command has been run here. After flashing and reconnecting, verify the standard layout first, then Fn+Space and the personal shortcuts.

Hardware checks are listed in `verification/results.md`. Firmware compilation and host tests cannot establish actual Ubuntu shortcut, USB or wireless behaviour.

## Flash directly from Ubuntu with dfu-util

Install the flashing program if needed:

```sh
sudo apt install dfu-util
```

Open a terminal in this package’s `firmware` folder. With the keyboard connected normally, run:

```sh
sudo dfu-util -w -d 0483:df11 -a 0 -s 0x08000000:leave -D keychron_q5_max_ansi_encoder_alastair.bin
```

Enter your sudo password before unplugging the keyboard. The `-w` option waits for the bootloader. Set the keyboard to Cable mode, unplug USB, hold Escape and reconnect USB. Release Escape once the DFU device is detected and downloading starts. Leave it connected until flashing finishes. The `:leave` option requests a return to normal keyboard operation; reconnect USB if needed, then press Fn+Space for Custom Linux mode.

This writes the personal firmware. To restore the separately built standard firmware later, use the same procedure with `keychron_q5_max_ansi_encoder_keychron.bin`. Export existing mappings before the first flash, as described above.

Command arguments match this checkout’s STM32 DFU settings in `platforms/chibios/bootloader.mk`. The installed dfu-util 0.11 help confirms `-w` waits for the device. This command has been documented, not executed.

## Clipboard update

This revision changes Triangle to Ctrl+Shift+C and Square to Ctrl+Shift+V, with left-butterfly combinations for plain Ctrl+C/V. It automatically migrates only the previous default square mapping if it is still saved in VIA. Other saved mappings are preserved. A full factory reset should not be necessary when updating from the first Custom Linux build.

Build and host checks pass, including modifier restoration, no stray Alt after a clipboard chord, ordinary Alt+Tab forwarding, and preserving an independently remapped square key. This revision has not been flashed or tested on the physical keyboard. The firmware filename is unchanged: use the newly packaged copy, whose checksum is recorded in build-manifest.json.

## Directory listing update

Fn+L and left-butterfly+L type `ls -ltr` followed by Enter in Linux mode. The command runs in the focused terminal; in other applications it types the same text and newline. The previous transparent Fn+L mapping is migrated without resetting other saved mappings.

Removed the unbounded `erested -> arrested` correction that matched the end of `interested`. All other dictionary entries remain unchanged; 3,666 entries remain.
