import requests
import time
import re
import json
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import warnings

warnings.filterwarnings('ignore')

# --- 1. CONFIGURATION ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # PASTE YOUR EXACT REDDIT COOKIE HERE
    "Cookie": "reddit_session=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml9hNWJxNmJxYyIsImV4cCI6MTc4OTUyNjcwNi42NjUxMjgsImlhdCI6MTc3Mzg4ODMwNi42NjUxMjgsImp0aSI6IkhkdTlZUjBYVzJ5ZTM1b0NBa0lNOWRTeEMwcGVqUSIsImF0IjoxLCJjaWQiOiJjb29raWUiLCJsY2EiOjE2MTIzNDAzMzk2MjksInNjcCI6ImVKeUtqZ1VFQUFEX193RVZBTGsiLCJmbG8iOjJ9.TzyIClwpUV3XMF8-m-uJA7nHYqDmE0WP5F5KM5pxBzxMZ5CmyKejoiDA4N31WWXnYoYV-3VwZdqti3ZlaIHjz_srjYEWl1fk_d8cq3K9XbLD8sIeuDiWDyL3e41Azq26ERoFXamQfiMr0ewbAAkFjX58LrrsLufnVsOt4TQfPTk6XPkkfbtgTc3OdIG_Y-i5SgYNPR2rlBEcy6PAMFB5HVz1Kau2E6hfWruuDuNuRfaXRZHHoKgM-1DLhDrAPWJUf90gS5RfZzKqD9qd2J0VONG32uFcbrq_Bk-RbC7W1MAN4tfx30_IRHlXcD3_jtBrvVvK8Wq-yHDO6j0NRnhWgw;" 
}

# The mega-sweep array. Add or remove subreddits as needed.
SUBREDDITS = ["stocks_picks", "ValueInvesting", "pennystocks"]
TARGET_PER_SUB = 300 # Try to get 300 posts from each sub (Total ~900 posts)

# --- 2. HYBRID EXTRACTION & SENTIMENT ---
def extract_potential_tickers(text):
    """Stage 1: High Recall Regex (Finds potential tickers to pass to the LLM)"""
    cash_tags = re.findall(r'\$[A-Za-z]{1,5}', text)
    bare_tags = re.findall(r'\b[A-Z]{2,5}\b', text)
    all_tickers = set([t.replace('$', '').upper() for t in cash_tags + bare_tags])
    
    # Expanded ignore list for common capitalized English words
    ignore_list = {"A", "I", "THE", "FOR", "AND", "DD", "YOLO", "EDIT", "WSB", "IT", "ALL", "NOW", "ARE", "HAS", "CAN", "OUT", "NEW", "ONE", "ANY", "SEE"}
    return list(all_tickers - ignore_list)

def get_targeted_sentiment(ticker, text, parent_context=""):
    """Stage 2: High Precision LLM (Classifies sentiment for ONE specific verified ticker)"""
    clean_text = text.replace('\n', ' ')[:1500] 
    context_prompt = f"Context (Main Post Title): {parent_context}\n" if parent_context else ""
    
    prompt = f"""
    Analyze the following text from a financial forum. 
    Determine the author's specific sentiment toward the stock ticker: {ticker}.
    If the text does not actually discuss {ticker} as a company or stock, output "INVALID".
    Use ONLY ONE WORD: "POSITIVE", "NEGATIVE", "NEUTRAL", or "INVALID". Do not explain your reasoning.

    {context_prompt}
    Text: "{clean_text}"
    """
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.0, "top_p": 0.1} # Zero hallucination setting
            }
        )
        if response.status_code == 200:
            result = response.json()['response'].strip().upper()
            for valid_label in ["POSITIVE", "NEGATIVE", "NEUTRAL", "INVALID"]:
                if valid_label in result:
                    return valid_label
        return "INVALID"
    except Exception as e:
        print(f"LLM Error: {e}")
        return "INVALID"

# --- 3. REDDIT SCRAPING MODULE ---
def get_paginated_posts(subreddit, target_count):
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
            print(f"Failed to fetch data from r/{subreddit}. HTTP {response.status_code}.")
            break

        data = response.json().get('data', {})
        posts = data.get('children', [])
        
        if not posts:
            break
            
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
            print(f"Reached the end of Reddit's history for r/{subreddit}.")
            break
            
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

