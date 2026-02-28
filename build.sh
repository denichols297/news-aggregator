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

# Install PyInstaller
pip install pyinstaller

# Convert the PNG to an ICNS file for macOS
sips -s format icns icon.png --out icon.icns

# Package the app
# -w: windowed (no console)
# -n: app name
# -i: icon
# --add-data: bundle the templates and sources.txt
pyinstaller --noconfirm --windowed --name "US News Aggregator" \
    --icon "icon.icns" \
    --add-data "templates:templates" \
    --add-data "sources.txt:." \
    desktop.py

echo "Build complete. App is located in dist/US News Aggregator.app"
