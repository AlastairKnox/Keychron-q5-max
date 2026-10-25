# Q5 Max Custom Linux firmware - recovery and editing

Release: **q5-max-linux-v1.0.0**, archived 25 October 2026.

This kit is intended to survive loss of the original development computer, chat and personal source repository. It contains the complete pinned Keychron/QMK source tree, the four source dependencies required for this STM32 board, the personal keymap, editable autocorrect dictionary, generated dictionary header, release binaries, checksums and host tests. Source does not need to be downloaded from GitHub to build this board.

A working Linux machine and standard build tools are still required. This is a source recovery archive, not a complete offline operating system or compiler image. Package installation below needs access to Ubuntu repositories and PyPI. The lockfile records the Python package versions used; compiler versions and upstream revisions are in build-manifest.json.

## 1. Install the build tools on Ubuntu

```bash
sudo apt update
sudo apt install git make gcc gcc-arm-none-eabi binutils-arm-none-eabi \
  libnewlib-arm-none-eabi libnewlib-dev dfu-util \
  python3 python3-venv python3-dev libhidapi-hidraw0 libusb-1.0-0
```

The release was built with ARM GCC 14.2.1 (20241119), QMK CLI 1.2.0 and Python 3.14. The exact package versions from the working Python environment are pinned in python-requirements.lock.txt. A different host or compiler may need updated dependencies; retain the original source and release binaries for comparison.

## 2. Extract and build

Extract the full source archive and enter its top-level folder:

```bash
tar -xzf q5-max-linux-v1.0.0-source.tar.gz
cd q5-max-linux-v1.0.0
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r python-requirements.lock.txt
./build.sh
```

The result is:

```text
qmk_firmware/keychron_q5_max_ansi_encoder_alastair.bin
```

The script runs `make keychron/q5_max/ansi_encoder:alastair SKIP_GIT=yes`. The archive intentionally has no Git metadata. QMK may print a warning that this is not a Git repository; that is expected for this deliberately self-contained source snapshot. The required submodule source is already expanded into lib/chibios, lib/chibios-contrib, lib/lufa and lib/printf. Do not run qmk setup or download another QMK checkout over this snapshot. Uninitialised dependencies for other boards and optional test frameworks are not included, and are not needed for this target.

The supplied firmware/ directory also contains the original compiled personal binary and a standard manufacturer-keymap binary. SHA256SUMS identifies the files in this kit. A fresh build need not have the same checksum, because QMK embeds build metadata; the saved binary is the authoritative archived release.

## 3. Where to edit

Personal source directory:

```text
qmk_firmware/keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair/
```

| File | Purpose |
|---|---|
| keymap.c | Six keymaps, encoder map, custom actions, mode switching, butterfly modifier handling, lighting and saved-map migrations |
| config.h | Six dynamic layers, macro buffer, key delay and lighting options |
| rules.mk | Enabled QMK features and build options |
| autocorrect_dict.txt | Editable 3,666-entry typo/correction dictionary |
| autocorrect_data.h | Generated lookup table used by the firmware |
| select_word.c / select_word.h | Word/line selection helper |

The standard Mac/Windows layers occupy indices 0-3 and the rear switch depends on them. Linux base and Fn are 4 and 5. Linux mode is selected through default_layer_state so that QMK dynamic macros can clear temporary layers without exiting Linux mode.

Keep personal actions gated to Linux mode. In particular, autocorrect, Shift+Backspace, left-butterfly handling and custom lighting must not affect standard mode.

The left butterfly is the third bottom-row key immediately before Space. Its Linux keycode is KC_LALT, despite its printed legend. Its modifier event is deferred so clipboard and command macros can consume it without leaking Alt to the host; other combinations forward normal Alt behaviour. The right butterfly is unchanged.

### Add or change a text macro

Find LIST_LONG and WIN_SIG in keymap.c for examples. LIST_LONG types `ls -ltr\n`, where the newline sends Enter. It is mapped on Fn+L and intercepted on left-butterfly+L. literal_text() clears and restores modifiers so text macros are literal even when triggered with a modifier held.

Append new custom keycodes to the enum; do not reorder existing ones. VIA may retain numeric keycodes in saved mappings between flashes. A changed default keymap alone may not change a saved mapping. keyboard_post_init_user() contains targeted migrations for the previous square binding and the formerly transparent Fn+L binding. Add similarly narrow migrations when necessary; preserve independently remapped keys.

The dynamic macro controls are different from these fixed text macros: Fn+R/S/P records, stops and replays a temporary sequence, lost after restart.

### Change autocorrect

Edit autocorrect_dict.txt, then regenerate inside the source tree using the activated environment:

```bash
cd qmk_firmware
qmk generate-autocorrect-data \
  keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair/autocorrect_dict.txt \
  -o keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair/autocorrect_data.h
cd ..
./build.sh
```

Do not edit only the comment list in autocorrect_data.h: the encoded bytes must be regenerated too. Typo rules can match inside correctly spelled words unless bounded appropriately. The unbounded `erested -> arrested` entry was removed because it changed `interested` to `intarrested`. All other entries from the prior dictionary remain. Autocorrect starts on; Fn+A toggles it for the current powered session.

## 4. Check the build and behaviour

```bash
python3 verification/run.py "$PWD/qmk_firmware"
python3 verification/check_dictionary.py
```

The host tests compile the real keymap and QMK dynamic-macro engine against mocked keyboard services. They cover mode isolation, standard-layout recovery, autocorrect gating, clipboard modifier handling, the listing macro including Enter, saved-map migration and temporary macro playback. The dictionary test walks the encoded tables and checks the interested-word regression plus ordinary corrections.

These checks are not a complete hardware simulation. After changes, check actual typing, Ubuntu shortcut handling, the knob, mode transitions, macros and any USB/wireless transport you rely on. KEYBOARD-GUIDE.md describes the current controls.

## 5. Flash the keyboard

For the personal image supplied in this kit:

```bash
sudo dfu-util -w -d 0483:df11 -a 0 -s 0x08000000:leave \
  -D firmware/keychron_q5_max_ansi_encoder_alastair.bin
```

For a newly built image, replace the path with `qmk_firmware/keychron_q5_max_ansi_encoder_alastair.bin`.

Enter the sudo password before disconnecting the keyboard. Use Cable mode and a data-capable USB cable. Hold Escape before reconnecting USB and briefly afterward. The command waits for the STM32 bootloader, writes the firmware and requests normal operation. A fallback is holding the reset button under the spacebar, just left of the main switch, while reconnecting USB.

Escape-at-startup can clear saved mappings; export any worth retaining first. The ordinary reset button is a bootloader entry method, not a guarantee that saved mappings are reset. Targeted migrations in the personal keymap handle the earlier defaults.

The target is **Keychron Q5 Max ANSI with knob**, not Q5, Q5 Pro, Q5 HE, ISO or JIS. To restore standard manufacturer firmware, use the same procedure with firmware/keychron_q5_max_ansi_encoder_keychron.bin.

## 6. Preserve future releases

After editing, save a new version of the custom source and full recovery kit, rebuilt binary, SHA256SUMS, updated guide and build manifest together. Update the website's download links and retain the older version as a fallback. Do not silently overwrite an archived release.

Upstream files and helpers retain their original licence notices. The complete upstream tree includes the relevant licences; the archive does not claim ownership of Keychron, QMK, ChibiOS, LUFA or Select Word.
