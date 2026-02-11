# DATA400 Mini-Project Idea 1
## Ben Brandt

For my mini-project, I plan on scraping housing data from Zillow from my zipcode and some neighboring zipcodes in order to predict the price of houses.

### Tractable Data
In terms of the kind of data I want, I want the typical information that someone looking for a home might consider when making a decision about buying a house. All of this information is available directly on the Zillow website. This information includes numerical values such as the number of bedrooms, number of bathrooms, square footage, and lot acreage. Additionally, there is a categorical variable present that I would like to include as well which is the kind of house (i.e townhouse, single family residence, etc.). This all together is used for as predictor variables for our response variable which would be the price of the house.

### Data Retrieval
The way I anticipate getting this data is by simply scraping it off the website myself. Using a list of zipcodes, I can navigate through all the available homes for each zipcode and use the XPath to scrape all the necessary data I might need. In practice, this would be very similar to the DATA200 GoodReads project.

### Specification of Model
I think the best model to use for this project is a Random Forest. This model is very versatile and is usable in most situations. I think in this case particularly it will better highlight the importance of certain variables over others. And since Random Forests deal with multicollinearity, there is less concern about variables being correlated with one another.

### Implications of Stakeholders
I think there are a lot of stakeholders at hand that can be affected by this project. The first and most obvious of which is people who are currently looking for a home in the Northern Virginia area who are trying to find an estimated price given their specifications. A second potential stakeholder would be the people selling their homes, they can use the model to see what their own home is worth and determine a price accordingly. A third stakeholder would be the realty companies selling these homes. They can use the model to better understand what types of homes are being sold and at what price points and can change their realty strategy accordingly.

### Ethical, Legal, and Societal Implications
There are definitely some legal and societal implications of doing this project both positive and negative. In terms of legality, Zillow likely is not a fan of people scraping their site and it might violate the terms of service. There is also the question of violating homeowners privacy but I think as long as addresses and photos are not included that should minimize any direct exposure to homeowners. Some negative societal impacts that could be at play is the potential that there might end up bringing reduced affordability in certain areas or bulk investing. However, there is also societal upsides that are also important to consider such as affordability transparency and helping buyers and renters make better decisions about the kind of home they buy.