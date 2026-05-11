import requests
import time
import json
import os
import pandas as pd
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# --- 1. CONFIGURATION ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    # PASTE YOUR EXACT REDDIT COOKIE HERE
    "Cookie": "reddit_session=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml9hNWJxNmJxYyIsImV4cCI6MTc4OTUyNjcwNi42NjUxMjgsImlhdCI6MTc3Mzg4ODMwNi42NjUxMjgsImp0aSI6IkhkdTlZUjBYVzJ5ZTM1b0NBa0lNOWRTeEMwcGVqUSIsImF0IjoxLCJjaWQiOiJjb29raWUiLCJsY2EiOjE2MTIzNDAzMzk2MjksInNjcCI6ImVKeUtqZ1VFQUFEX193RVZBTGsiLCJmbG8iOjJ9.TzyIClwpUV3XMF8-m-uJA7nHYqDmE0WP5F5KM5pxBzxMZ5CmyKejoiDA4N31WWXnYoYV-3VwZdqti3ZlaIHjz_srjYEWl1fk_d8cq3K9XbLD8sIeuDiWDyL3e41Azq26ERoFXamQfiMr0ewbAAkFjX58LrrsLufnVsOt4TQfPTk6XPkkfbtgTc3OdIG_Y-i5SgYNPR2rlBEcy6PAMFB5HVz1Kau2E6hfWruuDuNuRfaXRZHHoKgM-1DLhDrAPWJUf90gS5RfZzKqD9qd2J0VONG32uFcbrq_Bk-RbC7W1MAN4tfx30_IRHlXcD3_jtBrvVvK8Wq-yHDO6j0NRnhWgw;" 
}

SUBREDDITS = ["stocks_picks", "ValueInvesting", "pennystocks"]
RAW_LOG_FILE = "Raw_Live_Log.csv"
AGGREGATED_FILE = "Live_Daily_Signals.csv"

# Set your target model here! 
# qwen2.5:14b is recommended for 16GB VRAM. Use qwen2.5:32b if you want max accuracy and don't mind it being slower.
TARGET_MODEL = "qwen2.5:14b" 



def immortal_request(method, url, max_retries=1000, **kwargs):
    """
    Wraps requests to make them survive wifi drops, closed laptop lids, and Ollama timeouts.
    It will just pause and keep trying until the connection comes back.
    """
    retries = 0
    while retries < max_retries:
        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=15, **kwargs)
            else:
                response = requests.post(url, timeout=300, **kwargs)
                
            response.raise_for_status() # Raise an error for bad status codes
            return response
            
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"\n[NETWORK PAUSE] Connection lost or sleeping. Waiting for internet to return... ({e})")
            time.sleep(15) # Wait 15 seconds and try again
            retries += 1
        except Exception as e:
            print(f"\n[ERROR] Unexpected request error: {e}")
            time.sleep(15)
            retries += 1
            
    print("Max retries hit. Shutting down gracefully.")
    return None

# --- 2. THE DUPLICATE GATEKEEPER ---
def load_seen_signals():
    """Loads previously processed signals so we don't double-count them."""
    seen = set()
    if os.path.exists(RAW_LOG_FILE):
        df = pd.read_csv(RAW_LOG_FILE)
        for _, row in df.iterrows():
            seen.add(f"{row['Permalink']}_{row['Ticker']}")
    return seen

def append_to_raw_log(signal_dict):
    """Instantly saves a new signal to the running ledger."""
    file_exists = os.path.exists(RAW_LOG_FILE)
    keys = ["Date", "Subreddit", "Ticker", "Sentiment", "Permalink", "Original_Text"]
    
    with open(RAW_LOG_FILE, 'a', newline='', encoding='utf-8-sig') as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=keys)
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: signal_dict.get(k, '') for k in keys})

