### ~ Libraries ~ ###
library(ggplot2)
library(dplyr)
library(lubridate)

### ~ Extraction ~ ###

#Trains!
boston_rail <- read.csv('/Users/benjaminfox/Desktop/Data400_Spring26/data/Public Transit Fer Mini Project/Boston_Rail.csv')
ny_rail <- read.csv('/Users/benjaminfox/Desktop/Data400_Spring26/data/Public Transit Fer Mini Project/New_York_Rail.csv')
chicago_rail <- read.csv('/Users/benjaminfox/Desktop/Data400_Spring26/data/Public Transit Fer Mini Project/Chicago_Rail.csv')

#Tour dates for reference - csvs I made from existing data
newYorkDates <- read.csv('/Users/benjaminfox/Downloads/Artists Playing Dates - In New York.csv')
bostonDates <- read.csv('/Users/benjaminfox/Downloads/Artists Playing Dates - In Boston.csv')
chicagoDates <- read.csv('/Users/benjaminfox/Downloads/Artists Playing Dates - In Chicago.csv')

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

#New York Rail
newYorkNoPercent <- ny_rail |> select(Date, Subways..Total.Estimated.Ridership,
                                      Buses..Total.Estimated.Ridership, 
                                      LIRR..Total.Estimated.Ridership,
                                      Metro.North..Total.Estimated.Ridership,
                                      Access.A.Ride..Total.Scheduled.Trips,
                                      Bridges.and.Tunnels..Total.Traffic,
                                      Staten.Island.Railway..Total.Estimated.Ridership)

colnames(newYorkNoPercent) <- c("Date","Subway Total", "Bus Total", 
                                "LIRR Total","Metro North Total", 
                                "Access A Ride Total","Bridge & Tunnel Total", 
                                "Staten Island Total")
#FYI, LIRR = Long Island Rail Road
#Access A Ride is those with disabilities to get around the city

#I ran a bunch of commands to clean the numbers into being processed as numbers
newYorkNoPercent <- newYorkNoPercent %>% mutate(TransitTotal = `Subway Total` + `Bus Total` +
                                                  `LIRR Total` + `Metro North Total` + 
                                                  `Access A Ride Total` + `Bridge & Tunnel Total` +
                                                  `Staten Island Total`)

CleanedNYTransit <- newYorkNoPercent %>% select(Date, TransitTotal,`Subway Total`, `Bus Total`,
                                                 `LIRR Total`, `Metro North Total`, `Access A Ride Total`,
                                                 `Bridge & Tunnel Total`, `Staten Island Total`)

#Where do I actually need to analyze tho? Like which trains for which shows?
#I will make vectors of concert dates for each artist

CleanedNYTransit$Date <- mdy(CleanedNYTransit$Date)

#Focusing on looking at the mean and median travel by year in each city
newYorkByYear <- summarise(group_by(CleanedNYTransit, substr(Date, 1,4)), 
                           meanBoardings = mean(TransitTotal),
                           medianBoardings = median(TransitTotal))

bostonByYear <- summarise(group_by(boston_rail_by_day, substr(servicedate, 1,4)),
                          meanBoardings = mean(sum_boardings),
                          medianBoardings = median(sum_boardings))

chicagoByYear <- summarise(group_by(doubleTrain, substr(`Service Date`, 1, 4)),
                           meanBoardings = mean(Total),
                           medianBoardings = median(Total))

colnames(chicagoByYear) <- c("Year", "Mean Transit", "Median Transit")

###Making final date charts before doing a wee bit of analysis
blankVector <- c(1:nrow(chicagoDates))

#Ensuring dates are built well
chicagoDates$Date <- ymd(chicagoDates$Date)
chicagoDates <- arrange(chicagoDates, Date)

#which(boston_rail_by_day$servicedate %in% bostonDates$Date[6])

#Building Basic Columns
for (i in blankVector){
  replaceRow <- which(doubleTrain$`Service Date` %in% chicagoDates$Date[i])
  
  blankVector[i] <- doubleTrain$Total[replaceRow]
}

for (i in blankVector){
  yur <- substr(chicagoDates$Date[i], 1, 4)
  blankVector[i] <- yur
}

chicagoDates <- cbind(chicagoDates,blankVector)

#Switch case loop
for (i in blankVector){
  the <- switch(chicagoDates$Year[i],
                "2020" = chicagoByYear$`Mean Transit`[1],
                "2021" = chicagoByYear$`Mean Transit`[2],
                "2022" = chicagoByYear$`Mean Transit`[3],
                "2023" = chicagoByYear$`Mean Transit`[4],
                "2024" = chicagoByYear$`Mean Transit`[5],
                "2025" = chicagoByYear$`Mean Transit`[6])
  
  blankVector[i] <- the
}

for (i in blankVector){
  and <- switch(chicagoDates$Year[i],
                "2020" = chicagoByYear$`Median Transit`[1],
                "2021" = chicagoByYear$`Median Transit`[2],
                "2022" = chicagoByYear$`Median Transit`[3],
                "2023" = chicagoByYear$`Median Transit`[4],
                "2024" = chicagoByYear$`Median Transit`[5],
                "2025" = chicagoByYear$`Median Transit`[6])
  
  blankVector[i] <- and
}

#Mutate the differentials
chicagoDates <- chicagoDates %>% 
  mutate(meanDifferential = `Transit Total` - `Yearly Average`,
         medianDifferential = `Transit Total` - `Yearly Median`)

colnames(chicagoDates) <- c("Date", "Artist", "Venue", "Transit Total", "Year", 
                           "Yearly Average", "Yearly Median",
                           "Mean Differential", "Median Differential")

chicagoDates <- cbind(chicagoDates[1:4],chicagoDates[6:9])

CutYorkDates <- newYorkDates[1:38,]

meanDifferentials <- data.frame("Cities" = c("New York", "New York","Boston", "Boston","Chicago","Chicago"),
                                "Mean Differentials" = c(
                                  mean(CutYorkDates$`Mean Differential`),
                                  mean(CutYorkDates$`Median Differential`),
                                  mean(bostonDates$`Mean Differential`),
                                  mean(bostonDates$`Median Differential`),
                                  mean(chicagoDates$`Mean Differential`),
                                  mean(chicagoDates$`Median Differential`)
                                ), "Mode" = c("Mean","Median","Mean","Median","Mean","Median"))

allDates <- rbind(CutYorkDates, bostonDates, chicagoDates)
allDates <- arrange(allDates, Date)

mean(allDates$`Mean Differential`)
mean(allDates$`Median Differential`)
