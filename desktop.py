import webview
import threading
import time
import sys
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
