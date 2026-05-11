import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

def analyze_and_backtest(csv_file):
    print(f"Loading live signals from {csv_file}...")
    
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("CSV not found. Make sure you ran alpha_calculator.py first!")
        return

    # --- 1. DATA PREPARATION ---
    alpha_cols = ['1D_Alpha(%)', '1W_Alpha(%)', '2W_Alpha(%)', '3W_Alpha(%)', '1M_Alpha(%)']
    for col in alpha_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Date'] = pd.to_datetime(df['Date'])
    # Drop rows that haven't even had 1 day of trading yet
    df = df.dropna(subset=['1D_Alpha(%)'])
    df = df.sort_values('Date')
    
    print(f"Analyzing {len(df)} valid trading signals...\n")
    
    # --- PART 1: THE QUANT REPORT ---
    print("="*50)
    print(" 📈 LIVE DATA QUANTITATIVE REPORT")
    print("="*50)

    # Metric 1: Baseline Performance across Time
    print("\n[1] OVERALL ALPHA TRAJECTORY (The Hype Lifecycle)")
    overall_means = []
    for col in alpha_cols:
        valid_data = df[col].dropna()
        if not valid_data.empty:
            avg_alpha = valid_data.mean()
            win_rate = (valid_data > 0).mean() * 100
            overall_means.append(avg_alpha)
            print(f"  {col[:2]}: Avg Alpha = {avg_alpha:+.2f}% | Win Rate = {win_rate:.1f}%")

    # Metric 2: Cross-Subreddit Contagion Power (Using 1-Week Alpha)
    print("\n[2] CROSS-SUBREDDIT CONTAGION (1-Week Holding Period)")
    if 'Subreddits_Appeared' in df.columns and not df['1W_Alpha(%)'].dropna().empty:
        df['Multi_Sub'] = df['Subreddits_Appeared'].apply(lambda x: "Multi-Subreddit" if "," in str(x) else "Single Subreddit")
        contagion_group = df.groupby('Multi_Sub')['1W_Alpha(%)'].agg(['mean', 'count'])
        for status, row in contagion_group.iterrows():
            print(f"  {status} ({int(row['count'])} signals): Avg 1W Alpha = {row['mean']:+.2f}%")

    # Metric 3: Consensus Sentiment
    print("\n[3] LLM SENTIMENT POWER (1-Week Holding Period)")
    if not df['1W_Alpha(%)'].dropna().empty:
        sentiment_group = df.groupby('Consensus_Sentiment')['1W_Alpha(%)'].agg(['mean', 'count'])
        for sentiment, row in sentiment_group.iterrows():
            print(f"  {sentiment} ({int(row['count'])} signals): Avg 1W Alpha = {row['mean']:+.2f}%")

    # --- VISUALIZATION 1: The Alpha Decay Curve ---
    # We plot the trajectory of POSITIVE sentiment stocks over the month
    plt.figure(figsize=(9, 5))
    
    # Filter for only Positive signals
    pos_df = df[df['Consensus_Sentiment'] == 'POSITIVE']
    pos_means = [pos_df[col].mean() for col in alpha_cols]
    
    x_labels = ['1 Day', '1 Week', '2 Weeks', '3 Weeks', '1 Month']
    
    plt.plot(x_labels, overall_means, marker='o', linestyle='--', color='gray', label='All Reddit Stocks (Baseline)')
    plt.plot(x_labels, pos_means, marker='s', linewidth=3, color='green', label='LLM "POSITIVE" Stocks')
    
    plt.axhline(0, color='black', linestyle='-')
    plt.title('The Reddit Lifecycle: Alpha Trajectory over 1 Month', fontsize=14)
    plt.ylabel('Average Market-Relative Alpha (%)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    decay_chart = 'Alpha_Decay_Curve.png'
    plt.savefig(decay_chart)
    print(f"\n  -> Saved Chart: {decay_chart}")

    # --- PART 2: THE BACKTESTER ---
    print("\n" + "="*50)
    print(" 🚀 RUNNING 'LONG CONTAGION' TRADING SIMULATOR")
    print("="*50)
    
    STARTING_CAPITAL = 10000.00
    POSITION_SIZE = 1000.00       
    FRICTION_COST = 0.005 # 0.5% Slippage for long execution
    
    account_balance = STARTING_CAPITAL
    dates = [df['Date'].iloc[0] - pd.Timedelta(days=1)] 
    equity_curve = [STARTING_CAPITAL]
    
    winning_trades = 0
    losing_trades = 0

    print(f"Holding Period:   1 Week")
    print(f"Starting Capital: ${STARTING_CAPITAL:,.2f}")
    print(f"Position Size:    ${POSITION_SIZE:,.2f} per trade")
    print(f"Friction Penalty: {FRICTION_COST*100}% per trade\n")

    # Trade Simulator Loop
    for index, row in df.dropna(subset=['1W_Alpha(%)']).iterrows():
        
        # STRATEGY LOGIC: Buy if LLM says POSITIVE, and it has viral momentum
        if row['Consensus_Sentiment'] == 'POSITIVE' and (row['Total_Mentions'] > 1 or row['Multi_Sub'] == 'Multi-Subreddit'):
            
            gross_trade_return = row['1W_Alpha(%)'] / 100
            net_trade_return = gross_trade_return - FRICTION_COST
            
            dollar_profit = POSITION_SIZE * net_trade_return
            account_balance += dollar_profit
            
            if dollar_profit > 0:
                winning_trades += 1
            else:
                losing_trades += 1
                
            dates.append(row['Date'])
            equity_curve.append(account_balance)

    # Backtest Results
    total_trades = winning_trades + losing_trades
    if total_trades > 0:
        win_rate = (winning_trades / total_trades) * 100
        total_return = ((account_balance - STARTING_CAPITAL) / STARTING_CAPITAL) * 100

        print(f"Total Trades Executed: {total_trades}")
        print(f"Win Rate:              {win_rate:.1f}%")
        print(f"Final Balance:         ${account_balance:,.2f}")
        print(f"Total Return:          {total_return:+.2f}%\n")

        # --- VISUALIZATION 2: The Equity Curve ---
        plt.figure(figsize=(10, 6))
        plt.plot(dates, equity_curve, color='green', linewidth=2, label='Portfolio Value')
        plt.axhline(STARTING_CAPITAL, color='black', linestyle='--', label='Starting Capital ($10k)')
        
        plt.title('Live Forward-Tested Equity Curve: Long Contagion Strategy', fontsize=14)
        plt.ylabel('Account Balance ($)', fontsize=12)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gcf().autofmt_xdate() 
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        eq_chart = 'Live_Backtest_Equity_Curve.png'
        plt.savefig(eq_chart)
        print(f"  -> Saved Chart: {eq_chart}")
    else:
        print("No trades triggered the strategy criteria in this dataset.")

# --- EXECUTE ---
if __name__ == "__main__":
    target_csv = "Historical_Alpha_Results.csv" 
    analyze_and_backtest(target_csv)