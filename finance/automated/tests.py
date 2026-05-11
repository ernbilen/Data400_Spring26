import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def run_multi_timeframe_pumper(csv_file, target_subreddit):
    print(f"Loading data from {csv_file}...")
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"CSV not found! Make sure {csv_file} is in the folder.")
        return

    # --- 1. DATA PREP ---
    df['Date'] = pd.to_datetime(df['Date'])
    df['Subreddits_Appeared'] = df['Subreddits_Appeared'].astype(str)
    df = df.sort_values('Date')

    # --- 2. ISOLATE THE COHORT ---
    # We strictly want Positive sentiment, Small ADDV Liquidity, from the target subreddit
    cohort_df = df[
        (df['Consensus_Sentiment'] == 'POSITIVE') & 
        (df['Market_Cap_Size'] == 'Small') &
        (df['Subreddits_Appeared'].str.contains(target_subreddit, case=False))
    ].copy()

    if len(cohort_df) == 0:
        print(f"No trades found for r/{target_subreddit} matching the criteria.")
        return

    # The three timeframes we want to test
    timeframes = {
        '2-Week': '2W_Alpha(%)',
        '3-Week': '3W_Alpha(%)',
        '1-Month': '1M_Alpha(%)'
    }

    # --- 3. BACKTEST PARAMETERS ---
    STARTING_CAPITAL = 10000.00
    POSITION_SIZE = 1000.00       
    FRICTION_COST = 0.05 # 5% standard friction
    
    print("="*65)
    print(f" 🚀 MULTI-TIMEFRAME LONG STRATEGY: r/{target_subreddit.upper()}")
    print(f" Targeting: POSITIVE Sentiment on 'Small' Liquidity Stocks")
    print("="*65 + "\n")

    # Setup the chart
    plt.figure(figsize=(12, 7))
    colors = {'2-Week': '#1f77b4', '3-Week': '#2ca02c', '1-Month': '#d62728'}

    # --- 4. RUN ALL 3 SIMULATIONS ---
# --- 4. RUN ALL 3 SIMULATIONS ---
    for label, column in timeframes.items():
        # FIX: Coerce to numbers FIRST, then drop the resulting NaNs
        temp_df = cohort_df.copy()
        temp_df[column] = pd.to_numeric(temp_df[column], errors='coerce')
        temp_df = temp_df.dropna(subset=[column])
        
        account_balance = STARTING_CAPITAL
        # Initialize charting lists
        dates = [temp_df['Date'].iloc[0] - pd.Timedelta(days=1)] if len(temp_df) > 0 else []
        equity_curve = [STARTING_CAPITAL] if len(temp_df) > 0 else []
        
        winning_trades = 0
        losing_trades = 0

        for index, row in temp_df.iterrows():
            gross_trade_return = row[column] / 100
            net_trade_return = gross_trade_return - FRICTION_COST
            
            dollar_profit = POSITION_SIZE * net_trade_return
            account_balance += dollar_profit
            
            if dollar_profit > 0:
                winning_trades += 1
            else:
                losing_trades += 1
                
            dates.append(row['Date'])
            equity_curve.append(account_balance)

        # Calculate metrics
        total_trades = winning_trades + losing_trades
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        total_return = ((account_balance - STARTING_CAPITAL) / STARTING_CAPITAL) * 100

        # Print to terminal
        print(f"[{label} HOLDING PERIOD]")
        print(f"  Total Trades : {total_trades}")
        print(f"  Win Rate     : {win_rate:.1f}%")
        print(f"  Final Balance: ${account_balance:,.2f}")
        print(f"  Total Return : {total_return:+.2f}%\n")

        # Add to plot
        if total_trades > 0:
            plt.plot(dates, equity_curve, color=colors[label], linewidth=2, label=f'{label} Hold ({total_return:+.1f}%)')

    # --- 5. FINALIZE CHART ---
    plt.axhline(STARTING_CAPITAL, color='black', linestyle='--', label='Starting Capital ($10k)')
    plt.title(f'Simulated Equity Curve: r/{target_subreddit} Small-Cap Lifecycle', fontsize=14)
    plt.ylabel('Account Balance ($)', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate() 
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    chart_name = f'{target_subreddit}_Multi_Timeframe_Curve.png'
    plt.savefig(chart_name)
    print(f"-> Generated combined backtest chart: {chart_name}")

if __name__ == "__main__":
    # Pointing this to our newest, most accurate liquidity dataset
    run_multi_timeframe_pumper("Historical_Alpha_With_Liquidity.csv", "stocks_picks")