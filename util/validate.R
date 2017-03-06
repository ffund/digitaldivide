library(ggplot2)

houses <- Sys.glob( "consolidate*")
m <- gregexpr('[0-9]+',houses)
houses <- unlist(regmatches(houses, m))

dat <- data.frame(houseID = factor(), type = factor(), trial = integer(), measure = numeric())
truth <- data.frame(houseID = factor(), type = factor(), measure = numeric())

for (house in houses) {
  d <- read.csv( paste("consolidate-", house, ".csv", sep="") )
  d$houseID <- as.integer(house)
  d$measure <- as.numeric(d$measure)
  dat <- rbind(dat, d)

  t <- read.csv( paste("truth-", house, ".csv", sep="") )
  t$houseID <- as.integer(house)
  truth <- rbind(truth, t)
}


dat$houseID <- factor(dat$houseID)
dat <- dat[complete.cases(dat),]
truth$houseID <- factor(truth$houseID)
total <- merge(dat, truth, by=c("houseID", "type"))

library(plyr)
cdata <- ddply(dat, c("houseID","type"), summarise,
               N    = length(houseID),
               median = median(measure, na.rm=TRUE),                                            
               mean = mean(measure, na.rm=TRUE),
               sd   = sd(measure, na.rm=TRUE),
               se   = sd / sqrt(N)
)
ctotal <- merge(cdata, truth, by=c("houseID", "type"))

csum <- ddply(ctotal, c("type", "measure"), summarise,
	per = mean/measure
)

csumsum <- ddply(ctotal, c("type"), summarise,                                  
        mid = (quantile(mean/measure, 0.5, na.rm=TRUE)),
	lower = (quantile(mean/measure, 0.25, na.rm=TRUE)),
        upper = (quantile(mean/measure, 0.75, na.rm=TRUE))                                                                 
)                                                                               

print(csumsum)

print(unique(total$houseID))

# remove extreme (outlier) loss values
#dat <- dat[dat$type!="loss" | (dat$type=="loss" & dat$measure < 5.0), ]

q <- ggplot()
q <- q + geom_boxplot(data=dat, aes(x=houseID, y=measure, group=houseID))
q <- q + geom_point(data=truth, aes(x=houseID, y=measure, group=houseID), colour="red")
q <- q + facet_wrap(~ type, scales="free")
q <- q + theme(axis.text.x = element_text(angle = 90, hjust = 1))
q

r <- ggplot(total)  
r <- r + geom_point(aes(x=measure.y, y=measure.x), alpha=0.2)
r <- r + geom_point(aes(x=measure.y, y=measure.y), colour="red", size=0.5)                   

r <- r + facet_wrap(~ type, scales="free")                                      
r <- r + theme(axis.text.x = element_text(angle = 90, hjust = 1))               
r

down <- ggplot(ctotal[ctotal$type=="dlrate",]) 
down <- down + geom_point(aes(x=measure, y=mean), alpha=0.2)
down <- down + geom_point(aes(x=measure, y=measure), colour="red", size=0.5)      
down <- down + theme(axis.text.x = element_text(angle = 90, hjust = 1))               

down <- ggplot(csum) + facet_wrap(~type, scales="free")                                  
down <- down + geom_point(aes(x=measure, y=per), alpha=0.2)                    
down <- down + theme(axis.text.x = element_text(angle = 90, hjust = 1))         

