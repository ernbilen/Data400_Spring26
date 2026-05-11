import pandas as pd

def print_liquidity_matrix(input_csv):
    print(f"Loading liquidity data from {input_csv}...")
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: {input_csv} not found! Make sure you ran the liquidity proxy script.")
        return

    # --- 1. FILTERING OUT CROSSOVERS ---
    # Ensure it's read as a string, then keep ONLY rows WITHOUT a comma
    df['Subreddits_Appeared'] = df['Subreddits_Appeared'].astype(str)
    pure_df = df[~df['Subreddits_Appeared'].str.contains(',')]

    alpha_cols = ['1D_Alpha(%)', '1W_Alpha(%)', '2W_Alpha(%)', '3W_Alpha(%)', '1M_Alpha(%)']
    
    # Ensure alpha columns are numeric
    for col in alpha_cols:
        pure_df[col] = pd.to_numeric(pure_df[col], errors='coerce')

    print("Dropped multi-subreddit crossovers. Grouping pure signals by ADDV Liquidity...\n")
    
    # --- 2. GROUPING & AGGREGATING ---
    grouped = pure_df.groupby(['Subreddits_Appeared', 'Market_Cap_Size', 'Consensus_Sentiment'])
    
    matrix = grouped[alpha_cols].mean().round(2)
    matrix['Signal_Count'] = grouped.size()
    
    matrix = matrix.reset_index()
    
    # Drop empty groupings (just in case a subreddit has 0 dead stocks)
    matrix = matrix[matrix['Signal_Count'] > 0]
    
    # Reorder columns
    cols = ['Subreddits_Appeared', 'Market_Cap_Size', 'Consensus_Sentiment', 'Signal_Count'] + alpha_cols
    matrix = matrix[cols]
    
    # --- 3. SORTING FOR READABILITY ---
    # Updated to reflect our new ADDV Liquidity Tiers
    size_order = ['Large', 'Mid', 'Small', 'Dead/Untradable']
    sentiment_order = ['POSITIVE', 'NEUTRAL', 'NEGATIVE']
    
    matrix['Market_Cap_Size'] = pd.Categorical(matrix['Market_Cap_Size'], categories=size_order, ordered=True)
    matrix['Consensus_Sentiment'] = pd.Categorical(matrix['Consensus_Sentiment'], categories=sentiment_order, ordered=True)
    
    # Sort first by subreddit, then size, then sentiment
    matrix = matrix.sort_values(by=['Subreddits_Appeared', 'Market_Cap_Size', 'Consensus_Sentiment'])
    
    # --- 4. TERMINAL PRINT ---
    print("="*115)
    print(" 🎯 PURE ALPHA MATRIX: SINGLE SUBREDDIT SIGNALS BY LIQUIDITY")
    print("="*115)
    print(matrix.to_string(index=False))
    print("="*115)

if __name__ == "__main__":
    print_liquidity_matrix("Spring_2026_With_Liquidity.csv")