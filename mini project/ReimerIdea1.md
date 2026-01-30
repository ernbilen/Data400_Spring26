# First Idea
### Delaney Reimer

My idea is to look at Netflix original shows that were cancelled after only one season. I plan to look at all of these measures to see if there are patterns or outliers in the shows that were cancelled:
- Viewership Stats (both hours watched and total watches [hours watched/length of show])
- Cost to Produce/Market (if available)
- Rotten Tomatoes Rating
- Genre(s)/Categorization in Netflix

For viewership stats, I can pull data from 2023-2025 from Netflix's Engagement Reports, which have been compiled [here](https://www.whats-on-netflix.com/most-popular/netflix-engagement-report-search/). Rotten Tomatoes ratings will obviously be available on Rotten Tomatoes, which can potentially be scraped or individually input depending on the volume of data. I'm not sure where to find production and marketing costs, or if that'll even be publicly available for all of the shows I'm looking at yet. I've found a dataset with genre information on [Kaggle](https://www.kaggle.com/datasets/bhargavchirumamilla/netflix-movies-and-tv-shows-till-2025), so that's already settled. As for a list of cancelled Netflix original shows, [this article](https://en.wikipedia.org/wiki/List_of_ended_Netflix_original_programming) contains a comprehensive list of ended Netflix shows, which I will filter to only look at those that were cancelled (i.e., not limited series that were only expected to have a single season) and that only had one season before cancellation.

For this, I will be using an inferential model to determine if there is a correlation between viewership, rating, and genre and cancellation/lack of renewal, and if so, what it might be. 

This research will be important to both executives/stakeholders in knowing which shows are most likely to be cancelled after only one season and thus probably not as worth it to create, as viewers prefer complete stories over cliffhangers that will never be resolved. This will also be important to consumers to give an insight into the reasoning behind cancellation of shows and whether they can expect other shows they enjoy to be renewed or cancelled down the line. 

Since all of this data will be public (except for possibly costs), there is no ethical issues with data privacy. In terms of benefits, this model could potentially assist in future creation or production (like what genres may be more popular/likely to be more widely enjoyed), as well as make the process more transparent for consumers/subscribers, since for the most part Netflix does not make a statement on the official reasoning behind cancellation.