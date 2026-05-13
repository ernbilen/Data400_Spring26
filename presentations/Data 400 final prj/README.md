# Rising Fast, Falling Slow: The Hidden Cost of Gasoline Price Asymmetry
### A Data-Driven Analysis of Pass-Through Speed, Regional Disparity, and Price Prediction in U.S. Fuel Markets

**Authors:** Kien Nguyen · Hoa Ly  
**Course:** DATA 400 — Spring 2026  
**Institution:** Dickinson College

---

## Project Overview

This project investigates the "Rockets and Feathers" effect in U.S. retail gasoline markets — the well-documented but underquantified phenomenon where pump prices rise quickly when crude oil increases but fall slowly when crude decreases (Bacon, 1991).

Using 26 years of weekly data (2000–2026) from the U.S. Energy Information Administration (EIA) and the Federal Reserve Economic Data (FRED) API, we answer three research questions:

- **Q1:** Do gas prices rise faster than they fall, and by how much?
- **Q2:** Which U.S. regions are most vulnerable to price shocks?
- **Q3:** Can supply chain signals predict next-week gas price movements?

**Key Findings:**
- Asymmetric pass-through confirmed: upward pass-through is **17.8% faster** than downward (Wald F=4.82, p=0.028)
- Supply chain decomposition: asymmetry is concentrated entirely in **Stage 2 — retailers** (Wald F=55.01, p<0.0001). Refiners behave symmetrically (p=0.76)
- A **$2.14/gal regional price gap** exists between PADD 5 (West Coast, $4.42) and PADD 3 (Gulf Coast, $2.28)
- Best predictive model: **Lasso Regression** — MAE=$0.033/gal, R²=0.421, Directional Accuracy=76.9%
- Long-run ECM (Granger-Lee) confirms asymmetry is a **short-run pricing friction**, not a permanent structural bias

---

## Repository Structure

```
Data400_Spring/
├── README.md                            ← This file
├── requirements.txt                     ← Python dependencies
│
├── data/
│   ├── raw/
│   │   ├── eia/                         ← Raw EIA API responses (5 files)
│   │   │   ├── retail_gasoline_prices.csv
│   │   │   ├── spot_prices.csv
│   │   │   ├── gasoline_stocks.csv
│   │   │   ├── refinery_utilization.csv
│   │   │   └── futures_prices.csv
│   │   ├── fred/                        ← Raw FRED API responses (10 files)
│   │   │   ├── GASREGW.csv              ← Weekly retail gas price
│   │   │   ├── DCOILWTICO.csv           ← WTI Crude Oil (daily)
│   │   │   ├── DCOILBRENTEU.csv         ← Brent Crude Oil (daily)
│   │   │   ├── DTWEXBGS.csv             ← USD Index (daily)
│   │   │   ├── CPIAUCSL.csv             ← Consumer Price Index (monthly)
│   │   │   ├── UMCSENT.csv              ← Consumer Sentiment (monthly)
│   │   │   ├── DFF.csv                  ← Federal Funds Rate (daily)
│   │   │   ├── DHHNGSP.csv              ← Henry Hub Natural Gas (daily)
│   │   │   ├── GEPUCURRENT.csv          ← Global Economic Policy Uncertainty (monthly)
│   │   │   └── USEPUINDXD.csv           ← U.S. Economic Policy Uncertainty (daily)
│   │   └── us-states.json               ← GeoJSON for PADD choropleth map
│   └── processed/
│       └── master_dataset.csv           ← Final merged dataset (56 variables, 1,370 weeks)
│
├── 01_Data_Collection.ipynb             ← API pulls from EIA and FRED
├── 02_Data_Cleaning.ipynb               ← Cleaning, merging, feature engineering
├── 03_Viz1_PADD_Map.ipynb               ← U.S. PADD choropleth map with refineries
├── 04_Viz2_TimeSeries_Events.ipynb      ← 26-year timeline + crisis comparison
├── 05_Viz3_Geopolitical_NatGas.ipynb    ← Geopolitical uncertainty + natural gas
├── 06_Predictive_Modeling.ipynb         ← 7 models compared + asymmetric OLS
├── 07_Best_Model_Visuals.ipynb          ← Lasso optimization + poster-ready charts
├── 08_ECM_Asymmetric_PassThrough.ipynb  ← Error Correction Model (Granger-Lee 1989)
├── 09_Crack_Spread_Mediation.ipynb      ← Two-stage supply chain decomposition
│
└── outputs/                             ← All generated charts and tables (PNG)
```

