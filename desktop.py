import webview
import threading
import time
import sys
import os
import re

def load_shell_env():
    """Attempt to find and load GEMINI_API_KEY from user dotfiles."""
    home = os.path.expanduser("~")
    for rc_file in [".zshrc", ".bashrc", ".bash_profile"]:
        rc_path = os.path.join(home, rc_file)
        if os.path.exists(rc_path):
            try:
                with open(rc_path, 'r') as f:
                    content = f.read()
                    # Look for export GEMINI_API_KEY="key" or export GEMINI_API_KEY=key
                    match = re.search(r'export\s+GEMINI_API_KEY\s*=\s*["\']?([^"\'\n]+)["\']?', content)
                    if match:
                        os.environ["GEMINI_API_KEY"] = match.group(1)
                        print(f"Loaded GEMINI_API_KEY from {rc_path}")
                        return
            except Exception as e:
                print(f"Error reading {rc_path}: {e}")

# Load env variables BEFORE importing the app
load_shell_env()

from app import app

def start_flask():
    try:
        app.run(port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Flask failed to start: {e}")

if __name__ == '__main__':
    print("Starting US News Aggregator Desktop App...")
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()
    
    # Wait for flask to start
    time.sleep(1)

    window = webview.create_window(
        'US News Aggregator', 
        'http://127.0.0.1:5000', 
        width=1400, 
        height=900
    )
    
    webview.start()
    sys.exit()
