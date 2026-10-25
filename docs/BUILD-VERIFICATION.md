# Initial repository verification

Verified on 25 October 2026:

- The repository build script extracted its bundled pinned source, overlaid the tracked personal keymap and built the ANSI Q5 Max firmware successfully.
- The host checks passed for mode isolation, standard-layout recovery, saved-map migration, clipboard modifiers, the ls -ltr macro with Enter, and QMK dynamic-macro playback.
- Encoded-dictionary regression checks passed for interested/uninterested/disinterested and ordinary intrest/abotu corrections.
- The initial recovery download checksums match the archived files.
- Build output and the development environment are ignored by Git.

The build used the workspace ARM GCC 14.2.1 toolchain and QMK CLI 1.2.0. Host checks mock keyboard I/O; they are not a complete USB/Ubuntu/hardware simulation. This repository preparation did not flash the keyboard or deploy the Hugo site.
