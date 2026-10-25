# Keychron Q5 Max - Custom Linux firmware

Personal firmware for the **Keychron Q5 Max ANSI with knob**, retaining standard Mac/Windows layouts and adding Custom Linux mode for Ubuntu.

Current archived release: **v1.0.0** (25 October 2026).

## Current controls

- **Fn+Space:** enter/leave Linux mode. The rear switch and restart restore a standard layout.
- Tap left/right Shift for `(`/`)`; hold for normal Shift. **Shift+Backspace:** Delete.
- **Fn+A:** autocorrect, initially on. **Fn+C:** Caps Word.
- **Fn+D:** type `../`. **Fn+L or left butterfly+L:** type `ls -ltr` and press Enter.
- **Fn+M:** type `Thanks,\nAlastair.\n`.
- **Triangle / Square:** Ctrl+Shift+C / Ctrl+Shift+V. Hold the left butterfly for Ctrl+C / Ctrl+V instead.
- **Circle:** open terminal. **Fn+circle:** select word; add Shift for line selection.
- Knob: volume; press to mute; hold Fn to scroll.
- **Fn+R/S/P:** record, stop, replay a temporary macro.
- Escape: green = autocorrect on; amber = off; red = recording. Typing heatmap and Fn-key lighting are retained.

The left butterfly is immediately before Space and is mapped to left Alt in the Linux keymap. Ordinary Alt shortcuts remain available. Desktop/media response depends on the host application's bindings. Autocorrect has 3,666 rules; the unbounded `erested -> arrested` rule was removed because it altered `interested`.

See [the complete feature guide](docs/FEATURES.md) and [printable A5 landscape desk card](docs/cheat-sheet.pdf).

## What is backed up here

The editable personal source is in `keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair/`.

**The full recovery archive is deliberately included in Git**, under `recovery/`, so the first push preserves the pinned upstream source and required dependencies as well as the personal keymap. It is approximately 64 MiB, below GitHub's per-file limit. Keep this baseline immutable; use versioned GitHub Releases for additional full snapshots rather than repeatedly replacing a large archive in Git history.

The recovery kit contains Keychron/QMK commit `2b493ff95f2665db719b1e95c91babb5036e72f3` from branch `2025q3`, required ChibiOS/ChibiOS-Contrib/LUFA/printf sources, original compiled personal and manufacturer firmware, dictionary source, build script and tests. It does not require this chat, the original desktop or another GitHub checkout to recover the board implementation. A Linux system and standard build tools are still needed; this is not an offline OS/compiler image.

- [Detailed recovery instructions](docs/RECOVER.md)
- [Source recovery archive](recovery/q5-max-linux-v1.0.0-source.tar.gz)
- [Original release binary](recovery/keychron_q5_max_ansi_encoder_alastair.bin)
- [Build provenance](recovery/build-manifest.json)
- [Recovery download checksums](recovery/SHA256SUMS)

## Build the tracked source on Ubuntu

Install tools:

```bash
sudo apt update
sudo apt install git make gcc gcc-arm-none-eabi binutils-arm-none-eabi \
  libnewlib-arm-none-eabi libnewlib-dev dfu-util \
  python3 python3-venv python3-dev libhidapi-hidraw0 libusb-1.0-0
```

From this repository's root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock.txt
./scripts/build.sh
```

The script extracts the pinned source archive into ignored `build/`, overlays the **current tracked keymap**, and compiles with `SKIP_GIT=yes`. No upstream clone/submodule download is necessary. A warning that the extracted QMK folder is not a Git repository is expected.

Result:

```text
artifacts/keychron_q5_max_ansi_encoder_alastair.bin
```

The archived release used ARM GCC 14.2.1, QMK CLI 1.2.0 and Python 3.14. The Python packages are pinned in `requirements.lock.txt`. Other host/compiler versions may need dependency adjustments. Rebuilt firmware hashes can differ because QMK embeds build metadata; checksums identify the supplied release binary.

## Edit, check and rebuild

Edit the tracked keymap under `keyboards/`, not the disposable copy under `build/`. `keymap.c` contains maps, encoder actions, macros and behaviour; `config.h`/`rules.mk` enable features. The `autocorrect_dict.txt` file is editable, while `autocorrect_data.h` is generated.

To regenerate the dictionary after editing it, build once to restore the pinned QMK tree, then run from the repository root with the Python environment active:

```bash
repo_dir="$PWD"
cd build/q5-max-linux-v1.0.0/qmk_firmware
qmk generate-autocorrect-data \
  "$repo_dir/keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair/autocorrect_dict.txt" \
  -o "$repo_dir/keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair/autocorrect_data.h"
cd "$repo_dir"
./scripts/build.sh
```

Keep standard layer indices 0-3, Linux layers 4-5 and existing custom-keycode enum values stable. Append new custom keycodes instead of reordering them. VIA can retain old numeric mappings; `keyboard_post_init_user()` contains narrow upgrade migrations for changed defaults. Preserve independent user remaps.

Checks after a build:

```bash
python3 verification/run.py "$PWD/build/q5-max-linux-v1.0.0/qmk_firmware"
python3 verification/check_dictionary.py
```

The host tests exercise the real keymap and QMK's dynamic-macro code against mocked keyboard services. They do not replace a physical keyboard check. The dictionary regression fixture is the old header in `verification/`; it is not part of the firmware build. Update tests appropriately when intentionally changing dictionary rules.

The source of the printable card is `scripts/make-cheat-sheet.py`. It requires ReportLab and pypdf; these optional document libraries are not part of the firmware build environment.

## Flash a new build

```bash
sudo dfu-util -w -d 0483:df11 -a 0 -s 0x08000000:leave \
  -D artifacts/keychron_q5_max_ansi_encoder_alastair.bin
```

Enter the sudo password before disconnecting USB. Use Cable mode and a data-capable cable. Hold Escape before reconnecting and briefly afterward; the command waits and then flashes. The reset button beneath the spacebar, left of its main switch, is the fallback bootloader entry. Export saved mappings first because Escape-at-startup can reset them. This target is not compatible with Q5/Q5 Pro/Q5 HE or ISO/JIS layouts.

## Release checklist

1. Rebuild and run the host/dictionary checks; test physical behaviour.
2. Update the feature guide, printable card and website article.
3. Commit tracked source and tag a new version.
4. Upload its firmware, source/recovery archives, manifest and SHA256 checksums as versioned GitHub Release assets. Preserve the v1.0.0 baseline.
5. Keep a second copy of the recovery kit with the Hugo website backup.

See [third-party notices](THIRD-PARTY-NOTICES.md) for licensing. No credentials, build environment or website content are required in this repository.