---

## Data Sources

### EIA (U.S. Energy Information Administration)
**API:** https://www.eia.gov/opendata/  
**Requires:** Free API key (register at link above)

| File | Description | Rows | Coverage |
|------|-------------|------|----------|
| `retail_gasoline_prices.csv` | Retail gas prices by PADD region and grade ($/gal) | 10,332 | 1993–2026 |
| `spot_prices.csv` | Wholesale spot prices — WTI, Gulf Coast, NY Harbor | 6,256 | 1986–2026 |
| `gasoline_stocks.csv` | Gasoline inventory by PADD region (thousand barrels) | 16,884 | 1990–2026 |
| `refinery_utilization.csv` | Refinery utilization rates and crude inputs by region | 71,810 | 1982–2026 |
| `futures_prices.csv` | Crude oil futures contracts (1st and 2nd month, $/bbl) | 4,189 | 1983–2026 |

> EIA raw files include full API metadata columns: `period`, `duoarea`, `area-name`, `product`, `product-name`, `process`, `process-name`, `series`, `series-description`, `value`, `units`.

### FRED (Federal Reserve Bank of St. Louis)
**API:** https://fred.stlouisfed.org/  
**Requires:** Free API key (register at link above)

| File | Series ID | Description | Frequency | Coverage |
|------|-----------|-------------|-----------|----------|
| `GASREGW.csv` | GASREGW | U.S. weekly retail gasoline price ($/gal) | Weekly | 2000–2026 |
| `DCOILWTICO.csv` | DCOILWTICO | WTI Crude Oil spot price ($/bbl) | Daily | 2000–2026 |
| `DCOILBRENTEU.csv` | DCOILBRENTEU | Brent Crude Oil spot price ($/bbl) | Daily | 2000–2026 |
| `DTWEXBGS.csv` | DTWEXBGS | Nominal USD broad dollar index | Daily | 2006–2026 |
| `CPIAUCSL.csv` | CPIAUCSL | Consumer Price Index, all urban consumers | Monthly | 2000–2026 |
| `UMCSENT.csv` | UMCSENT | U. of Michigan Consumer Sentiment Index | Monthly | 2000–2026 |
| `DFF.csv` | DFF | Federal Funds Effective Rate (%) | Daily | 2000–2026 |
| `DHHNGSP.csv` | DHHNGSP | Henry Hub Natural Gas spot price ($/MMBtu) | Daily | 2000–2026 |
| `GEPUCURRENT.csv` | GEPUCURRENT | Global Economic Policy Uncertainty Index | Monthly | 2000–2025 |
| `USEPUINDXD.csv` | USEPUINDXD | U.S. Economic Policy Uncertainty Index | Daily | 2000–2026 |

> FRED raw files are 2-column format: `date`, `value`.

---

## Master Dataset

**File:** `data/processed/master_dataset.csv`  
**Observations:** 1,370 weeks (2000-01-03 to 2026-03-30)  
**Variables:** 56 total  
**Frequency:** Weekly (resampled to Monday)

### Complete Variable List

**Regional Retail Prices**

