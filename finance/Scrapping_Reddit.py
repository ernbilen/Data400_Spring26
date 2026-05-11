import requests
import time
import re
import random
from datetime import datetime, timedelta

# Remember to use your actual cookie from the previous step
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": "reddit_session=YOUR_LONG_COOKIE_STRING_HERE;" 
}

def extract_tickers(text):
    cash_tags = re.findall(r'\$[A-Za-z]{1,5}', text)
    bare_tags = re.findall(r'\b[A-Z]{2,5}\b', text)
    all_tickers = set([t.replace('$', '') for t in cash_tags + bare_tags])
    ignore_list = {"A", "I", "THE", "FOR", "AND", "DD", "YOLO", "EDIT", "WSB", "IT"}
    return list(all_tickers - ignore_list)

def get_historical_random_sample(subreddit, target_count=10):
    # Target the 'top' endpoint for the past 'year'
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t=year&limit=100"
    
    print(f"Fetching top posts of the year from r/{subreddit}...")
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

    data = response.json()
    posts = data['data']['children']
    
    # Define our time boundaries (Unix Timestamps)
    now = datetime.now()
    six_months_ago = (now - timedelta(days=180)).timestamp()
    one_year_ago = (now - timedelta(days=365)).timestamp()
    
    valid_posts = []
    
    for post in posts:
        post_data = post['data']
        created_utc = post_data.get('created_utc')
        
        # FILTER 1: Is it between 6 and 12 months old?
        if one_year_ago <= created_utc <= six_months_ago:
            
            full_text = post_data.get('title', '') + " " + post_data.get('selftext', '')
            tickers = extract_tickers(full_text)
            
            # FILTER 2: Does it contain a stock ticker?
            if tickers:
                post_date = datetime.fromtimestamp(created_utc)
                valid_posts.append({
                    "subreddit": subreddit,
                    "title": post_data.get('title'),
                    "tickers": tickers,
                    "date": post_date.strftime('%Y-%m-%d'),
                    "upvotes": post_data.get('ups'),
                    "comments": post_data.get('num_comments')
                })

    print(f"Found {len(valid_posts)} total posts matching the timeframe and ticker criteria.")
    
    # Shuffle the list to ensure our sample is random, not just the absolute highest upvoted
    random.shuffle(valid_posts)
    
    # Return only the amount we need (e.g., 10)
    return valid_posts[:target_count]

# --- Main Execution ---
if __name__ == "__main__":
    sampled_pennystocks = get_historical_random_sample("pennystocks", target_count=10)
    time.sleep(3) # Respect the server, avoid bans
    sampled_stockpicks = get_historical_random_sample("stock_picks", target_count=10)
    
    print("\n--- Final Sampled Data ---")
    for item in sampled_pennystocks + sampled_stockpicks:
        print(f"{item['date']} | r/{item['subreddit']} | Tickers: {item['tickers']} | {item['title'][:50]}...")