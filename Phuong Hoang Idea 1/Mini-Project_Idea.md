# Mini-Project Idea Proposal: When does Google Search fail to predict opening revenue for blockbusters?
By Phuong Hoang
> *“Every time I go to a movie, it's magic, no matter what the movie’s about.”* — Steven Spielberg

--

#### Project goal

- The goal of this project is to examine the extent to which Google Search interest predicts opening-weekend box office revenue and how the introduction of TikTok as a new social media channel may systematically alter this relationship. 

- Using a dataset of 50 pre-2025 movies with opening weekend revenue, Google Trends pre-release search interest, and movie characteristics, the analysis applies standard regression and a Difference-in-Differences framework. The project aims to reveal the limitations of online search behavior as an economic signal for consumer demand.


#### Tractable Data

- The dataset for this project does not exist in a single, ready-to-use form and must be collected and combined from multiple sources. It will consist of **50** pre-2025 movies selected based on theoretically motivated conditions under which Google Search is expected to fail as a predictor of opening-weekend revenue. 

- For each movie, numeric variables such as opening weekend revenue (USD), number of theaters, and Google Trends search interest will be included, along with categorical variables such as distributor, release year, and optionally engineered features like franchise status, holiday release, or big studio classification. [attentive to change]

- By merging information from sources such as Box Office Mojo, Google Trends, and IMDb, the final dataset is small, clean, and fully observable.


#### Data Retrieval
- Firstly, using [boxofficemojo-scraper](https://github.com/tjwaterman99/boxofficemojo-scraper), the dataset scraped from [Box Office Mojo](https://www.boxofficemojo.com), this project will run filtering codes to select 50 pre-2025 movies under specific conditions. The filtered data will include original columns such as "date", "title", "revenue (USD)", "#theaters", "distributor". Using these variables, the project will later create engineered features including "franchise" (Yes/No), "during_holiday" (Yes/No), "big_studio" (Yes/No) [attentive to change].

- Secondly, using  `pytrends` in Python or manually via Google Trends interface, this project will have consistent and predetermined search terms for all selected movies. The period of search will be 2-4 weeks prior to release data and the geography will be set to the U.S. A clean dataset can be downloaded with "search terms" , "search interest", "increase percent."

- Thirdly, any other needed feature engineering will be gathered ultilizing webscraping through [IMDB](https://www.imdb.com) official website [attentive to change]. 

- Finally, a binary variable indicating whether the movie was released after TikTok will be added to facilitate the Difference-in-Differences analysis. 

- The final dataset will be a merged and filtered version of all sources, including opening weekend revenue, Google Trends data, movie characteristics, and TikTok timing, ready for regression, Difference-in-Differences analysis, and exploratory data analysis.


#### Exploratory Data Analysis 
###### [attentive to change]
- The exploratory data analysis (EDA) will focus on understanding the relationships between Google Trends search interest, opening-weekend revenue, and other movie characteristics, as well as identifying patterns related to TikTok adoption. 

- Likely EDA techniques include scatterplots comparing Google Trends scores to actual revenue, boxplots or histograms showing summary statistics (mean, median, standard deviation) of predicting variables. 

- Additionally, a correlation heatmap will be used to examine the relationships among predictors such as revenue, number of theaters, Google Trends scores, and engineered features like franchise or holiday release. 

- Further visualizations may examine differences across categories such as franchise vs. non-franchise, genre, and pre- versus post-TikTok movies to explore systematic shifts in prediction error. 

#### Implications for stakeholders
The findings of this project have practical implications for multiple stakeholders in the film industry. Movie studios and marketing teams should understand that Google Search interest does not always accurately predict opening-weekend revenue. Particularly in the era of social media platforms like TikTok, Gen Z's attention has shifted outside traditional search channels. This insight can inform marketing strategies, such as investing in viral social media campaigns or targeting audiences on platforms like TikTok for early hype.

#### Ethical, legal, societal implications
- This project relies exclusively on publicly available data, including Box Office Mojo, Google Trends, and IMDb, and does not violate private or personally identifiable information.

- Legally, the data collection methods, including scraping and using APIs, will comply with the respective platforms’ terms of service. 

- From a societal perspective, the project highlights the limitations of relying on solely search engine interests, like Google Search, as indicators for real-world economic behavior. Understanding possible biases is important for investors to not overrely on these metrics and misrepresent consumer demand.