| Variable | Description | Units |
|----------|-------------|-------|
| `period` | Week start date (Monday) | Date |
| `retail_national` | U.S. average retail gasoline price | $/gal |
| `retail_padd1_east` | PADD 1 East Coast retail price | $/gal |
| `retail_padd2_midwest` | PADD 2 Midwest retail price | $/gal |
| `retail_padd3_gulf` | PADD 3 Gulf Coast retail price | $/gal |
| `retail_padd4_rocky` | PADD 4 Rocky Mountain retail price | $/gal |
| `retail_padd5_west` | PADD 5 West Coast retail price | $/gal |

**Wholesale & Crude Prices**

| Variable | Description | Units |
|----------|-------------|-------|
| `spot_gasoline` | NY Harbor wholesale gasoline spot price | $/gal |
| `spot_gas_gulf` | Gulf Coast wholesale gasoline spot price | $/gal |
| `spot_gas_nyh` | NY Harbor gasoline spot price (alternate series) | $/gal |
| `wti_crude` | WTI crude oil spot price (EIA source) | $/barrel |
| `wti_crude_fred` | WTI crude oil spot price (FRED source) | $/barrel |
| `brent_crude` | Brent crude oil spot price | $/barrel |
| `crude_per_gallon` | WTI crude converted to per-gallon (÷42) | $/gal |
| `crude_futures_1m` | Crude oil front-month futures price | $/barrel |
| `crude_futures_2m` | Crude oil second-month futures price | $/barrel |

**Supply Chain & Margins**

| Variable | Description | Units |
|----------|-------------|-------|
| `crack_spread` | Refiner margin: spot_gasoline − crude_per_gallon | $/gal |
| `crude_retail_spread` | Full chain spread: retail_national − crude_per_gallon | $/gal |
| `refinery_util_national` | U.S. national refinery utilization rate | % |
| `refinery_util_r10` | PADD 1 refinery utilization | % |
| `refinery_util_r20` | PADD 2 refinery utilization | % |
| `refinery_util_r30` | PADD 3 refinery utilization | % |
| `refinery_util_r40` | PADD 4 refinery utilization | % |
| `refinery_util_r50` | PADD 5 refinery utilization | % |
| `gasoline_stocks` | U.S. total gasoline inventory | thousand barrels |
| `stocks_r10` | PADD 1 total stocks | thousand barrels |
| `stocks_r1x` | PADD 1A stocks | thousand barrels |
| `stocks_r1y` | PADD 1B stocks | thousand barrels |
| `stocks_r1z` | PADD 1C stocks | thousand barrels |
| `stocks_r20` | PADD 2 stocks | thousand barrels |
| `stocks_r30` | PADD 3 stocks | thousand barrels |
| `stocks_r40` | PADD 4 stocks | thousand barrels |
| `stocks_r50` | PADD 5 stocks | thousand barrels |

**Macroeconomic Variables**

| Variable | Description | Units |
|----------|-------------|-------|
| `usd_index` | Nominal USD broad dollar index | Index |
| `cpi` | Consumer Price Index (all urban) | Index |
| `consumer_sentiment` | U. of Michigan Consumer Sentiment | Index |
| `fed_funds_rate` | Federal Funds Effective Rate | % |
| `retail_gas_fred` | Weekly retail gas price (FRED GASREGW series) | $/gal |

**Engineered Features**

| Variable | Description | Units |
|----------|-------------|-------|
| `retail_national_chg` | Week-over-week retail price change | $/gal |
| `retail_national_pct_chg` | Week-over-week retail price % change | % |
| `wti_crude_chg` | Week-over-week WTI crude change (EIA) | $/barrel |
| `wti_crude_pct_chg` | Week-over-week WTI crude % change | % |
| `wti_crude_fred_chg` | Week-over-week WTI crude change (FRED) | $/barrel |
| `wti_crude_fred_pct_chg` | Week-over-week WTI crude % change (FRED) | % |
| `spot_gasoline_chg` | Week-over-week spot gasoline change | $/gal |
| `spot_gasoline_pct_chg` | Week-over-week spot gasoline % change | % |
| `gasoline_stocks_chg` | Week-over-week inventory change | thousand barrels |
| `gasoline_stocks_pct_chg` | Week-over-week inventory % change | % |
| `retail_ma4` | 4-week moving average of retail price | $/gal |
| `retail_ma12` | 12-week moving average of retail price | $/gal |
| `month` | Month of observation (1–12) | Integer |
| `week_of_year` | Week of year (1–52) | Integer |
| `quarter` | Quarter (1–4) | Integer |
| `is_summer_blend` | Summer blend season flag: 1 = Mar–Sep | 0/1 |
| `target_next_week_chg` | **Target variable:** next week's price change | $/gal |
| `target_direction` | Direction of next week's change (1=up, 0=down) | 0/1 |

