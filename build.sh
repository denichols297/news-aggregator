#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Ensure venv exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Convert the PNG to an ICNS file for macOS if not present
if [ ! -f "icon.icns" ]; then
    sips -s format icns icon.png --out icon.icns
fi

# Package the app using PyInstaller
# --windowed prevent a separate python terminal icon
# --icon uses our custom icon natively
echo "Packaging application with PyInstaller..."
pip install pyinstaller || true

rm -rf "dist/US News Aggregator.app" build/

pyinstaller --noconfirm --windowed --name "US News Aggregator" \
    --icon "icon.icns" \
    --add-data "templates:templates" \
    --add-data "sources.txt:." \
    desktop.py

echo "Build complete. App is located in dist/US News Aggregator.app"

