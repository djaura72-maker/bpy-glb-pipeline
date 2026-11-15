#!/usr/bin/env bash
set -euo pipefail

BLENDER_BIN="${BLENDER_BIN:-/Applications/Blender.app/Contents/MacOS/Blender}"
if [ ! -x "$BLENDER_BIN" ]; then
  BLENDER_BIN="$(command -v blender || true)"
fi

if [ -z "$BLENDER_BIN" ]; then
  echo "Blender executable not found. Set BLENDER_BIN=/path/to/Blender and retry."
  exit 1
fi

"$BLENDER_BIN" --background --python pipeline.py -- --demo --output output --name demo_asset
