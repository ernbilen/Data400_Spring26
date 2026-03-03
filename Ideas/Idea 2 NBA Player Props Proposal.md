# Luke Finkielstein Mini Project Idea Proposal 2:
# NBA Player Props Prediction

Research Question: Can we predict NBA player point totals with reasonable accuracy using historical performance, matchup data, and contextual factors?

Approach: Develop a regression model to predict individual player point totals in NBA games using historical player statistics and game context. The model will help identify player prop betting opportunities.

## Gathering Tractable Data

**Target:** Individual player point totals per game

**Key Features:**
- Player historical scoring average (season, last 10 games, vs. specific opponents)
- Opponent defensive rating (points allowed per game)
- Game context (home/away, back-to-back games, rest days)
- Player usage rate and minutes played trends
- Opponent pace of play
- Player injury/availability status

**Data sources:** ESPN, Basketball-reference.com, NBA.com, Kaggle datasets with historical player-game logs. Feasibility is high—player statistics are publicly available and well-documented.

## Retrieval & Preparation

Two approaches:
- Use existing player-game log datasets (faster, reduces timeline)
- Web scrape player statistics from ESPN/Basketball-reference (more control, more time-intensive)

## EDA & Insights

Analyze how player scoring varies by opponent strength, rest status, and usage rate. Identify key predictive features (recent form, matchup difficulty). Calculate correlations between candidate features and player point totals. Visualizations will include scatter plots of usage rate vs. scoring, distribution plots of scoring by opponent defense rating, and time-series analysis of individual player trends. Compare model performance against a simple baseline (e.g., using season average) to ensure meaningful predictive value.

## Potential Limitations

- **Game-to-game variance:** Player performance is highly variable; some games are outliers due to hot/cold shooting.
- **Injury uncertainty:** Last-minute injuries or load management decisions affect playing time unpredictably.
- **Small sample sizes:** Some matchups may have limited historical data.
- **Model assumes consistency:** Player form and roles can change mid-season due to trades or coaching changes.

## Implications for Stakeholders

**Sports Bettors:** Help identify player prop bets with positive expected value.

**Sportsbooks:** Understand what drives player prop lines and refine odds-setting.

**NBA Analysts:** Identify which factors most influence individual player performance.

## Responsible Deployment & Ethics

**Concerns:** Model could encourage problem gambling; predictions are probabilistic.

**Legal:** Gambling laws vary by state. This model is for analysis only, not financial advice.

**Mitigation:** Include gambling risk disclaimers; frame as educational/analytical exercise.