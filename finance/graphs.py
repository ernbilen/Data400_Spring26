import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

def analyze_reddit_alpha(csv_file):
    print(f"Loading data from {csv_file}...")
    
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("CSV not found. Make sure the scraper has finished running!")
        return

    alpha_cols = ['1D_Alpha(%)', '1W_Alpha(%)', '1M_Alpha(%)']
    for col in alpha_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=alpha_cols, how='all')
    print(f"Analyzing {len(df)} valid daily signals...\n")
    print("="*50)
    print(" 📈 MEGA-PIPELINE QUANT REPORT")
    print("="*50)

    # --- METRIC 1: Overall Averages & Win Rates ---
    print("\n[1] OVERALL BASELINE PERFORMANCE")
    for col in alpha_cols:
        valid_data = df[col].dropna()
        if not valid_data.empty:
            avg_alpha = valid_data.mean()
            win_rate = (valid_data > 0).mean() * 100
            print(f"  {col}: Avg Alpha = {avg_alpha:+.2f}% | Win Rate = {win_rate:.1f}%")

    # --- METRIC 2: Consensus Sentiment Predictive Accuracy ---
    print("\n[2] CONSENSUS SENTIMENT POWER (1-Week Alpha)")
    if not df['1W_Alpha(%)'].dropna().empty:
        sentiment_group = df.groupby('Consensus_Sentiment')['1W_Alpha(%)'].agg(['mean', 'count'])
        for sentiment, row in sentiment_group.iterrows():
            print(f"  {sentiment} ({int(row['count'])} signals): Avg 1W Alpha = {row['mean']:+.2f}%")
            
        plt.figure(figsize=(8, 5))
        sns.barplot(data=df, x='Consensus_Sentiment', y='1W_Alpha(%)', palette='coolwarm', order=['NEGATIVE', 'NEUTRAL', 'POSITIVE'])
        plt.title('Average 1-Week Alpha by Consensus Sentiment')
        plt.axhline(0, color='black', linestyle='--')
        plt.savefig('Consensus_Sentiment_vs_Alpha.png')
        print("  -> Saved chart: Consensus_Sentiment_vs_Alpha.png")

    # --- METRIC 3: The Virality Effect (Total Mentions) ---
    print("\n[3] THE VIRALITY EFFECT (Total Mentions vs. Performance)")
    if 'Total_Mentions' in df.columns and not df['1W_Alpha(%)'].dropna().empty:
        median_mentions = df['Total_Mentions'].median()
        df['Hype_Level'] = np.where(df['Total_Mentions'] > median_mentions, 'High Hype', 'Low Hype')
        
        hype_group = df.groupby('Hype_Level')['1W_Alpha(%)'].mean()
        for hype, mean_alpha in hype_group.items():
            print(f"  {hype} (> {median_mentions} mentions): Avg 1W Alpha = {mean_alpha:+.2f}%")

    # --- METRIC 4: Cross-Subreddit Contagion ---
    print("\n[4] CROSS-SUBREDDIT CONTAGION")
    if 'Subreddits_Appeared' in df.columns and not df['1W_Alpha(%)'].dropna().empty:
        # If there's a comma, it appeared in multiple subreddits
        df['Multi_Sub'] = df['Subreddits_Appeared'].apply(lambda x: "Multi-Subreddit" if "," in str(x) else "Single Subreddit")
        contagion_group = df.groupby('Multi_Sub')['1W_Alpha(%)'].agg(['mean', 'count'])
        for status, row in contagion_group.iterrows():
            print(f"  {status} ({int(row['count'])} signals): Avg 1W Alpha = {row['mean']:+.2f}%")

    # --- METRIC 5: Correlation Matrix ---
    print("\n[5] CORRELATIONS")
    print("  (Values near 1.0 = strong positive link, near -1.0 = strong negative link)")
    corr_cols = ['Total_Upvotes', 'Total_Mentions', '1W_Alpha(%)']
    corr_cols = [c for c in corr_cols if c in df.columns] 
    if len(corr_cols) > 1:
        corr_matrix = df[corr_cols].corr()
        print(f"  Correlation between Upvotes and 1W Alpha:  {corr_matrix.loc['Total_Upvotes', '1W_Alpha(%)']:+.3f}")
        print(f"  Correlation between Mentions and 1W Alpha: {corr_matrix.loc['Total_Mentions', '1W_Alpha(%)']:+.3f}")

    print("\n==================================================")
    print("Analysis Complete. Check your folder for generated charts!")

if __name__ == "__main__":
    target_csv = "Mega_Reddit_Alpha_Dataset.csv" 
    analyze_reddit_alpha(target_csv)