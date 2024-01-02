library(ggplot2)

setwd("C:/Users/Elie/OneDrive/Desktop/Spring 2022/CMPS 276/Milestones/Milestone 2/Milestone 2")
df <- read.csv("finalDataset.csv", header=TRUE, na.strings = "")
head(df)

for (i in seq_len(length(df$Year))) {
  df$Year[i] <- (paste("01-01-",as.character(df$Year[i]),sep=""))
}

df$Year <- as.Date(df$Year, format="%d-%m-%Y")
unique(df$Year)
sapply(df, class)

df$HDI <- sapply(df$HDI, cut, breaks = c(0, 0.55, 0.7, 0.8, 1),
               labels = c("Low", "Medium", "High", "Very High"))
df <- na.omit(df)
df <- subset(df, df$Continent.Code!="Unknown")
ggplot(df, aes(x=Year, y=Net.Migration.Ratio, group=Year)) +
  geom_boxplot() +
  coord_cartesian(ylim=c(-50,50)) +
  labs(title = "Variation of Net Migration per Year",
       y = "Net Migration Rate", x = "Year")

ggplot(df[df$DALYs<150000,], aes(x=Year, y=DALYs, group=Year)) +
  geom_boxplot() +
  labs(title = "Variation of DALYs~ per Year",
       y = "DALYs", x = "Year")

ggplot(df, aes(x=Year, y=GDP, group=Year)) +
  geom_boxplot() +
  coord_cartesian(ylim=c(-30,30)) +
  labs(title = "Variation of GDP growth per Year",
       y = "GDP growth (%)", x = "Year")

countryName <- "Honduras"
plot1 <- ggplot(df[df$Country.Name==countryName,], aes(x=Year, y=Inflation)) +
  geom_line(stat="Identity") +
  geom_smooth() +
  labs(title = "Variation of Net Migration and Inflation",
       y = "Inflation, consumer prices (annual %)", x = "", subtitle = countryName)

plot2 <- ggplot(df[df$Country.Name==countryName,], aes(x=Year, y=Net.Migration.Ratio)) +
  geom_line(stat="Identity") +
  geom_smooth() +
  labs(y = "Net Migration Rate", x = "Year")

countryName <- "Iraq"
plot3 <- ggplot(df[df$Country.Name==countryName,], aes(x=Year, y=Inflation)) +
  geom_line(stat="Identity") +
  geom_smooth() +
  labs(title = "Variation of Net Migration and Inflation",
       y = "Inflation, consumer prices (annual %)", x = "", subtitle = countryName)

plot4 <- ggplot(df[df$Country.Name==countryName,], aes(x=Year, y=Net.Migration.Ratio)) +
  geom_line(stat="Identity") +
  geom_smooth() +
  labs(y = "Net Migration Rate", x = "Year")

gridExtra::grid.arrange(plot1, plot3, plot2, plot4,nrow = 2)

agg1 <- aggregate(cbind(Net.Migration.Ratio, GDP) ~ HDI+Year+Continent.Code, data=df, FUN=mean)

ggplot(agg1, aes(x=Year, y=Net.Migration.Ratio, color=HDI)) +
  geom_line(stat="identity", lwd=1) +
  # geom_smooth(method=NULL) +
  facet_wrap(~ Continent.Code) +
  labs(title = "Variation of Net Migration per Year",
       subtitle = "Divided according to Continent",
       y = "Net Migration Rate", x = "Year")

ggplot(agg1, aes(x=Year, y=Net.Migration.Ratio, color=Continent.Code)) +
  geom_line(stat="identity", lwd=1)+
  labs(title = "Variation of Net Migration per Year",
       subtitle = "Divided according to HDI",
       y = "Net Migration Rate", x = "Year") +
  facet_wrap(~HDI)

df <- df[df$DALYs<50000,]

agg2 <- aggregate(cbind(Net.Migration.Ratio,DALYs,GDP,Inflation,Healthcare.expenditure,Mortality,Life.Expectancy) ~ HDI+Year, data=df, FUN=mean)
names(agg2)
names(agg2) <- c("HDI", "Year", "Mig", "DALYs", "GDP",
                 "Inflation", "Outofpock", "Mortality", 
                 "LifeExp")

agg2 <- aggregate(cbind(Net.Migration.Ratio) ~ HDI+Year, data=df, FUN=mean)
ggplot(agg2, aes(x=Year, y=Net.Migration.Ratio, color=HDI)) +
  geom_line(stat="identity", lwd=1.2) +
  geom_smooth(linetype=2) +
  labs(title = "Variation of Net Migration per Year",
       subtitle = "Divided according to HDI",
       y = "Net Migration Rate", x = "")

agg2 <- aggregate(cbind(Net.Migration.Ratio,DALYs,GDP,Inflation,Healthcare.expenditure,Mortality,Life.Expectancy,HDI) ~ Continent.Code+Year, data=na.omit(df), FUN=mean)
names(agg2)
names(agg2) <- c("ContinentCode", "Year", "Mig", "DALYs", "GDP",
                 "Inflation", "Outofpock", "Mortality", 
                 "LifeExp", "HDI")
agg2$HDI <- sapply(agg2$HDI, cut, breaks = c(1, 1.75, 2.5, 3.25, 4),
                   labels = c("Low", "Medium", "High", "Very High"))

agg2 <- aggregate(cbind(Net.Migration.Ratio) ~ Continent.Code+Year, data=df, FUN=mean)
ggplot(agg2[,], aes(x=Year, y=Net.Migration.Ratio, color=Continent.Code)) +
  geom_line(stat="identity", lwd=1, alpha=0.5, linetype=1) +
  #facet_wrap(~ Continent.Code) +
  geom_smooth(linetype=2)+
  labs(title = "Variation of Net Migration per Year",
       subtitle = "Divided according to Continent",
       y = "Net Migration Rate", x = "Year")
  
ggplot(agg2, aes(x=agg2$Year, y=agg2$Mortality, color=agg2$ContinentCode)) +
  geom_line(data=df1, linetype=1, lwd=1) + geom_smooth()

gridExtra::grid.arrange(plot1, plot2, nrow = 2)
