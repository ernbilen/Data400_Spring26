import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time
import os
import warnings

# Suppress messy pandas/yfinance warnings in the terminal
warnings.filterwarnings('ignore')

def calculate_historical_alphas(input_csv, output_csv="Historical_Alpha_Results.csv", benchmark="SPY"):
    print(f"Loading live signals from {input_csv}...")
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: {input_csv} not found. Run your live bot first!")
        return

    # Map our timeframes to the approximate number of trading days
    intervals = {"1D": 1, "1W": 5, "2W": 10, "3W": 15, "1M": 21}
    
    # 1. Initialize all Alpha columns as 'Pending'
    for label in intervals.keys():
        df[f'{label}_Alpha(%)'] = "Pending"

    # 2. THE LOCK-BOX: Load existing historical data if it exists
    if os.path.exists(output_csv):
        print(f"Found existing {output_csv}. Engaging Lock-Box to protect past data...")
        history_df = pd.read_csv(output_csv)
        
        # Create a lookup dictionary: Key = "Ticker_YYYY-MM-DD"
        history_dict = {}
        for _, h_row in history_df.iterrows():
            date_str = str(h_row['Date']).split(' ')[0]
            key = f"{h_row['Ticker']}_{date_str}"
            history_dict[key] = h_row

        # Apply securely locked data to our current dataframe
        for index, row in df.iterrows():
            date_str = str(row['Date']).split(' ')[0]
            key = f"{row['Ticker']}_{date_str}"
            
            if key in history_dict:
                for label in intervals.keys():
                    col_name = f'{label}_Alpha(%)'
                    if col_name in history_dict[key]:
                        old_val = history_dict[key][col_name]
                        # If the old value is a real number or a confirmed Delisting, lock it in!
                        if pd.notna(old_val) and old_val not in ["Pending", "N/A", "nan"]:
                            df.at[index, col_name] = old_val

    yf_cache = {}
    processed_count = 0
    today = datetime.now()

    print(f"\nScanning {len(df)} signals for missing/pending Alpha calculations...")

    for index, row in df.iterrows():
        ticker = row['Ticker']
        post_date_str = str(row['Date']).split(' ')[0] 
        start_date = datetime.strptime(post_date_str, '%Y-%m-%d')
        
        # Determine which specific timeframes still need to be calculated
        missing_intervals = {}
        for label, trading_days in intervals.items():
            current_val = str(df.at[index, f'{label}_Alpha(%)'])
            if current_val in ["Pending", "N/A", "nan"]:
                missing_intervals[label] = trading_days

        # SMART BYPASS: If everything is locked in, skip Yahoo Finance entirely
        if not missing_intervals:
            processed_count += 1
            continue

        cache_key = f"{ticker}_{post_date_str}"

        # 3. Fetch data from Yahoo Finance ONLY for missing intervals
        if cache_key not in yf_cache:
            try:
                # Cap the fetch window at 45 days, or today (whichever is sooner)
                end_date = start_date + timedelta(days=45)
                if end_date > today + timedelta(days=1):
                    end_date = today + timedelta(days=1)

                data = yf.download(
                    [ticker, benchmark],
                    start=start_date.strftime('%Y-%m-%d'),
                    end=end_date.strftime('%Y-%m-%d'),
                    progress=False
                )['Close']

                if not data.empty and ticker in data.columns and benchmark in data.columns:
                    data = data.dropna()
                    yf_cache[cache_key] = data
                else:
                    yf_cache[cache_key] = None
            except Exception:
                yf_cache[cache_key] = None
            
            time.sleep(0.1) # Be polite to the API

        # 4. Calculate Alpha & Detect Bankruptcies
        price_data = yf_cache[cache_key]

        for label, trading_days in missing_intervals.items():
            calendar_days_passed = (today - start_date).days
            expected_calendar_days = trading_days * 1.5 + 2 # Convert trading days to real-world days

            if price_data is not None and not price_data.empty:
                if len(price_data) > trading_days:
                    # SUCCESS: We have the data, calculate and lock in the Alpha
                    p0_stock = price_data[ticker].iloc[0]
                    p0_bench = price_data[benchmark].iloc[0]

                    pT_stock = price_data[ticker].iloc[trading_days]
                    pT_bench = price_data[benchmark].iloc[trading_days]

                    stock_return = (pT_stock - p0_stock) / p0_stock
                    bench_return = (pT_bench - p0_bench) / p0_bench

                    alpha = (stock_return - bench_return) * 100
                    df.at[index, f'{label}_Alpha(%)'] = round(alpha, 2)
                else:
                    # Partial Data: It survived the post, but did it survive the interval?
                    if calendar_days_passed > expected_calendar_days + 7:
                        # Time passed, but YF stopped tracking it = Bankruptcy/Delisting
                        df.at[index, f'{label}_Alpha(%)'] = "N/A (Delisted)"
                    else:
                        # Time simply hasn't passed yet. Wait for tomorrow.
                        df.at[index, f'{label}_Alpha(%)'] = "Pending"
            else:
                # NO Data: AI Hallucination or instant delisting
                if calendar_days_passed > 5:
                    df.at[index, f'{label}_Alpha(%)'] = "N/A (Invalid/Delisted)"
                else:
                    df.at[index, f'{label}_Alpha(%)'] = "Pending"

        processed_count += 1
        if processed_count % 50 == 0:
            print(f"Processed {processed_count}/{len(df)} signals...")

    # 5. Save the perfectly preserved and updated dataset
    df.to_csv(output_csv, index=False)
    print(f"\nSUCCESS! Alpha calculations protected and updated in {output_csv}")

if __name__ == "__main__":
    calculate_historical_alphas("Live_Daily_Signals.csv")