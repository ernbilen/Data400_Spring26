# Luke Finkielstein Mini Project Idea Proposal: 
# NBA Game & Stat Prediction  


Research Question: How can we predict the outcome of NBA games with better than 60% accuracy? 

Approach: Develop a classification model (probably logistic regression) to predict NBA game outcomes using historical game statistics and betting odds. The model will identify games with favorable edges to inform predictions. 


## Gathering Tractable Data  

**Target:** Game outcomes (win/loss)

**Key Features:**
- Team performance metrics (record, scoring, defense)
- Player availability/injury status
- Opponent strength ranking
- Game context (home/away, back-to-back games)
- Betting odds from sportsbooks (BetGM, DraftKings, Fanduel, etc.)

**Data sources:** ESPN, NBA.com, Basektball-reference.com, Kaggle all have pre-compiled datasets of real games going back 20+ years. Additional data can be scraped from these websites if necessary. Feasibility is high—game data and odds are publicly available. 

## Retrieval & Preparation

Two viable approaches:

- Use existing public dataset (faster, reduces timeline overhead)
- Web scrape/API calls for game stats and odds (more control, more time-intensive)


## EDA & Insights

Analyze outcome variation by team strength, matchups, injuries, and game context. Identify predictive features (home-court advantage, efficiency metrics). Perform EDA and visualize feature correlations with game outcomes. Calculate correlations between candidate features and game outcomes to determine which have the strongest predictive signals. Visualizations will include scatter plots of team efficiency metrics, heatmaps of feature correlations, and distribution plots comparing home vs. away performance. I can compare the model performance against a simple baseline (like always predicting the higher-seeded team) to ensure the model adds meaningful value.

## Potential Limitations

- **Unpredictable events:** Model cannot account for unexpected injuries, trades, coaching changes, or rest decisions made close to game time.
- **Probabilistic predictions:** Accuracy >50% does not guarantee profit; individual game predictions are probabilistic and subject to variance.
- **Data limitations:** Historical data may not fully capture changes in league dynamics, rule changes, or roster composition over 20+ years.
- **Sample size:** Model performance is limited by the number of games available for training and testing.

## Implications for Stakeholders 

**Sports Bettors/Fans:** Would help make informed decisions on predicting winners and increase profitability.

**Sportsbooks:** Understand what drives betting patterns and refine odds-setting.

**NBA Teams**: Understanding which factors affect a team's ability to win would be very interesting to coaches/players/owners.

## Responsible Deployment & Ethics

**Concerns:** Model could encourage problem gambling; predictions are probabilistic and not deterministic. 

**Legal:** Gambling laws vary by state (sports betting is legal in PA, both online and in person). This model would be for analysis only, not financial advice.

**Mitigation:** Include gambling risk disclaimers, talk about it as purely academic.

## Timeline

- Weeks 1-2: Data collection/preparation
- Week 3: EDA and feature engineering
- Weeks 4-5: Model development and evaluation

**Deliverable:** Trained  model with accuracy metrics and feature importance analysis.