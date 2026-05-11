import requests
import time
import json
import csv
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# --- 1. CONFIGURATION ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # PASTE YOUR EXACT REDDIT COOKIE HERE
    "Cookie": "reddit_session=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml9hNWJxNmJxYyIsImV4cCI6MTc4OTUyNjcwNi42NjUxMjgsImlhdCI6MTc3Mzg4ODMwNi42NjUxMjgsImp0aSI6IkhkdTlZUjBYVzJ5ZTM1b0NBa0lNOWRTeEMwcGVqUSIsImF0IjoxLCJjaWQiOiJjb29raWUiLCJsY2EiOjE2MTIzNDAzMzk2MjksInNjcCI6ImVKeUtqZ1VFQUFEX193RVZBTGsiLCJmbG8iOjJ9.TzyIClwpUV3XMF8-m-uJA7nHYqDmE0WP5F5KM5pxBzxMZ5CmyKejoiDA4N31WWXnYoYV-3VwZdqti3ZlaIHjz_srjYEWl1fk_d8cq3K9XbLD8sIeuDiWDyL3e41Azq26ERoFXamQfiMr0ewbAAkFjX58LrrsLufnVsOt4TQfPTk6XPkkfbtgTc3OdIG_Y-i5SgYNPR2rlBEcy6PAMFB5HVz1Kau2E6hfWruuDuNuRfaXRZHHoKgM-1DLhDrAPWJUf90gS5RfZzKqD9qd2J0VONG32uFcbrq_Bk-RbC7W1MAN4tfx30_IRHlXcD3_jtBrvVvK8Wq-yHDO6j0NRnhWgw;" 
}

