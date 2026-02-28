# US News Aggregator

A standalone desktop application built with Python, Flask, and PyWebView that aggregates news from a customizable list of sources, categorizes them by AllSides bias ratings, and uses Google's Gemini AI to generate a cohesive "Daily Brief".

## Architecture
- **Backend:** Flask web server fetching RSS feeds from Google News.
- **Frontend:** Vanilla HTML/CSS injected via Flask templates, optimized for instant load times using AJAX.
- **Desktop Wrapper:** PyWebView running a native desktop window over the local Flask instance.

## Requirements

You must have Python 3 installed. The application relies on the following Python packages:
- `flask`
- `requests`
- `beautifulsoup4`
- `pywebview`
- `google-generativeai`
- `feedparser`

*(Note: These are handled automatically by the launch script, but you can view them in `requirements.txt`).*

## Setup and Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/denichols297/news-aggregator.git
   cd news-aggregator
   ```

2. **Configure your News Sources:**
   You can easily edit the sources the app monitors by modifying the `sources.txt` file. Add or remove any source simply by placing its name on a new line (e.g., "The New York Times", "NPR", "Fox News").

3. **Injecting the Gemini API Key:**
   To use the "View Daily Brief" feature, the application needs access to the Google Gemini AI. The application looks for an environment variable named `GEMINI_API_KEY`. It is **not** stored in the code.
   
   Before running the app, export the key in your terminal:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. **Launch the Application:**
   Run the included `run.sh` script. This script automatically creates an isolated Python virtual environment, installs all necessary dependencies from `requirements.txt`, and launches the desktop app.
   ```bash
   ./run.sh
   ```

   *(Note: You can safely run this script multiple times; it will just activate the existing virtual environment if it detects one).*

---
*The app is designed to load instantly and fetch the RSS stories asynchronously. The Daily Brief button routes to a dedicated interface while the AI synthesizes the day's stories in the background.*