# --- 4. AGGREGATION & ALPHA MODULE ---
def clean_and_aggregate_signals(raw_signals_list):
    """Removes duplicates and aggregates daily sentiment/hype."""
    print("\nSTAGE 3: Aggregating daily signals to remove duplicates...")
    df = pd.DataFrame(raw_signals_list)
    
    if df.empty:
        return df
        
    # Convert sentiment strings to numbers to calculate consensus
    sentiment_map = {"POSITIVE": 1, "NEUTRAL": 0, "NEGATIVE": -1}
    df['Sent_Val'] = df['Sentiment'].map(sentiment_map)
    
    aggregated_df = df.groupby(['Date', 'Ticker']).agg(
        Total_Mentions=('Ticker', 'count'),
        Avg_Sentiment_Score=('Sent_Val', 'mean'),
        Total_Upvotes=('Upvotes', 'sum'),
        Subreddits_Appeared=('Subreddit', lambda x: ', '.join(set(x))),
        Sample_Text=('Original_Text', 'first') # Keep one text sample for reference
    ).reset_index()
    
    def assign_final_label(score):
        if score >= 0.33: return "POSITIVE"
        elif score <= -0.33: return "NEGATIVE"
        else: return "NEUTRAL"
        
    aggregated_df['Consensus_Sentiment'] = aggregated_df['Avg_Sentiment_Score'].apply(assign_final_label)
    aggregated_df = aggregated_df.sort_values('Date', ascending=False)
    
    print(f"Compressed {len(df)} raw mentions into {len(aggregated_df)} clean daily signals.")
    return aggregated_df

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
    
    all_raw_signals = []
    
    print("STAGE 1 & 2: Scraping and LLM Processing across subreddits...")
    
    for subreddit in SUBREDDITS:
        scraped_posts = get_paginated_posts(subreddit, target_count=TARGET_PER_SUB)
        
        for idx, post in enumerate(scraped_posts):
            print(f"[{subreddit}] Processing Post {idx+1}/{len(scraped_posts)} (Comments: {post['comments_count']})")
            
            # 1. Process Main Post
            post_tickers = extract_potential_tickers(post['text'])
            if post_tickers and len(post_tickers) <= 4:
                for ticker in post_tickers:
                    # Targeted LLM check
                    sentiment = get_targeted_sentiment(ticker, post['text'])
                    if sentiment != "INVALID":
                        all_raw_signals.append({
                            "Date": post['date'],
                            "Subreddit": post['subreddit'],
                            "Ticker": ticker,
                            "Sentiment": sentiment,
                            "Upvotes": post['upvotes'],
                            "Original_Text": post['text'].replace('\n', ' ')[:300]
                        })
            
            # 2. Process Comments ONLY if > 5 comments
            if post['comments_count'] > 5:
                comments = get_post_comments(post['permalink'])
                for comment in comments[:15]: # Take top 15 comments
                    comment_tickers = extract_potential_tickers(comment['text'])
                    if comment_tickers and len(comment_tickers) <= 2:
                        for ticker in comment_tickers:
                            # Targeted LLM check with parent context
                            sentiment = get_targeted_sentiment(ticker, comment['text'], parent_context=post['title'])
                            if sentiment != "INVALID":
                                all_raw_signals.append({
                                    "Date": comment['date'],
                                    "Subreddit": post['subreddit'],
                                    "Ticker": ticker,
                                    "Sentiment": sentiment,
                                    "Upvotes": comment['upvotes'],
                                    "Original_Text": comment['text'].replace('\n', ' ')[:300]
                                })

    # --- AGGREGATE AND FETCH ALPHA ---
    daily_signals_df = clean_and_aggregate_signals(all_raw_signals)
    
    print("\nSTAGE 4: Fetching Financial Alpha Data...")
    final_dataset = []
    yf_cache = {}
    
    # Iterate through the clean, deduplicated DataFrame
    for index, row in daily_signals_df.iterrows():
        ticker = row['Ticker']
        date = row['Date']
        
        cache_key = f"{ticker}_{date}"
        if cache_key not in yf_cache:
            yf_cache[cache_key] = get_performance_alpha(ticker, date)
            time.sleep(0.5) 
            
        alpha_data = yf_cache[cache_key]
        
        if alpha_data:
            # Reconstruct the row into a dictionary and add the financial data
            final_row = row.to_dict()
            final_row["Start_Price"] = alpha_data.get('Start_Price', 'N/A')
            final_row["1D_Alpha(%)"] = alpha_data.get('1_Day_Alpha', 'N/A')
            final_row["1W_Alpha(%)"] = alpha_data.get('1_Week_Alpha', 'N/A')
            final_row["1M_Alpha(%)"] = alpha_data.get('1_Month_Alpha', 'N/A')
            
            final_dataset.append(final_row)
            
            # Print update so you know it's working
            print(f" -> Logged Alpha for {ticker} on {date}")

    # --- FINAL EXPORT ---
    if final_dataset:
        final_df = pd.DataFrame(final_dataset)
        
        # Organize columns cleanly
        cols = ['Date', 'Ticker', 'Total_Mentions', 'Consensus_Sentiment', 'Total_Upvotes', 
                'Start_Price', '1D_Alpha(%)', '1W_Alpha(%)', '1M_Alpha(%)', 
                'Subreddits_Appeared', 'Sample_Text']
        
        final_df = final_df[cols]
        csv_filename = "Mega_Reddit_Alpha_Dataset.csv"
        
        final_df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        
        print(f"\nSUCCESS! Processed and saved {len(final_df)} highly validated signals.")
        print(f"Data is safely stored in {csv_filename}")
    else:
        print("\nNo valid ticker data could be processed.")