data <- read.csv("Country_Level_Info.csv", header=TRUE)

subdata <- data[data[,'Country_Region'] == 'China', ]
print(subdata)

ggplot(subdata, aes(Date, New_Confirmed_Cases)) + geom_line() + xlab(" ") + ylab("Daily Views")

country_name <- unique(data[,"Country_Region"])

print(country_name)

data$Date <- as.Date(data$Date)
typeof(data$Date)
print(data)
