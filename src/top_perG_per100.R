### Packages
library(ggplot2)
library(tidyverse)
library(plotly)

### Functions
hline <- function(y = 0, color = "gray") {
        list(
                type = "line",
                x0 = 0,
                x1 = 1,
                xref = "paper",
                y0 = y,
                y1 = y,
                line = list(color = color, dash="dot")
        )
}

vline <- function(x = 0, color = "gray") {
        list(
                type = "line",
                y0 = 0,
                y1 = 1,
                yref = "paper",
                x0 = x,
                x1 = x,
                line = list(color = color, dash="dot")
        )
}

### Reading Data
# per game stats

perG <- data.frame(read.csv("data/breference/raw/players_perG.csv", 
                            encoding = "UTF-8",
                            blank.lines.skip = TRUE))
perG <- head(perG, -1) 
# per 100 poss
per100 <- data.frame(read.csv("data/breference/raw/players_per100.csv", 
                              encoding = "UTF-8",
                              blank.lines.skip = TRUE))
per100 <- head(per100, -1)

### Cleaning Data
per100 <- per100 %>% 
        select(-c(X)) %>%
        filter(MP > 100) %>%
        group_by(Player) %>%
        summarise(
                PTS = mean(PTS),
                TRB = mean(TRB), 
                AST = mean(AST),
                STL = mean(STL),
                BLK = mean(BLK),
                X3P = mean(X3P)
        )
                
perG <- perG %>%
        filter(G > 10) %>%
        group_by(Player) %>%
        summarise(
                PTS = mean(PTS),
                TRB = mean(TRB), 
                AST = mean(AST),
                STL = mean(STL),
                BLK = mean(BLK),
                X3P = mean(X3P)
        )

### Dta Analysis
joined_stats <- merge(x = perG, y = per100, by = "Player", 
                      all = FALSE, suffixes = c("_G", "_100"))
write.csv(joined_stats, "data/breference/refined/players_joined.csv")
traducao <- c("Points", "Rebounds", "Assists", "Steals", "Blocks",
              "3-Pointers")
cols <- c("PTS", "TRB", "AST", "STL", "BLK", "X3P")

for (i in seq_along(cols)){
        x_idx = paste(cols[i], "_100", sep = "")
        y_idx = paste(cols[i], "_G", sep="")
        trad <- traducao[i]
        
        fig <- plot_ly(x=joined_stats[,x_idx], y=joined_stats[,y_idx],
                       type = 'scatter', mode = 'markers', 
                       color = joined_stats[,x_idx],
                       text = ~paste("Player: ", joined_stats$Player),
                       height = 400,
                       width = 400,
        )
        
        fig <- fig %>% layout(paper_bgcolor="black",
                              plot_bgcolor="black",
                              title=paste("<b>", trad, "per Game X per 100<b>"),
                              xaxis = list(zeroline = FALSE,
                                           title = paste(trad, "per 100")
                              ),
                              yaxis = list(zeroline = FALSE,
                                           title = paste(trad, "per Game")
                              ),
                              shapes = list(
                                      hline(median(joined_stats[,y_idx])),
                                      vline(median(joined_stats[,x_idx]))
                                        ),
                              margin = list(t = 50,
                                            b = 60),
                              font = list(color="white")
                        ) %>%
                        hide_colorbar()
        print(fig)
        path = paste("plots/perGame_per100", cols[i], ".png", sep="")
        orca(fig, path)
}
