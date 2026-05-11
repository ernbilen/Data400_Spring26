import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def run_long_backtest(csv_file):
    print(f"Loading data from {csv_file}...")
    
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("CSV not found!")
        return

    # --- 1. DATA CLEANING ---
    df['Date'] = pd.to_datetime(df['Date'])
    df['1W_Alpha(%)'] = pd.to_numeric(df['1W_Alpha(%)'], errors='coerce')
    df = df.dropna(subset=['1W_Alpha(%)'])
    df = df.sort_values('Date')
    
    print(f"Total Unique Daily Trading Signals: {len(df)}\n")

    # --- 2. BACKTEST PARAMETERS ---
    STARTING_CAPITAL = 10000.00
    POSITION_SIZE = 1000.00       
    
    # Going LONG is much cheaper than shorting. 
    # 0.5% covers bid/ask spread and standard execution slippage.
    FRICTION_COST = 0.005         
    
    account_balance = STARTING_CAPITAL
    dates = [df['Date'].iloc[0] - pd.Timedelta(days=1)] 
    equity_curve = [STARTING_CAPITAL]
    
    winning_trades = 0
    losing_trades = 0

    print("="*50)
    print(" 🚀 RUNNING 'LONG CONTAGION' STRATEGY")
    print("="*50)
    print(f"Starting Capital: ${STARTING_CAPITAL:,.2f}")
    print(f"Position Size:    ${POSITION_SIZE:,.2f} per trade")
    print(f"Friction Penalty: {FRICTION_COST*100}% per trade\n")

    # --- 3. TRADE SIMULATOR ---
    for index, row in df.iterrows():
        
        # Check if the signal appeared in multiple subreddits
        multi_sub = "," in str(row.get('Subreddits_Appeared', ''))
        
        # THE STRATEGY RULE: 
        # Must be explicitly POSITIVE AND (Highly Mentioned OR Multi-Subreddit)
        if row['Consensus_Sentiment'] == 'POSITIVE' and (row['Total_Mentions'] > 1 or multi_sub):
            
            # Since we are going LONG, we capture the exact Alpha directly.
            # E.g., If Alpha is +5%, our position gains 5%.
            gross_trade_return = row['1W_Alpha(%)'] / 100
            
            # Subtract execution slippage
            net_trade_return = gross_trade_return - FRICTION_COST
            
            dollar_profit = POSITION_SIZE * net_trade_return
            account_balance += dollar_profit
            
            if dollar_profit > 0:
                winning_trades += 1
            else:
                losing_trades += 1
                
            dates.append(row['Date'])
            equity_curve.append(account_balance)

    # --- 4. RESULTS & VISUALIZATION ---
    total_trades = winning_trades + losing_trades
    if total_trades == 0:
        print("No trades triggered your strategy criteria.")
        return

    win_rate = (winning_trades / total_trades) * 100
    total_return = ((account_balance - STARTING_CAPITAL) / STARTING_CAPITAL) * 100

    print(f"Total Trades Executed: {total_trades}")
    print(f"Win Rate:              {win_rate:.1f}%")
    print(f"Final Balance:         ${account_balance:,.2f}")
    print(f"Total Return:          {total_return:+.2f}%\n")

    # Generate Chart
    plt.figure(figsize=(10, 6))
    plt.plot(dates, equity_curve, color='green', linewidth=2, label='Portfolio Value')
    plt.axhline(STARTING_CAPITAL, color='black', linestyle='--', label='Starting Capital ($10k)')
    
    plt.title('Simulated Equity Curve: Long Contagion Strategy', fontsize=14)
    plt.ylabel('Account Balance ($)', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gcf().autofmt_xdate() 
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    chart_name = 'Long_Contagion_Equity_Curve.png'
    plt.savefig(chart_name)
    print(f"-> Generated backtest chart: {chart_name}")

if __name__ == "__main__":
    target_csv = "Mega_Reddit_Alpha_Dataset.csv" 
    run_long_backtest(target_csv)