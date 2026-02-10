Draft Proposal
For my capstone project, I will analyze publicly available economic and insurance industry data to explore how life insurance and annuity activity relates to macroeconomic conditions such as interest rates, inflation, and market volatility. I will use Federal Reserve Economic Data (FRED) as the primary source of longitudinal time-series data, focusing specifically on series tagged under life insurance and related financial accounts. The data are real, time-aligned, and suitable for quantitative analysis with methods like regression and trend modeling.
Data Sources
I will use the following FRED series as part of my dataset:
Industry-Level Life Insurance and Annuity Economic Series
Life Insurance Total Financial Assets, Level (Quarterly & Annual) — This series shows the aggregate value of life insurance company assets, useful as a high-level indicator of industry scale over time. Life Insurance Companies; Total Financial Assets, Level (Quarterly & Annual)
Life Insurance Premium Volume to GDP (Annual) — Measures the relative size of life insurance premium flows compared to the overall economy, which can serve as a proxy for sales activity over time.  
Households and Nonprofits; Life Insurance Reserves; Asset, Level (Quarterly & Annual) — Captures the reserves held by households and nonprofits for life insurance, which offers insight into long-term commitments and purchasing behavior.  
Life Insurance Reserves & Annuity Entitlements; Liability (IMA), Level & Quarterly — Shows annual and quarterly liabilities for life insurance reserves and annuity entitlements, essential for connecting insurance commitments to macro movements.  
Life Insurance Companies; Total Liabilities & Total Assets (Quarterly) — Provides balance-sheet context for the industry as a whole.  
Producer Price Index: Insurance & Annuities: Life Insurance (WPU41110101) — A price index that can help connect price inflation and cost trends to insurance activity.  
These series extend back decades, which enables long-run analysis of economic cycles, interest rate regimes, and structural changes in insurance markets. The tagging system on FRED shows that thousands of related series are available, allowing flexibility in exploratory analysis.  
Macro Variables 
To explain industry behavior relative to the broader environment, I will also retrieve:
Interest rate series such as the 10-year Treasury yield
Inflation indicators like CPI or PPI
Equity market indices (e.g., S&P 500)
Volatility measures (e.g., VIX)
These macro series will be merged with the insurance industry series at a quarterly frequency for regression and trend analysis.
How the Data Will Be Used
Constructing a Longitudinal Panel: I will compile the quarterly and annual FRED series into a unified dataset covering several decades. Variables will be normalized where appropriate (e.g., ratios to GDP, index bases) so that structural relationships can be modeled.
Correlation and Regression Modeling: Using statistical methods, I will assess how life insurance assets, liabilities, and premium flows correlate with key macro factors such as interest rates, inflation, equity returns, and volatility. Separate models will be estimated for different segments of industry activity to understand heterogeneity in responses.
Comparative Insights Across Product Types: While FRED does not provide product-line sales directly (e.g., term vs IUL vs SPDA), industry financial account series offer proxies for how overall life insurance and annuity exposures grow or contract in response to macro conditions. I will compare these patterns to documented findings from actuarial and LIMRA-cited research where possible.
Contextualization with Prior Research: I will integrate findings from the empirical literature (e.g., studies on life insurance sales, goal-setting behavioral work) to support theoretical interpretation of observed macro-insurance patterns.
Ethical and Practical Considerations
All data used come from public, non-proprietary sources and are aggregated at an industry level, ensuring that individual privacy is preserved and data use complies with ethical standards. The analysis focuses on system-level behavior and economic relationships, not individual outcomes.
FRED Links 
Insurance, Life – Economic Data Series (Index of all relevant series)
https://fred.stlouisfed.org/tags/series?t=insurance%3Blife  
Life Insurance Companies; Total Financial Assets
(from the tag browser list on FRED)  
Life Insurance Premium Volume to GDP
(displayed in the FRED tag browser)  
Life Insurance Reserves & Annuity Entitlements; Liability (IMA), Level
https://fred.stlouisfed.org/series/BOGZ1FL543152205A  
Producer Price Index: Insurance & Annuities (Life Insurance)
https://fred.stlouisfed.org/series/WPU41110101  