# --- 3. THE UNIFIED LLM BRAIN ---
def analyze_with_llm(text, parent_context=""):
    """
    Passes text to the LLM to simultaneously extract tickers (resolving names) and sentiment.
    Returns a list of dictionaries: [{'ticker': 'AAPL', 'sentiment': 'POSITIVE'}]
    """
    clean_text = text.replace('\n', ' ')[:2000] 
    if not clean_text.strip():
        return []

    context_prompt = f"Context (Main Post Title): {parent_context}\n" if parent_context else ""
    
    prompt = f"""
    You are a quantitative data extraction engine. Read the following Reddit text.
    1. Identify any publicly traded companies mentioned (by their proper name, slang, or $TICKER).
    2. Resolve the company to its official US stock ticker (e.g., if they say "Palantir", output "PLTR").
    3. Determine the sentiment strictly toward that company (POSITIVE, NEGATIVE, NEUTRAL).
    
    {context_prompt}
    Text: "{clean_text}"
    
    CRITICAL INSTRUCTIONS:
    - Output ONLY a valid JSON object with a single key called "tickers".
    - The value of "tickers" must be an array of objects.
    - Format exactly like this:
      {{"tickers": [{{"ticker": "PLTR", "sentiment": "POSITIVE"}}, {{"ticker": "DIS", "sentiment": "NEGATIVE"}}]}}
    - If no companies are discussed, output: {{"tickers": []}}
    """

    try:
        response = immortal_request("POST",
            "http://localhost:11434/api/generate",
            json={
                "model": TARGET_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json", # Forces strict JSON output
                "options": {"temperature": 0.0, "top_p": 0.1}
            }
        )
        
        if response.status_code == 200:
            result_text = response.json()['response']
            extracted_data = json.loads(result_text)
            
            if isinstance(extracted_data, list):
                return extracted_data
            elif isinstance(extracted_data, dict) and "tickers" in extracted_data:
                return extracted_data["tickers"]
            else:
                return []
        else:
            return []
            
    except Exception as e:
        print(f"LLM Parsing Error: {e}")
        return []

# --- 4. THE LIVE SCRAPER ---
def get_new_posts(subreddit):
    print(f"\nScanning r/{subreddit} for new posts...")
    valid_posts = []
    after_token = None
    cutoff_time = (datetime.now() - timedelta(days=365)).timestamp()
    
    while True:
        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=100"
        if after_token:
            url += f"&after={after_token}"
            
        response = immortal_request("GET",url, headers=HEADERS)
        if response.status_code != 200:
            break

        data = response.json().get('data', {})
        posts = data.get('children', [])
        
        if not posts:
            break
            
        reached_old_posts = False
        
        for post in posts:
            post_data = post['data']
            created_utc = post_data.get('created_utc')
            
            if created_utc < cutoff_time:
                reached_old_posts = True
                break
                
            valid_posts.append({
                "subreddit": subreddit,
                "title": post_data.get('title'),
                "text": post_data.get('title', '') + " \n " + post_data.get('selftext'),
                "permalink": post_data.get('permalink'),
                "date": datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d'), 
                "comments_count": post_data.get('num_comments')
            })
            
        if reached_old_posts or not data.get('after'):
            break
            
        after_token = data.get('after')
        time.sleep(2) 

    return valid_posts

def get_post_comments(permalink):
    url = f"https://www.reddit.com{permalink}.json"
    response = immortal_request("GET",url, headers=HEADERS)
    time.sleep(2) 
    
    if response.status_code != 200: return []
    try:
        comment_data = response.json()[1]['data']['children']
        extracted = []
        for comment in comment_data:
            if comment['kind'] == 't1':
                body = comment['data'].get('body', '')
                if body and body not in ["[deleted]", "[removed]"]:
                    extracted.append({
                        "text": body,
                        "permalink": comment['data'].get('permalink'),
                        "date": datetime.fromtimestamp(comment['data'].get('created_utc')).strftime('%Y-%m-%d')
                    })
        return extracted
    except Exception:
        return []

