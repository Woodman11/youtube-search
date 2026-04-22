#!/bin/bash
set -e

echo "==> Installing build dependencies..."
venv/bin/pip install pyinstaller rumps -q

echo "==> Building app bundle..."
venv/bin/pyinstaller \
  --windowed \
  --name "My YouTube Search" \
  --add-data "extension/icons:icons" \
  --hidden-import youtube_transcript_api \
  --noconfirm \
  app.py

echo ""
echo "==> Done! App is at: dist/My YouTube Search.app"
echo "    Drag it to /Applications to install."
