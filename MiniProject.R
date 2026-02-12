### ~ Libraries ~ ###
library(ggplot2)
library(dplyr)
library(lubridate)

### ~ Extraction ~ ###

#Trains!
boston_rail <- read.csv('/Users/benjaminfox/Desktop/Data400_Spring26/data/Public Transit Fer Mini Project/Boston_Rail.csv')
ny_rail <- read.csv('/Users/benjaminfox/Desktop/Data400_Spring26/data/Public Transit Fer Mini Project/New_York_Rail.csv')
chicago_rail <- read.csv('/Users/benjaminfox/Desktop/Data400_Spring26/data/Public Transit Fer Mini Project/Chicago_Rail.csv')
la_rail <- ":)"
philly_rail <- ":("

#Hotels!


#Tour dates for reference


### ~ Refactoring ~ ###

#Boston Rail
boston_rail_by_day <- summarise(group_by(boston_rail, servicedate), sum_boardings = sum(estimated_boardings))

boston_rail_by_day <- boston_rail_by_day %>% mutate(generous_revenue = sum_boardings * 2.4,
                                                    kinda_generous = sum_boardings * 1.1)

#Chicago Rail
which(grepl('202',chicago_rail$service_date)==TRUE)
trimmed_chicago <- chicago_rail[which(grepl('202',chicago_rail$service_date)==TRUE),]

chicago_dates_for_r <- mdy(trimmed_chicago$service_date)

doubleTrain <- cbind(chicago_dates_for_r,weekdays(chicago_dates_for_r),
                     trimmed_chicago[2:5])
colnames(doubleTrain) <- c("Service Date", "Day of Week", "Day Type", "Bus", "Rail", "Total")

