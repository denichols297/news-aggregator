import sys
import os
import time
import threading
from flask import Flask, render_template, jsonify

try:
    from scrapers import load_sources, get_news_for_sources
    from ai_client import generate_daily_brief
except ImportError:
    pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, template_folder=resource_path('templates'))

news_cache = {
    "data": None,
    "last_updated": 0,
    "brief": None
}
cache_lock = threading.Lock()
CACHE_DURATION = 3600 # 1 hour

def get_cached_or_fetch_news():
    global news_cache
    should_update = False
    with cache_lock:
        if news_cache["data"] is None or (time.time() - news_cache["last_updated"] > CACHE_DURATION):
            should_update = True
            
    if should_update:
        try:
            print("Updating news cache...")
            
            # Use the live text file so changes are picked up dynamically
            live_sources_path = os.path.expanduser("~/.gemini/antigravity/scratch/news-aggregate/sources.txt")
            if os.path.exists(live_sources_path):
                sources_file = live_sources_path
            else:
                sources_file = resource_path('sources.txt')
                
            sources = load_sources(sources_file)
            data = get_news_for_sources(sources)
            with cache_lock:
                news_cache["data"] = data
                news_cache["last_updated"] = time.time()
                # Invalidate the brief when news updates
                news_cache["brief"] = None
            print("News cache updated successfully.")
        except Exception as e:
            print(f"Failed to fetch news: {e}")
            
    with cache_lock:
        return news_cache.get("data", {})

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/')
def index():
    # Instantly return the pure HTML shell
    return render_template('index.html')

@app.route('/columns')
def columns():
    # This route is hit via an AJAX call so the spinner can display in the UI
    data = get_cached_or_fetch_news()
    return render_template('columns.html', news=data)

@app.route('/brief')
def brief():
    # Instantly return the empty Brief shell with a loading spinner
    return render_template('brief.html')

@app.route('/api/generate_brief')
def api_generate_brief():
    global news_cache
    
    # Needs to ensure news data is available first
    data = get_cached_or_fetch_news()
    
    with cache_lock:
        existing_brief = news_cache.get("brief")
        
    if not existing_brief:
        print("Generating Daily Brief (Background Process)...")
        new_brief = generate_daily_brief(data)
        with cache_lock:
            news_cache["brief"] = new_brief
            existing_brief = new_brief
            
    return jsonify({"html": existing_brief})

if __name__ == '__main__':
    # No pre-fetching!
    app.run(debug=True, port=5000)
