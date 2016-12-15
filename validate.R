
houses <- c(10900,9164,243236,11750,12767,8478,1059,27140,10900)

dat <- data.frame(houseID = factor(), type = factor(), trial = integer(), measure = numeric())

for (house in houses) {
  d <- read.csv( paste("consolidate-", house, ".csv", sep="") )
  d$houseID <- as.integer(house)
  dat <- rbind(dat, d)
}

truth <- read.csv("truth.csv")


dat$houseID <- factor(dat$houseID)
truth$houseID <- factor(truth$houseID)

q <- ggplot()
q <- q + geom_boxplot(data=dat, aes(x=houseID, y=measure, group=houseID))
q <- q + geom_point(data=truth, aes(x=houseID, y=measure, group=houseID), colour="red")
q <- q + facet_wrap(~ type, scales="free")
q