# --- 2. LOCAL LLM BRAIN (Ollama) ---
def analyze_with_llm(text, parent_context=""):
    """
    Passes text to local Llama 3.1 to extract tickers and contextual sentiment.
    Returns a list of dictionaries: [{'ticker': 'AAPL', 'sentiment': 'POSITIVE'}]
    """
    clean_text = text.replace('\n', ' ')[:2000] 
    if not clean_text.strip():
        return []

    context_prompt = f"Context (Main Post Title): {parent_context}\n" if parent_context else ""
    
    # We remove the specific ticker examples from the prompt so it doesn't copy them
    prompt = f"""
    You are a strictly logical financial data extraction bot. Read the following Reddit text.
    Your ONLY job is to identify valid US stock tickers mentioned explicitly in the text.
    Ignore common words that look like tickers (e.g., FOR, ALL, NOW, ARE, EDIT, YOLO, PUMP, MOON).
    
    If you find a valid ticker, determine the author's sentiment towards buying or holding that specific stock. 
    Use ONLY: "POSITIVE", "NEGATIVE", or "NEUTRAL".
    
    {context_prompt}
    Text to analyze: "{clean_text}"
    
    CRITICAL INSTRUCTIONS:
    - If there are NO explicitly mentioned stock tickers in the text, you MUST output an empty array: []
    - DO NOT guess. DO NOT hallucinate large tech companies if they are not written in the text.
    - Output your response STRICTLY as a JSON array of objects. 
    - Format exactly like this if a ticker is found: [{{"ticker": "XYZ", "sentiment": "POSITIVE"}}]
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1",
                "prompt": prompt,
                "stream": False,
                "format": "json",
                # NEW: Setting temperature to 0 makes the model highly analytical and removes hallucination
                "options": {
                    "temperature": 0.0,
                    "top_p": 0.1
                }
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
            
    except Exception:
        return []

# --- 3. REDDIT SCRAPING MODULE ---
def get_paginated_posts(subreddit, target_count=100):
    print(f"\nFetching posts from r/{subreddit} (Target: {target_count})...")
    valid_posts = []
    after_token = None
    
    now = datetime.now()
    one_month_ago = (now - timedelta(days=30)).timestamp()
    one_year_ago = (now - timedelta(days=365)).timestamp()
    
    while len(valid_posts) < target_count:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t=year&limit=100"
        if after_token:
            url += f"&after={after_token}"
            
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch data. HTTP {response.status_code}. Check your cookie!")
            break

        data = response.json()['data']
        posts = data['children']
        
        for post in posts:
            post_data = post['data']
            created_utc = post_data.get('created_utc')
            
            if one_year_ago <= created_utc <= one_month_ago:
                valid_posts.append({
                    "subreddit": subreddit,
                    "title": post_data.get('title'),
                    "text": post_data.get('title', '') + " \n " + post_data.get('selftext', ''),
                    "permalink": post_data.get('permalink'),
                    "date": datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d'),
                    "upvotes": post_data.get('ups'),
                    "comments_count": post_data.get('num_comments')
                })
                
                if len(valid_posts) >= target_count:
                    break
        
        after_token = data.get('after')
        if not after_token:
            break
            
        print(f"  ...Collected {len(valid_posts)} posts so far. Fetching next page...")
        time.sleep(2) 

    return valid_posts

def get_post_comments(permalink):
    url = f"https://www.reddit.com{permalink}.json"
    response = requests.get(url, headers=HEADERS)
    time.sleep(2) # Crucial sleep to avoid bans
    
    if response.status_code != 200:
        return []

    try:
        comment_data = response.json()[1]['data']['children']
        extracted_comments = []
        for comment in comment_data:
            if comment['kind'] == 't1':
                body = comment['data'].get('body', '')
                if body and body not in ["[deleted]", "[removed]"]:
                    extracted_comments.append({
                        "text": body,
                        "upvotes": comment['data'].get('ups', 0),
                        "date": datetime.fromtimestamp(comment['data'].get('created_utc')).strftime('%Y-%m-%d')
                    })
        return extracted_comments
    except Exception:
        return []

# --- 4. FINANCIAL ALPHA MODULE ---
def get_performance_alpha(ticker, post_date_str, benchmark="SPY"):
    start_date = datetime.strptime(post_date_str, '%Y-%m-%d')
    end_date = start_date + timedelta(days=45) 
    try:
        data = yf.download([ticker, benchmark], start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)['Close']
    except Exception:
        return None

    if data.empty or ticker not in data.columns:
        return None

    data = data.dropna()
    intervals = {"1_Day": 1, "1_Week": 5, "1_Month": 21}
    results = {"Start_Price": round(data[ticker].iloc[0], 2) if not data.empty else "N/A"}

    for label, trading_days in intervals.items():
        if len(data) > trading_days:
            p0_stock, p0_bench = data[ticker].iloc[0], data[benchmark].iloc[0]
            pT_stock, pT_bench = data[ticker].iloc[trading_days], data[benchmark].iloc[trading_days]
            stock_return = (pT_stock - p0_stock) / p0_stock
            bench_return = (pT_bench - p0_bench) / p0_bench
            results[f"{label}_Alpha"] = round((stock_return - bench_return) * 100, 2)
        else:
            results[f"{label}_Alpha"] = "N/A"
    return results

# --- 5. MASTER EXECUTION PIPELINE ---
if __name__ == "__main__":
    target_subreddit = "stocks_picks" 
    sample_size = 1000
    
    print("STAGE 1: Scraping Top Posts...")
    scraped_posts = get_paginated_posts(target_subreddit, target_count=sample_size)
    
    raw_signals = []
    mentions_counter = {} # Format: {'2023-10-05': {'AAPL': 2, 'PLTR': 1}}

    print("\nSTAGE 2: Analyzing Text with Llama 3.1 (This requires some GPU compute)...")
    for idx, post in enumerate(scraped_posts):
        print(f"Processing Post {idx+1}/{len(scraped_posts)} (Comments: {post['comments_count']})")
        
        # 1. Ask LLM to process Main Post
        llm_results = analyze_with_llm(post['text'])
        
        # Focus filter: Only log if it focuses on 1-3 stocks to avoid portfolio dumps
        if llm_results and len(llm_results) <= 3:
            for item in llm_results:
                ticker = item.get('ticker', '').upper().replace('$', '')
                sentiment = item.get('sentiment', 'NEUTRAL').upper()
                
                if ticker:
                    # Update our daily mention counter
                    if post['date'] not in mentions_counter:
                        mentions_counter[post['date']] = {}
                    mentions_counter[post['date']][ticker] = mentions_counter[post['date']].get(ticker, 0) + 1
                    
                    raw_signals.append({
                        "Date": post['date'],
                        "Source_Type": "POST",
                        "Subreddit": post['subreddit'],
                        "Ticker": ticker,
                        "Sentiment": sentiment,
                        "Upvotes": post['upvotes'],
                        "Parent_Title": post['title'],
                        "Original_Text": post['text'].replace('\n', ' ')[:500]
                    })
        
        # 2. Process Comments ONLY if > 5 comments
        if post['comments_count'] > 5:
            comments = get_post_comments(post['permalink'])
            for comment in comments[:20]:
                # Pass the parent title so the LLM understands the context
                c_llm_results = analyze_with_llm(comment['text'], parent_context=post['title'])
                
                if c_llm_results and len(c_llm_results) <= 2:
                    for item in c_llm_results:
                        ticker = item.get('ticker', '').upper().replace('$', '')
                        sentiment = item.get('sentiment', 'NEUTRAL').upper()
                        
                        if ticker:
                            if comment['date'] not in mentions_counter:
                                mentions_counter[comment['date']] = {}
                            mentions_counter[comment['date']][ticker] = mentions_counter[comment['date']].get(ticker, 0) + 1
                            
                            raw_signals.append({
                                "Date": comment['date'],
                                "Source_Type": "COMMENT",
                                "Subreddit": post['subreddit'],
                                "Ticker": ticker,
                                "Sentiment": sentiment,
                                "Upvotes": comment['upvotes'],
                                "Parent_Title": post['title'],
                                "Original_Text": comment['text'].replace('\n', ' ')[:500]
                            })

    print("\nSTAGE 3: Fetching Financial Alpha Data and Saving to CSV...")
    
    ordered_keys = ["Date", "Source_Type", "Subreddit", "Ticker", "Mentions_That_Day", 
                    "Sentiment", "Upvotes", "Start_Price", "1D_Alpha(%)", 
                    "1W_Alpha(%)", "1M_Alpha(%)", "Parent_Title", "Original_Text"]
    
    csv_filename = f"{target_subreddit}_Llama3_alpha_data.csv"
    yf_cache = {}
    valid_count = 0
    
    # Continuous Save Block
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=ordered_keys)
        writer.writeheader()
        
        for signal in raw_signals:
            ticker = signal['Ticker']
            date = signal['Date']
            
            signal['Mentions_That_Day'] = mentions_counter[date][ticker]
            
            cache_key = f"{ticker}_{date}"
            if cache_key not in yf_cache:
                yf_cache[cache_key] = get_performance_alpha(ticker, date)
                time.sleep(0.5) 
                
            alpha_data = yf_cache[cache_key]
            
            if alpha_data:
                signal["Start_Price"] = alpha_data.get('Start_Price', 'N/A')
                signal["1D_Alpha(%)"] = alpha_data.get('1_Day_Alpha', 'N/A')
                signal["1W_Alpha(%)"] = alpha_data.get('1_Week_Alpha', 'N/A')
                signal["1M_Alpha(%)"] = alpha_data.get('1_Month_Alpha', 'N/A')
                
                writer.writerow({k: signal[k] for k in ordered_keys})
                f.flush() 
                valid_count += 1

    print(f"\nSUCCESS! Processed and saved {valid_count} valid signals.")
    print(f"Data is safely stored in {csv_filename}")