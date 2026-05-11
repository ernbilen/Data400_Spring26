import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import warnings

# Suppress annoying yfinance timezone warnings for clean terminal output
warnings.filterwarnings('ignore')

def get_performance_alpha(ticker, post_date_str, benchmark="SPY"):
    """
    Calculates 1-day, 1-week, and 1-month performance of a stock vs a benchmark.
    """
    # 1. Setup our time window
    start_date = datetime.strptime(post_date_str, '%Y-%m-%d')
    # Grab 45 calendar days to ensure we get at least 21 trading days (1 month)
    end_date = start_date + timedelta(days=45) 

    # 2. Download the data for both the stock and the benchmark
    try:
        # progress=False stops yfinance from printing a loading bar for every single ticker
        data = yf.download([ticker, benchmark], 
                           start=start_date.strftime('%Y-%m-%d'), 
                           end=end_date.strftime('%Y-%m-%d'), 
                           progress=False)['Close']
    except Exception as e:
        print(f"Failed to download data for {ticker}: {e}")
        return None

    # Handle cases where the ticker is invalid or delisted
    if data.empty or ticker not in data.columns:
        print(f"No valid pricing data found for {ticker}.")
        return None

    # Drop missing values in case one asset halted trading
    data = data.dropna()
    
    # 3. Define our Trading Day indices
    intervals = {
        "1_Day": 1,
        "1_Week": 5,
        "1_Month": 21
    }
    
    results = {
        "Ticker": ticker,
        "Post_Date": start_date.strftime('%Y-%m-%d'),
        "Start_Price": round(data[ticker].iloc[0], 2) if not data.empty else None
    }

    # 4. Calculate Alpha for each timeframe
    for label, trading_days in intervals.items():
        # Check if enough time has passed to calculate this interval
        if len(data) > trading_days:
            # Baseline prices (Day 0)
            p0_stock = data[ticker].iloc[0]
            p0_bench = data[benchmark].iloc[0]
            
            # Future prices
            pT_stock = data[ticker].iloc[trading_days]
            pT_bench = data[benchmark].iloc[trading_days]
            
            # Absolute Returns
            stock_return = (pT_stock - p0_stock) / p0_stock
            bench_return = (pT_bench - p0_bench) / p0_bench
            
            # Relative Return (Alpha)
            alpha = stock_return - bench_return
            
            results[f"{label}_Stock_Return"] = round(stock_return * 100, 2)
            results[f"{label}_Bench_Return"] = round(bench_return * 100, 2)
            results[f"{label}_Alpha"] = round(alpha * 100, 2)
        else:
            # If the post was made too recently, we won't have 1-month forward data yet
            results[f"{label}_Stock_Return"] = "N/A"
            results[f"{label}_Bench_Return"] = "N/A"
            results[f"{label}_Alpha"] = "N/A"
            
    return results

# --- Main Execution / Test ---
if __name__ == "__main__":
    # Let's test a historical hypothetical: 
    # Someone posted about Palantir ($PLTR) on Jan 15th, 2023.
    # The whole market was choppy, so let's see how PLTR did vs SPY.
    
    test_ticker = "PLTR"
    test_date = "2023-01-15" 
    
    print(f"Fetching Alpha Data for {test_ticker} posted on {test_date}...\n")
    performance = get_performance_alpha(test_ticker, test_date)
    
    if performance:
        print(f"--- Results for {performance['Ticker']} ---")
        print(f"Starting Price on Day 0: ${performance['Start_Price']}")
        print(f"1-Day Alpha:   {performance.get('1_Day_Alpha')}%")
        print(f"1-Week Alpha:  {performance.get('1_Week_Alpha')}%")
        print(f"1-Month Alpha: {performance.get('1_Month_Alpha')}%")
        print("\nFull Data Payload:")
        for key, value in performance.items():
            print(f"  {key}: {value}")