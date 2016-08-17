library(ggplot2)

dat <- read.csv("statespeeds.csv")
names(dat) <- c("x", "state", "speed")

dat$state <- tolower(as.character(dat$state))

states_map <- map_data("state")
q <- ggplot(dat, aes(map_id = state)) + theme_bw(base_size=16) + 
    geom_map(aes(fill = speed), map = states_map) + 
    expand_limits(x = states_map$long, y = states_map$lat)
q <- q +   theme(axis.line = element_line(colour = "black"),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.border = element_blank(),
    panel.background = element_blank()) 
q <- q + theme(axis.title=element_blank(),
        axis.text=element_blank(),
        axis.ticks=element_blank())
q <- q + theme(legend.position="bottom")
q <- q + scale_fill_distiller("Average advertised download rate (Mbps)", palette = "Spectral")
q <- q + guides(fill = guide_colorbar(barwidth = 16, barheight = 2, title.position="top", title.hjust = 0.5))

png("stateSpeedsMap.png", width=800, height=600)
print(q)
dev.off()

pdf("stateSpeedsMap.pdf", width=8, height=6)
print(q)
dev.off()
