import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import os

# --- CONFIGURATION ---
SUBREDDITS = ["stocks_picks", "ValueInvesting", "pennystocks"]
RAW_DATA_FILE = "Raw_Reddit_Text.csv"

# Make this look like a custom bot so Reddit doesn't mistake it for a malicious scraper
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
REDDIT_COOKIES = "reddit_session=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml9hNWJxNmJxYyIsImV4cCI6MTc4OTUyNjcwNi42NjUxMjgsImlhdCI6MTc3Mzg4ODMwNi42NjUxMjgsImp0aSI6IkhkdTlZUjBYVzJ5ZTM1b0NBa0lNOWRTeEMwcGVqUSIsImF0IjoxLCJjaWQiOiJjb29raWUiLCJsY2EiOjE2MTIzNDAzMzk2MjksInNjcCI6ImVKeUtqZ1VFQUFEX193RVZBTGsiLCJmbG8iOjJ9.TzyIClwpUV3XMF8-m-uJA7nHYqDmE0WP5F5KM5pxBzxMZ5CmyKejoiDA4N31WWXnYoYV-3VwZdqti3ZlaIHjz_srjYEWl1fk_d8cq3K9XbLD8sIeuDiWDyL3e41Azq26ERoFXamQfiMr0ewbAAkFjX58LrrsLufnVsOt4TQfPTk6XPkkfbtgTc3OdIG_Y-i5SgYNPR2rlBEcy6PAMFB5HVz1Kau2E6hfWruuDuNuRfaXRZHHoKgM-1DLhDrAPWJUf90gS5RfZzKqD9qd2J0VONG32uFcbrq_Bk-RbC7W1MAN4tfx30_IRHlXcD3_jtBrvVvK8Wq-yHDO6j0NRnhWgw;" # Put your cookie here again!

DAYS_TO_SCRAPE = 90 

def immortal_request(url, max_retries=1000):
    retries = 0
    headers = {
        'User-Agent': USER_AGENT,
        'Cookie': REDDIT_COOKIES
    }
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            # Specifically handle the 429 Too Many Requests error
            if response.status_code == 429:
                print("  [RATE LIMIT] Reddit 429 hit. Sleeping for 60 seconds...")
                time.sleep(60)
                retries += 1
                continue
                
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"  [NETWORK PAUSE] Sleeping 15s... ({e})")
            time.sleep(15)
            retries += 1
    return None

def save_to_csv(data_list):
    """Saves a batch of data immediately to prevent data loss."""
    if data_list:
        df = pd.DataFrame(data_list)
        if os.path.exists(RAW_DATA_FILE):
            df.to_csv(RAW_DATA_FILE, mode='a', header=False, index=False)
        else:
            df.to_csv(RAW_DATA_FILE, index=False)

def scrape_reddit():
    cutoff_time = (datetime.now() - timedelta(days=DAYS_TO_SCRAPE)).timestamp()
    
    # Load existing data to avoid re-scraping the same exact comments
    existing_ids = set()
    if os.path.exists(RAW_DATA_FILE):
        existing_df = pd.read_csv(RAW_DATA_FILE)
        existing_ids = set(existing_df['ID'].astype(str).tolist())
        print(f"Loaded {len(existing_ids)} previously scraped items.")

    for sub in SUBREDDITS:
        print(f"\nVacuuming r/{sub}...")
        url = f"https://www.reddit.com/r/{sub}/new.json?limit=100"
        
        while url:
            data = immortal_request(url)
            if not data or 'data' not in data or 'children' not in data['data']:
                break
                
            posts = data['data']['children']
            if not posts:
                break
                
            for post in posts:
                p_data = post['data']
                post_id = p_data.get('id', '')
                created_utc = p_data.get('created_utc', 0)
                
                # Stop if we hit the time limit
                if created_utc < cutoff_time:
                    url = None 
                    break
                
                title = p_data.get('title', '')
                permalink = p_data.get('permalink', '')
                post_date = datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
                
                current_batch = [] # Hold the data just for this post
                
                # 1. Save the Post Body
                selftext = p_data.get('selftext', '')
                if selftext and f"post_{post_id}" not in existing_ids:
                    current_batch.append({
                        "ID": f"post_{post_id}",
                        "Date": post_date,
                        "Subreddit": sub,
                        "Parent_Title": title,
                        "Text_To_Analyze": selftext,
                        "URL": f"https://reddit.com{permalink}"
                    })
                    existing_ids.add(f"post_{post_id}")
                
                # 2. Scrape the Top Comments
                comments_url = f"https://www.reddit.com{permalink}.json?sort=top"
                comment_data = immortal_request(comments_url)
                
                if comment_data and len(comment_data) > 1:
                    comments = comment_data[1]['data']['children']
                    for comment in comments[:15]:
                        if 'data' in comment and 'body' in comment['data']:
                            c_id = comment['data'].get('id', '')
                            c_body = comment['data'].get('body', '')
                            
                            if f"comment_{c_id}" not in existing_ids:
                                current_batch.append({
                                    "ID": f"comment_{c_id}",
                                    "Date": post_date,
                                    "Subreddit": sub,
                                    "Parent_Title": title, 
                                    "Text_To_Analyze": c_body,
                                    "URL": f"https://reddit.com{permalink}{c_id}"
                                })
                                existing_ids.add(f"comment_{c_id}")
                
                # THE FIX: Save to CSV instantly after finishing the post
                save_to_csv(current_batch)
                
                print(f"  Scraped post: {post_id}")
                time.sleep(3) # Give Reddit 3 full seconds of breathing room
            
            # Handle Pagination
            if url: 
                after = data['data'].get('after')
                if after:
                    url = f"https://www.reddit.com/r/{sub}/new.json?limit=100&after={after}"
                else:
                    url = None

if __name__ == "__main__":
    scrape_reddit()