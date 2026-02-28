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

# Package the app via osacompile AppleScript wrapper
echo "Creating macOS App Launcher wrapper..."
rm -rf "US News Aggregator.app"
osacompile -o "US News Aggregator.app" -e "do shell script \"cd '$DIR' && ./run.sh > /dev/null 2>&1 &\""

# Replace the default icon with our generated icon
cp icon.icns "US News Aggregator.app/Contents/Resources/applet.icns"
touch "US News Aggregator.app"

echo "Build complete. App launcher is located at US News Aggregator.app"