# --- 5. MASTER EXECUTION PIPELINE ---
if __name__ == "__main__":
    
    seen_signals = load_seen_signals()
    print(f"Loaded {len(seen_signals)} previously processed signals. Proceeding with Live Scan...")
    
    new_signals_found = 0
    
    for subreddit in SUBREDDITS:
        recent_posts = get_new_posts(subreddit)
        
        for idx, post in enumerate(recent_posts):
            
            # 1. Ask LLM to process Main Post
            llm_results = analyze_with_llm(post['text'])
            
            # Anti-spam filter: only log if the post focuses on 1-4 stocks
            if llm_results and len(llm_results) <= 4:
                for item in llm_results:
                    ticker = item.get('ticker', '').upper().replace('$', '')
                    sentiment = item.get('sentiment', 'NEUTRAL').upper()
                    
                    if ticker and sentiment in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
                        signal_id = f"{post['permalink']}_{ticker}"
                        
                        # GATEKEEPER: Skip if already processed
                        if signal_id not in seen_signals:
                            signal_data = {
                                "Date": post['date'],
                                "Subreddit": post['subreddit'],
                                "Ticker": ticker,
                                "Sentiment": sentiment,
                                "Permalink": post['permalink'],
                                "Original_Text": post['text'].replace('\n', ' ')[:300]
                            }
                            append_to_raw_log(signal_data)
                            seen_signals.add(signal_id)
                            new_signals_found += 1
            
            # 2. Process Comments
            if post['comments_count'] > 0:
                comments = get_post_comments(post['permalink'])
                for comment in comments[:15]: 
                    
                    c_llm_results = analyze_with_llm(comment['text'], parent_context=post['title'])
                    
                    if c_llm_results and len(c_llm_results) <= 2:
                        for item in c_llm_results:
                            ticker = item.get('ticker', '').upper().replace('$', '')
                            sentiment = item.get('sentiment', 'NEUTRAL').upper()
                            
                            if ticker and sentiment in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
                                signal_id = f"{comment['permalink']}_{ticker}"
                                
                                if signal_id not in seen_signals:
                                    signal_data = {
                                        "Date": comment['date'],
                                        "Subreddit": post['subreddit'],
                                        "Ticker": ticker,
                                        "Sentiment": sentiment,
                                        "Permalink": comment['permalink'],
                                        "Original_Text": comment['text'].replace('\n', ' ')[:300]
                                    }
                                    append_to_raw_log(signal_data)
                                    seen_signals.add(signal_id)
                                    new_signals_found += 1

    print(f"\nLive Scan Complete. Found and logged {new_signals_found} NEW signals.")
    
    # --- 6. AGGREGATE THE RAW LEDGER FOR THE BACKTESTER ---
    if os.path.exists(RAW_LOG_FILE):
        print("Re-compiling the Master Daily Signals board...")
        df = pd.read_csv(RAW_LOG_FILE)
        
        sentiment_map = {"POSITIVE": 1, "NEUTRAL": 0, "NEGATIVE": -1}
        df['Sent_Val'] = df['Sentiment'].map(sentiment_map)
        
        aggregated_df = df.groupby(['Date', 'Ticker']).agg(
            Total_Mentions=('Ticker', 'count'),
            Avg_Sentiment_Score=('Sent_Val', 'mean'),
            Subreddits_Appeared=('Subreddit', lambda x: ', '.join(set(x)))
        ).reset_index()
        
        def assign_final_label(score):
            if score >= 0.33: return "POSITIVE"
            elif score <= -0.33: return "NEGATIVE"
            else: return "NEUTRAL"
            
        aggregated_df['Consensus_Sentiment'] = aggregated_df['Avg_Sentiment_Score'].apply(assign_final_label)
        aggregated_df = aggregated_df.sort_values('Date', ascending=False)
        
        aggregated_df.to_csv(AGGREGATED_FILE, index=False)
        print(f"Aggregated {len(df)} raw logs into {len(aggregated_df)} unique daily trading signals.")
        print(f"Board updated: {AGGREGATED_FILE}")