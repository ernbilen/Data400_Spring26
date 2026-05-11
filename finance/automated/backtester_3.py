import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def run_short_backtest(csv_file):
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

    # --- 2. BACKTEST PARAMETERS ---
    STARTING_CAPITAL = 10000.00
    POSITION_SIZE = 1000.00       
    
    # 0.5% friction is MANDATORY here. 
    # Shorting incurs the bid-ask spread PLUS a "Hard-to-Borrow" fee from the broker.
    FRICTION_COST = 0.005         
    
    account_balance = STARTING_CAPITAL
    dates = [df['Date'].iloc[0] - pd.Timedelta(days=1)] 
    equity_curve = [STARTING_CAPITAL]
    
    winning_trades = 0
    losing_trades = 0

    print("="*50)
    print(" 💀 RUNNING 'DOOM-SEEKER' SHORT STRATEGY")
    print("="*50)
    print(f"Holding Period:   1 Week (Short Position)")
    print(f"Position Size:    ${POSITION_SIZE:,.2f} per trade")
    print(f"Friction Penalty: {FRICTION_COST*100}% per trade\n")

    # --- 3. TRADE SIMULATOR ---
    for index, row in df.iterrows():
        
        # STRATEGY RULE: 
        # Exclusively target stocks the LLM flagged as NEGATIVE.
        if row['Consensus_Sentiment'] == 'NEGATIVE':
            
            # INVERT THE ALPHA: We are shorting. 
            # If the stock drops 5% (-0.05), we make +5% (+0.05).
            gross_trade_return = (row['1W_Alpha(%)'] / 100) * -1
            
            # Subtract execution slippage and borrow fees
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
    plt.plot(dates, equity_curve, color='#d62728', linewidth=2, label='Short-Seller Portfolio')
    plt.axhline(STARTING_CAPITAL, color='black', linestyle='--', label='Starting Capital')
    
    plt.title('Simulated Equity Curve: Doom-Seeker Short Strategy', fontsize=14)
    plt.ylabel('Account Balance ($)', fontsize=12)
    plt.xlabel('Date', fontsize=12)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate() 
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    chart_name = 'Doom_Seeker_Equity_Curve.png'
    plt.savefig(chart_name)
    print(f"-> Generated backtest chart: {chart_name}")

if __name__ == "__main__":
    target_csv = " Historical_Alpha_With_Liquidity.csv" 
    run_short_backtest(target_csv)