---

## Notebook Guide

| Notebook | Purpose | Key Outputs |
|----------|---------|-------------|
| `01_Data_Collection.ipynb` | Pulls all raw data via EIA and FRED APIs | Raw CSVs in `data/raw/` |
| `02_Data_Cleaning.ipynb` | Cleans, aligns, merges all series + engineers all features | `master_dataset.csv` |
| `03_Viz1_PADD_Map.ipynb` | PADD choropleth with ~125 refineries, 9 oil fields, 7 city prices | `map_padd_refineries_v2.png`, `map_price_premium.png` |
| `04_Viz2_TimeSeries_Events.ipynb` | 26-year timeline with 19 annotated world events + crisis comparison | `timeline_annotated_full.png`, `crisis_comparison.png`, `rockets_feathers.png` |
| `05_Viz3_Geopolitical_NatGas.ipynb` | Global Policy Uncertainty overlay + natural gas correlation (r=0.04) | `geopolitical_uncertainty.png`, `natural_gas_comparison.png` |
| `06_Predictive_Modeling.ipynb` | Compares 7 ML models + asymmetric OLS (Bacon 1991 method) | `model_comparison_final.png`, `asymmetry_regression.png` |
| `07_Best_Model_Visuals.ipynb` | Optimized Lasso with LassoCV + poster-ready prediction charts | `prediction_dashboard.png`, `price_trajectory.png`, `feature_importance_lasso.png` |
| `08_ECM_Asymmetric_PassThrough.ipynb` | Engle-Granger cointegration + Granger-Lee asymmetric ECM | `ecm_asymmetry_dashboard.png`, `table_ecm_summary.png` |
| `09_Crack_Spread_Mediation.ipynb` | Two-stage supply chain decomposition — who captures the asymmetry? | `crack_margin_history.png`, `crack_asymmetry_decomposition.png`, `table_crack_summary.png` |

---

