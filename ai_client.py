import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

ALLSIDES_RATINGS = {
    "New York Times": "Lean Left",
    "Fox News": "Right",
    "CNN": "Left",
    "NPR": "Lean Left",
    "Wall Street Journal": "Center",
    "BBC News": "Center",
    "Associated Press": "Lean Left",
    "Reuters": "Center",
    "HuffPost": "Left",
    "Washington Post": "Lean Left",
    "New York Post": "Lean Right",
    "Bloomberg": "Lean Left",
    "Axios": "Lean Left",
    "Politico": "Lean Left"
}

def get_bias_rating(source_name):
    for known_source, rating in ALLSIDES_RATINGS.items():
        if known_source.lower() in source_name.lower():
            return rating
    return "Unknown"

def generate_daily_brief(news_data):
    if not model:
        return "<h2>AI Unvailable</h2><p>Please set the <code>GEMINI_API_KEY</code> environment variable to generate the daily brief.</p>"

    # Ensure news_data isn't inherently empty
    if not news_data:
        return "<h2>No Data</h2><p>No news data was available to summarize.</p>"

    text_payload = "Here are today's top US national and world affairs stories across various sources:\n\n"
    for source, data in news_data.items():
        text_payload += f"Source: {source} (Bias: {data['rating']})\n"
        for story in data.get('stories', []):
            text_payload += f"- {story['title']}: {story['summary']}\n"
        text_payload += "\n"

    prompt = f"""
{text_payload}

Based on the news stories provided above from multiple sources of varying political biases, write a comprehensive but concise one-page daily brief.
Your goal is to synthesize the overlapping stories into cohesive narratives, identifying the major themes of the day in US national and world affairs. 
Highlight where different sources emphasize different aspects of the same story.

Format your response strictly in HTML (using tags like <h2>, <h3>, <p>, <ul>, <li>, <strong>) as it will be injected directly into a webpage. Do not include ```html blocks or outer <html> tags. Start straight with an <h2> title like "Today's Top Stories".
"""

    try:
        response = model.generate_content(prompt)
        html_content = response.text.strip()
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        if html_content.startswith("```"):
            html_content = html_content[3:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]
            
        return html_content.strip()
    except Exception as e:
        print(f"Failed to generate daily brief: {e}")
        return f"<p>Error generating daily brief: {e}</p>"
