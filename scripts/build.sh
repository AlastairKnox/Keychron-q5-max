#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
kit_dir="$repo_dir/build/q5-max-linux-v1.0.0"
keymap_path="keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair"
if [[ ! -f "$kit_dir/qmk_firmware/Makefile" ]]; then
    mkdir -p "$repo_dir/build"
    tar -xzf "$repo_dir/recovery/q5-max-linux-v1.0.0-source.tar.gz" -C "$repo_dir/build"
fi
# Tracked source is authoritative; build/ is disposable.
cp -a "$repo_dir/$keymap_path/." "$kit_dir/qmk_firmware/$keymap_path/"
cd "$kit_dir/qmk_firmware"
make keychron/q5_max/ansi_encoder:alastair SKIP_GIT=yes -j"${JOBS:-4}"
mkdir -p "$repo_dir/artifacts"
cp keychron_q5_max_ansi_encoder_alastair.bin "$repo_dir/artifacts/"
printf '\nBuilt firmware: %s\n' "$repo_dir/artifacts/keychron_q5_max_ansi_encoder_alastair.bin"