## Setup & Reproduction

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Data400_Spring.git
cd Data400_Spring
```

### 2. Create Conda Environment
```bash
conda create -n gas_analysis python=3.10
conda activate gas_analysis
pip install -r requirements.txt
```

### 3. Install geopandas via Conda (required for Notebook 03 only)
```bash
# Do NOT use pip for geopandas — conda handles the proj/gdal dependency correctly
conda install -c conda-forge geopandas
```

### 4. Add Your API Keys
Open `01_Data_Collection.ipynb` and replace at the top:
```python
EIA_API_KEY  = "your_eia_key_here"   # Free: https://www.eia.gov/opendata/
FRED_API_KEY = "your_fred_key_here"  # Free: https://fred.stlouisfed.org/
```

### 5. Run Notebooks in Order
```
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09
```

> **Shortcut:** `master_dataset.csv` is already provided in `data/processed/`. You can skip notebooks 01–02 and run 03–09 directly without any API keys.

---

## Data Quality Notes

| Issue | Resolution |
|-------|-----------|
| 10.3% null values in refinery utilization | Forward-filled up to 4 weeks maximum |
| 6,531 invalid negative values in refinery data | Filtered to valid range 0–105% |
| EIA API returned pagination metadata as strings | Cast to integers before processing |
| Mixed frequencies (daily/weekly/monthly) | All series resampled to Monday-weekly |
| Data leakage in Notebook 07 | `target_next_week_chg`, `target_direction`, `price_direction` excluded from all feature sets |

---

## Key Results Summary

### Q1 — Asymmetric Pass-Through (Rockets & Feathers)

**Short-run OLS (Notebook 06):**
- β₁ (crude rises) = 0.284 vs β₂ (crude falls) = 0.241 — Wald F=4.82, **p=0.028** ✅
- 12-week cumulative: +6% after crude rises vs −4% after crude falls

**Supply Chain Decomposition (Notebook 09):**
- Stage 1 (crude → refiner margin): Wald p=0.76 → refiners are **symmetric**
- Stage 2 (spot → retail): Wald F=55.01, **p<0.0001** → **retailers drive all asymmetry**
- Ukraine 2022 exception: refiners captured record margin ($1.57/gal crack spread peak)

**Long-run ECM (Notebook 08):**
- Asymmetry is a short-run pricing friction, not a permanent long-run structural bias

### Q2 — Regional Vulnerability

| PADD Region | Avg Price | vs National | Refineries |
|-------------|-----------|-------------|------------|
| PADD 5 — West Coast | $4.42/gal | +$1.10 | 16 |
| PADD 1 — East Coast | $3.20/gal | −$0.12 | 5 |
| PADD 4 — Rocky Mountain | $3.09/gal | −$0.23 | 15 |
| PADD 2 — Midwest | $3.04/gal | −$0.28 | 22 |
| PADD 3 — Gulf Coast | $2.28/gal | −$1.04 | 40 |
| **Max − Min Gap** | **$2.14/gal** | | |

### Q3 — Predictive Modeling

| Model | MAE | RMSE | R² | Dir. Accuracy |
|-------|-----|------|----|---------------|
| Naive Baseline | $0.0458 | $0.0566 | −0.003 | 57.7% |
| LR (Crude Only) | $0.0399 | $0.0518 | 0.160 | 63.5% |
| Multiple LR | $0.0460 | $0.0573 | −0.025 | 63.5% |
| Ridge | $0.0402 | $0.0491 | 0.246 | 69.2% |
| Random Forest | $0.0360 | $0.0470 | 0.308 | 78.8% |
| XGBoost | $0.0358 | $0.0468 | 0.315 | 75.0% |
| **Lasso (Best)** | **$0.0326** | **$0.0430** | **0.421** | **76.9%** |

Train/test split: 910 train weeks / 52 test weeks — strict temporal ordering, no data leakage.

**Top 5 Predictive Features:**
1. `retail_national_chg` — last week's price change (importance: 0.197)
2. `retail_national_pct_chg` — % change (0.148)
3. `retail_ma4` — 4-week moving average deviation (0.070)
4. `spot_gasoline_chg` — wholesale price change (0.028)
5. `crude_futures_2m` — 2-month crude futures (0.027)

---

## References

- Bacon, R.W. (1991). "Rockets and feathers: the asymmetric speed of adjustment of UK retail gasoline prices." *Energy Economics*, 13(3), 211–218.
- Granger, C.W.J., & Lee, T.H. (1989). "Investigation of production, sales and inventory relationships using multicointegration and non-symmetric error correction models." *Journal of Applied Econometrics*, 4, S145–S159.
- Borenstein, S., Cameron, A.C., & Gilbert, R. (1997). "Do gasoline prices respond asymmetrically to crude oil price changes?" *Quarterly Journal of Economics*, 112(1), 305–339.
- Baker, S., Bloom, N., & Davis, S. (2016). "Measuring Economic Policy Uncertainty." *Quarterly Journal of Economics*, 131(4), 1593–1636.
- U.S. Energy Information Administration. Open Data API. https://www.eia.gov/opendata/
- Federal Reserve Bank of St. Louis. FRED Economic Data. https://fred.stlouisfed.org/

---

*Last updated: April 2026*
