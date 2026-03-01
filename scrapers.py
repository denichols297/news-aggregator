import os
import urllib.parse
import feedparser
from bs4 import BeautifulSoup
from ai_client import get_bias_rating, get_factual_reporting

def load_sources(filepath):
    if not os.path.exists(filepath):
        return []
        
    with open(filepath, 'r') as f:
        sources = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return sources

def get_google_news_rss(source_name):
    query = f'source:"{source_name}" (US OR "national" OR "world" OR "international" OR "foreign affairs" OR "politics")'
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    return url

def clean_html(raw_html):
    if not raw_html:
        return ""
    cleantext = BeautifulSoup(raw_html, "html.parser").text
    return cleantext.strip()

def fetch_rss_stories(url, limit=5):
    stories = []
    try:
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:limit]:
            title = entry.get('title', 'No Title')
            
            if " - " in title:
                title = " - ".join(title.split(" - ")[:-1])
                
            raw_summary = entry.get('description', '')
            clean_summary = clean_html(raw_summary)
            link = entry.get('link', '')
            
            # Fast raw feed loading
            summary_text = clean_summary[:200] + ("..." if len(clean_summary) > 200 else clean_summary)
            
            stories.append({
                "title": title,
                "summary": summary_text,
                "url": link
            })
            
    except Exception as e:
        print(f"Error fetching RSS from {url}: {e}")
        
    return stories

def get_news_for_sources(sources):
    news_data = {}
    
    for source in sources:
        print(f"Fetching news for {source}...")
        rss_url = get_google_news_rss(source)
        stories = fetch_rss_stories(rss_url, limit=5)
        rating = get_bias_rating(source)
        factual = get_factual_reporting(source)
        
        news_data[source] = {
            "rating": rating,
            "factual_rating": factual,
            "stories": stories
        }
        
    return news_data
