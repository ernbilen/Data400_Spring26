import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_market_cap(ticker):
    """Pings Yahoo Finance for the market cap of a single ticker."""
    try:
        info = yf.Ticker(ticker).info
        return ticker, info.get('marketCap', 0)
    except Exception:
        return ticker, 0

def analyze_by_size(input_csv, output_csv):
    print(f"Loading data from {input_csv}...")
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: {input_csv} not found!")
        return

    # --- 1. DATA CLEANING ---
    # Drop rows where 1W_Alpha is missing (delisted, hallucinated, or foreign)
    df['1W_Alpha(%)'] = pd.to_numeric(df['1W_Alpha(%)'], errors='coerce')
    initial_len = len(df)
    df = df.dropna(subset=['1W_Alpha(%)'])
    print(f"Dropped {initial_len - len(df)} rows with invalid or missing Alpha data.")
    
    unique_tickers = df['Ticker'].dropna().unique()
    print(f"Fetching Market Caps for {len(unique_tickers)} valid unique tickers...\n")

    # --- 2. MARKET CAP FETCHING ---
    market_caps = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {executor.submit(get_market_cap, t): t for t in unique_tickers}
        for i, future in enumerate(as_completed(future_to_ticker), 1):
            ticker, cap = future.result()
            market_caps[ticker] = cap
            if i % 50 == 0:
                print(f"  [{i}/{len(unique_tickers)}] Tickers processed...")

    # --- 3. CATEGORIZATION ---
    def categorize_cap(cap):
        if cap is None or cap == 0:
            return "Unknown"
        elif cap >= 10_000_000_000:
            return "Large"
        elif cap >= 300_000_000:
            return "Mid"
        else:
            return "Small"

    ticker_to_size = {t: categorize_cap(c) for t, c in market_caps.items()}
    
    # Map the new size tags back to the main dataframe
    df['Market_Cap_Size'] = df['Ticker'].map(ticker_to_size)
    
    # Save the enriched dataset to a new CSV
    df.to_csv(output_csv, index=False)
    print(f"\n✅ Saved enriched dataset with Size Tags to: {output_csv}")

    # --- 4. COHORT BACKTESTING ---
    print("\n" + "="*50)
    print(" 📉 'DOOM-SEEKER' SHORT STRATEGY BY COMPANY SIZE")
    print("="*50)

    STARTING_CAPITAL = 10000.00
    POSITION_SIZE = 1000.00
    FRICTION_COST = 0.005 # 0.5% standard friction

    # Filter strictly for the NEGATIVE sentiment short strategy
    short_df = df[df['Consensus_Sentiment'] == 'NEGATIVE'].copy()

    # Test each size cohort individually
    for size in ['Large', 'Mid', 'Small', 'Unknown']:
        size_df = short_df[short_df['Market_Cap_Size'] == size]
        if len(size_df) == 0:
            continue
            
        account_balance = STARTING_CAPITAL
        winning_trades = 0
        losing_trades = 0
        
        for index, row in size_df.iterrows():
            # INVERT THE ALPHA: We are shorting
            gross_trade_return = (row['1W_Alpha(%)'] / 100) * -1
            
            # Subtract execution slippage
            net_trade_return = gross_trade_return - FRICTION_COST
            
            dollar_profit = POSITION_SIZE * net_trade_return
            account_balance += dollar_profit
            
            if dollar_profit > 0:
                winning_trades += 1
            else:
                losing_trades += 1
                
        total_trades = winning_trades + losing_trades
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        total_return = ((account_balance - STARTING_CAPITAL) / STARTING_CAPITAL) * 100

        print(f"[{size.upper()} CAP COMPANIES]")
        print(f"  Total Trades : {total_trades}")
        print(f"  Win Rate     : {win_rate:.1f}%")
        print(f"  Final Balance: ${account_balance:,.2f}")
        print(f"  Total Return : {total_return:+.2f}%\n")

if __name__ == "__main__":
    analyze_by_size("Historical_Alpha_Results.csv", "Historical_Alpha_With_Size.csv")