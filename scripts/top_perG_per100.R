### Análise de qualidade dos jogadores da NBA - por jogo e por posse de bola

## O que não falta na NBA é diversidade dentro e fora das quadras. Times rápidos,
## lentos, ataques focados em um jogador, outros mais coletivos. Como podemos
## analisar os atletas da melhor forma possível? É quase um consenso que usando 
## estatísticas por jogo, nossas conclusões provavelmente estarão enviesadas. 
## Atualmente, a principal forma de analisá-los é por dados para cada 100 posses
## de bola (ou por posse de bola, dividindo esses dados por 100). Mas por que? 
## Justamente para não valorizar atletas que estão em times mais rápidos, com 
## mais posses de bola, e portanto mais chances de sucesso em relação aos outros,
## além de assim ser possível analisar com maior precisão o impacto de jogadores
## que possuem uma minutagem menor do que as grandes estrelas. 
## Com isso em mente, criei gráficos com as estatísticas "básicas" de um atleta
## da NBA - Pontos, Rebotes, Assistências, Roubos de bola, Tocos e Bolas de 3
## pontos; relacionando o "score" de cada atleta por jogo e por posse de bola, 
## para podermos identificar as diferenças e porque é necessário essa forma
## diferente ao analisar os mestres da nossa bola laranja.

### Pacotes
library(ggplot2)
library(tidyverse)
library(plotly)

### Funções
hline <- function(y = 0, color = "gray") {
        # produz uma linha horizontal para ser adicionada em uma figura plotly
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
        # produz uma linha vertical para ser adicionada em uma figura plotly
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

### Lendo Dados
# dados por jogo
perG <- data.frame(read.csv("data/importado/players_perG.csv", 
                            encoding = "UTF-8",
                            blank.lines.skip = TRUE))
perG <- head(perG, -1) # pulando última linha
# dados por 100 posses de bola
per100 <- data.frame(read.csv("data/importado/players_per100.csv", 
                              encoding = "UTF-8",
                              blank.lines.skip = TRUE))
per100 <- head(per100, -1)

### Limpando Dados
per100 <- per100 %>% 
        select(-c(Rk, X, Player.additional)) %>%
        filter(MP > 100) %>%
        group_by(Player) %>%
        summarise(
                PTS = mean(PTS),
                TRB = mean(TRB), 
                AST = mean(AST),
                STL = mean(STL),
                BLK = mean(BLK),
                X3P = mean(X3P)
        ) # como alguns jogadores foram trocados no meio da temporada, há mais de
          # uma ocorrência deles no dataset. Então, agrupei por jogador e calculei
          # as médias das estatísticas que iremos analisar
                
perG <- select(perG, -c(Rk, Player.additional)) %>%
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

### Análise dos dados
# juntando os dataframes
joined_stats <- merge(x = perG, y = per100, by = "Player", 
                      all = FALSE, suffixes = c("_G", "_100"))
write.csv(joined_stats, "data/transformado/players_joined.csv")
# Gráfico de dispersão
traducao <- c("Pontos", "Rebotes", "Assistências", "Roubos de bola", "Tocos",
              "Bolas de 3")
cols <- c("PTS", "TRB", "AST", "STL", "BLK", "X3P")

for (i in seq_along(cols)){
        x_idx = paste(cols[i], "_100", sep = "")
        y_idx = paste(cols[i], "_G", sep="")
        trad <- traducao[i]
        
        # criação da figura
        fig <- plot_ly(x=joined_stats[,x_idx], y=joined_stats[,y_idx],
                       type = 'scatter', mode = 'markers', 
                       color = joined_stats[,x_idx],
                       text = ~paste("Player: ", joined_stats$Player),
                       height = 400,
                       width = 400,
        )
        
        # atualizando layout da figura
        fig <- fig %>% layout(paper_bgcolor="black",
                              plot_bgcolor="black",
                              title=paste("<b>", trad, "por jogo X por 100 posses<b>"),
                              xaxis = list(zeroline = FALSE,
                                           title = paste(trad, "por 100 posses")
                              ),
                              yaxis = list(zeroline = FALSE,
                                           title = paste(trad, "por jogo")
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
        # salvando a figura em formato .png
        path = paste("plots/", cols[i], ".png", sep="")
        orca(fig, path)
        
}
