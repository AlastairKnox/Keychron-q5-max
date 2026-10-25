# Initial repository verification

Verified on 25 October 2026:

- The repository build script extracted its bundled pinned source, overlaid the tracked personal keymap and built the ANSI Q5 Max firmware successfully.
- The host checks passed for mode isolation, standard-layout recovery, saved-map migration, clipboard modifiers, the ls -ltr macro with Enter, and QMK dynamic-macro playback.
- Encoded-dictionary regression checks passed for interested/uninterested/disinterested and ordinary intrest/abotu corrections.
- The initial recovery download checksums match the archived files.
- Build output and the development environment are ignored by Git.

The build used the workspace ARM GCC 14.2.1 toolchain and QMK CLI 1.2.0. Host checks mock keyboard I/O; they are not a complete USB/Ubuntu/hardware simulation. This repository preparation did not flash the keyboard or deploy the Hugo site.

## v1.0.1 - 26 October 2026

Build and host tests passed for repeated unchanged rear-switch reports while in Linux mode, including retaining the autocorrect setting and active Fn layer. Existing tests still verify explicit mode exit and real switch movement. Physical sleep/wake testing remains outstanding.

## v1.0.2 - 26 October 2026

Firmware build and host regression tests passed for the new P/H/keypad-0 actions through both triggers, press-only execution, Alt isolation, saved-map migration and preservation of deliberate remaps. Dynamic macro replay now uses Fn+O. Sleep and dictionary regression checks still pass. Ubuntu calculator launch and physical keyboard operation require hardware testing.
