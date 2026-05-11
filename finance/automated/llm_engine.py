import pandas as pd
import requests
import json
import time
import os
import warnings

warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
RAW_DATA_FILE = "Raw_Reddit_Text.csv"
RAW_LOG_FILE = "Raw_Live_Log.csv"
AGGREGATED_FILE = "Live_Daily_Signals.csv"
OLLAMA_URL = "http://localhost:11434/api/generate"
TRACKER_FILE = "Processed_IDs.txt"

def immortal_ollama_request(prompt, max_retries=1000):
    retries = 0
    payload = {
        "model": "qwen2.5:14b",
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.0}
    }
    
    while retries < max_retries:
        try:
            # 5-Minute timeout to give the 14B model plenty of time
            response = requests.post(OLLAMA_URL, json=payload, timeout=700)
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            print(f"  [AI PAUSE] Engine busy or sleeping. Retrying in 15s... ({e})")
            time.sleep(15)
            retries += 1
    return None

def analyze_text(text, context=""):
    # THE SHIELD: Protect the GPU from massive walls of text
    safe_text = str(text)[:2000]
    safe_context = str(context)[:500]
    
    prompt = f"""
    You are a quantitative data extraction engine. Read the following Reddit text.
    1. Identify any publicly traded companies mentioned (by proper name, slang, or $TICKER).
    2. Resolve the company to its official US stock ticker.
    3. Determine the sentiment strictly toward that company (POSITIVE, NEGATIVE, NEUTRAL).
    
    Context: "{safe_context}"
    Text: "{safe_text}"
    
    CRITICAL INSTRUCTIONS:
    - Output ONLY a valid JSON object with a single key called "tickers".
    - The value of "tickers" must be an array of objects.
    - Format exactly like this:
      {{"tickers": [{{"ticker": "PLTR", "sentiment": "POSITIVE"}}]}}
    - If no companies are discussed, output: {{"tickers": []}}
    """
    
    raw_response = immortal_ollama_request(prompt)
    
    if raw_response:
        try:
            parsed = json.loads(raw_response)
            if isinstance(parsed, dict) and "tickers" in parsed:
                return parsed["tickers"]
        except json.JSONDecodeError:
            return []
    return []

def run_engine():
    if not os.path.exists(RAW_DATA_FILE):
        print(f"Error: {RAW_DATA_FILE} not found. Run your scraper first!")
        return

    print("Loading raw Reddit data...")
    raw_df = pd.read_csv(RAW_DATA_FILE)
    total_rows = len(raw_df)
    print(f"Total texts to process: {total_rows}")

    # Build the Gatekeeper using the new Tracker file
    processed_ids = set()
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            processed_ids = set(line.strip() for line in f)
        print(f"Resuming progress: {len(processed_ids)} texts already processed.")

    new_signals = 0
    for index, row in raw_df.iterrows():
        source_id = str(row['ID'])
        
        # The Gatekeeper: Skip instantly if the ID is in our tracker
        if source_id in processed_ids:
            continue 

        if index % 50 == 0:
            print(f"Processing {index}/{total_rows}...")

        extracted_data = analyze_text(text=row['Text_To_Analyze'], context=row['Parent_Title'])
        
        if not extracted_data:
            print(f"  [IGNORED] -> Row {index} (No tickers)")
        else:
            for item in extracted_data:

                # THE FIX: Force Python to check if the item is a dictionary first
                if not isinstance(item, dict):
                    print(f"  [WARNING] LLM returned garbage data format: {item}. Skipping.")
                    continue # Skip this broken item and move to the next one
            
                ticker = item.get('ticker', '').upper()
                sentiment = item.get('sentiment', '').upper()
                
                if ticker and sentiment in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
                    signal = {
                        "Date": row['Date'],
                        "Subreddit": row['Subreddit'],
                        "Ticker": ticker,
                        "Sentiment": sentiment,
                        "Source_ID": source_id,
                        "URL": row['URL']
                    }
                    
                    # Save the signal to the data ledger
                    signal_df = pd.DataFrame([signal])
                    signal_df.to_csv(RAW_LOG_FILE, mode='a', header=not os.path.exists(RAW_LOG_FILE), index=False)
                    print(f"  [SAVED] -> {ticker} ({sentiment})")
                    new_signals += 1
        
        # THE FIX: Always save the receipt, even if ignored
        with open(TRACKER_FILE, "a") as f:
            f.write(source_id + "\n")
        processed_ids.add(source_id)

    print(f"\nAI Processing Complete! Found {new_signals} new signals.")
    aggregate_signals()

def aggregate_signals():
    print(f"\nAggregating raw logs into {AGGREGATED_FILE}...")
    if not os.path.exists(RAW_LOG_FILE):
        print("No raw logs to aggregate.")
        return

    df = pd.read_csv(RAW_LOG_FILE)
    if df.empty:
        return

    # Group by Ticker and Date to match your original backtester format
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    aggregated = []

    for (date, ticker), group in df.groupby(['Date', 'Ticker']):
        subreddits = list(group['Subreddit'].unique())
        sentiments = group['Sentiment'].tolist()
        
        pos = sentiments.count('POSITIVE')
        neg = sentiments.count('NEGATIVE')
        
        if pos > neg:
            consensus = 'POSITIVE'
        elif neg > pos:
            consensus = 'NEGATIVE'
        else:
            consensus = 'NEUTRAL'
            
        aggregated.append({
            "Date": date,
            "Ticker": ticker,
            "Total_Mentions": len(group),
            "Consensus_Sentiment": consensus,
            "Subreddits_Appeared": ", ".join(subreddits)
        })

    agg_df = pd.DataFrame(aggregated)
    agg_df = agg_df.sort_values(by=['Date', 'Total_Mentions'], ascending=[False, False])
    
    # Atomic write to prevent file corruption
    temp_file = AGGREGATED_FILE + ".temp"
    agg_df.to_csv(temp_file, index=False)
    os.replace(temp_file, AGGREGATED_FILE)
    
    print(f"Board safely updated: {AGGREGATED_FILE} with {len(agg_df)} unique daily signals.")

if __name__ == "__main__":
    run_engine()