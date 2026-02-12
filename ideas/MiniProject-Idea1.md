# What health searches are gaining attention in each state, according to Google Trends? How does this interest associate with state-level obesity rate?
### _by Tu Tong_

## Data Sources

For this mini project, I plan to use Google Trends (https://trends.google.com/trends) search engine to retrieve time series data of different terms by different states in the U.S. Specifically, I would use relevant search terms (list not finalized) to collect data: 

- Diet: “Cheap food", “organic food", “supplements", “healthy foods”, “nutrition”, “calorie", “vegetable", “low carb”, “protein." 

- Behavioral: “gym near me", “weight loss", “exercises at home", “meal prep.” 

For the obesity rate, I am thinking of either using Prevalence of Obesity Based on Self- Reported Weight and Height by State, which is provided in csv file by [CDC Adult Obesity Prevalence Maps](https://www.cdc.gov/obesity/data-and-statistics/adult-obesity-prevalence-maps.html), or simply the obesity rate that is available on [Statista](https://www.statista.com/statistics/378988/us-obesity-rate-by-state/#:~:text=Data%20for%20obesity%20rates%20by%20state%20show,mostly%20found%20in%20the%20Southern%20United%20States.). The two sources here are both from 2024. 

After exploratory data analysis, I would use an ML model to predict obesity rates using people's interest in health. My features would be the frequency of those searches by state, and the obesity relevance (obesity rate) is the variable I want to predict. 

## Data Retrieval
At the moment, I am finalizing what keywords would be relevant to my topic before retrieving the data. I am consider to look at the data for multiple years.

## Model 

I am considering using either Random Forest or XGBoost to predict obesity based on the frequencies of the search terms mentioned above. 

 

## Implications for stakeholders 

Results from this project will help people who work in healthcare (CDC, health policymakers) understand more about how health interest relates to outcomes. This would help understand what health trends are gaining popularity within each state. Additionally, we can see if awareness/trends can impact health behaviors and outcomes. 



## Ethical, legal, societal implications 

What contributes to health outcome improvements is really hard to decide, as health is influenced by social and economic context. While studies in this area often focus on external factors, this project concentrates on the expressed interest and curiosity one has in terms of health. This project uses machine learning to help with prediction and to determine if social interests in health from people can signify outcomes or not. The result would reveal relevancy and correlation, instead of causal inference. Google Trends data is aggregated data; therefore, the result from this project does not indicate individual behaviors or responsibility, instead, it provides a look into social trends related to health. 

----
## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
