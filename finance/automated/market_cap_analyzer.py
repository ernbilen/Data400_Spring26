import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

def get_dollar_volume(ticker):
    """Calculates the Median Daily Dollar Volume over the last year of trading."""
    try:
        # Pull 1 year of historical price and volume data
        hist = yf.Ticker(ticker).history(period="1y")
        if hist.empty:
            return ticker, 0
            
        # Calculate daily dollar volume (Close Price * Volume)
        hist['Dollar_Volume'] = hist['Close'] * hist['Volume']
        
        # Return the median dollar volume to avoid being skewed by one crazy pump day
        median_dv = hist['Dollar_Volume'].median()
        return ticker, median_dv
    except Exception:
        return ticker, 0

def fix_unknown_sizes(input_csv, output_csv):
    print(f"Loading data from {input_csv}...")
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: {input_csv} not found!")
        return

    # Filter for valid Alpha rows
    df['1W_Alpha(%)'] = pd.to_numeric(df['1W_Alpha(%)'], errors='coerce')
    df = df.dropna(subset=['1W_Alpha(%)'])
    
    unique_tickers = df['Ticker'].dropna().unique()
    print(f"Calculating Historical Dollar Volume for {len(unique_tickers)} tickers...\n")

    # Fetch ADDV concurrently
    dollar_volumes = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {executor.submit(get_dollar_volume, t): t for t in unique_tickers}
        for i, future in enumerate(as_completed(future_to_ticker), 1):
            ticker, dv = future.result()
            dollar_volumes[ticker] = dv
            if i % 50 == 0:
                print(f"  [{i}/{len(unique_tickers)}] Tickers processed...")

    # --- NEW ADDV CATEGORIZATION LOGIC ---
    def categorize_liquidity(dv):
        if pd.isna(dv) or dv == 0:
            return "Dead/Untradable"
        elif dv >= 50_000_000:
            return "Large"   # Highly Liquid (> $50M/day)
        elif dv >= 5_000_000:
            return "Mid"     # Liquid ($5M - $50M/day)
        else:
            return "Small"   # Illiquid (< $5M/day)

    # Map the new liquidity tags
    ticker_to_size = {t: categorize_liquidity(v) for t, v in dollar_volumes.items()}
    df['Market_Cap_Size'] = df['Ticker'].map(ticker_to_size)
    
    # Save the repaired dataset
    df.to_csv(output_csv, index=False)
    
    # --- REPORT GENERATION ---
    print("\n" + "="*50)
    print(" 📊 REVISED LIQUIDITY TIER ANALYSIS (ADDV)")
    print("="*50)
    
    counts = df['Market_Cap_Size'].value_counts()
    total = len(df)
    
    for tier, count in counts.items():
        pct = (count / total) * 100
        print(f"{tier.ljust(20)}: {count} signals ({pct:.1f}%)")
        
    print(f"\n✅ Repaired dataset saved to: {output_csv}")
    print("You can now run 'pure_granular_matrix.py' again using this new CSV!")

if __name__ == "__main__":
    # We take the original results CSV and create a newly repaired one
    fix_unknown_sizes("Spring_2026_Results.csv", "Spring_2026_With_Liquidity.csv")