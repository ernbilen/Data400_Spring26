# Seeking Alpha: Optimal Asset Allocation & Alternative Data

**Authors:** Thanh Vu & Noah Lape  
**Course:** DATA 400  

## Overview
This project explores two primary quantitative methods for generating Alpha (excess market return):
1. **Macroeconomic Regime-Aware Allocation:** Adjusting portfolio weights based on four distinct economic environments over a 50-year backtest (1976–2025).
2. **Alternative Data via Retail Sentiment:** Using a locally hosted Large Language Model (LLM) to systematically extract structured financial signals from unstructured trading forums to front-run retail momentum.

## Data Sources & Technologies
* **Traditional Financial Data:** S&P 500, U.S. Treasury yields (2yr/10yr), Gold (GLD), House Price Index (HPI), CPI, and INDPRO via Federal Reserve Economic Data (FRED), Investing.com, and Macrotrend.
* **Alternative Data Extraction:** Custom asynchronous Python scraper utilized to pull raw JSON data from niche Reddit trading communities (r/ValueInvesting, r/pennystocks, r/stock-picks), featuring rolling-rate-limit evasion.
* **Sentiment Analysis:** Locally hosted 14-Billion parameter LLM (Qwen 2.5) deployed to classify complex financial slang that traditional NLP tools (like VADER or finBERT) fail to categorize.
* **Financial Grounding:** `yfinance` API for historical pricing and market-relative Alpha benchmarking against the SPY.

## Methodology & Pipeline Architecture
### Phase 1: Macro Regime Backtest
* Evaluated an equal-weighted benchmark portfolio against a regime-aware portfolio.
* Categorized the market into four macro environments: Expansion, Stagflation, Deflationary Bust, and Goldilocks.

### Phase 2: Addressing Statistical Biases & Execution Friction
* **Look-Ahead Bias:** Enforced strictly chronological scraping by "New" rather than "Top" to prevent sorting by future outcomes.
* **Survivorship Bias:** Engineered a "Lock-Box" memory system to account for total portfolio losses from delisted or bankrupt companies that standard APIs purge.
* **Liquidity Taxes:** Utilized Average Daily Dollar Volume (ADDV) to filter assets into liquidity tiers, proving that massive theoretical returns in Micro-Caps are structurally un-extractable due to extreme execution friction, wide bid-ask spreads, and exorbitant borrow fees.

## Key Findings
* **Regime-Aware Portfolio Outperformance:** Over 50 years, the regime-aware strategy produced 2x the terminal wealth of the equal-weight benchmark ($65,784 vs. $32,802) with a higher CAGR (8.74% vs. 7.23%) and a significantly reduced max drawdown (-4.11%).
* **The "Slow-Burn" Long:** Identified a highly scalable, institutional-grade strategy by isolating positive sentiment in large-cap stocks on r/ValueInvesting, generating a linear +2.75% net Alpha per trade over a 1-month horizon.
* **The Exit-Liquidity Scam:** Mathematical proof that highly concentrated "positive" signals on r/pennystocks act as coordinated pump-and-dumps, yielding -3.68% negative Alpha over a 1-month period as early entrants manufacture exit liquidity.

## Future Work
* Transitioning from historical backfilling to a daily, chronological scrape job executed via Windows Task Scheduler.
* Connecting the Alpha pipeline to the **Alpaca Trading API** to deploy a live paper-trading bot for real-time forward testing and execution slippage measurement.

---
*Disclaimer: This project and analysis serve strictly as an academic reference framework. We are not registered investment advisors. Nothing in this repository constitutes a buy, sell, or hold recommendation.*
