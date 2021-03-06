library(ggplot2)

file = "..\\..\\out\\corr_stats_final.csv"

data <- read.csv(file, header = TRUE)

data[['numero_exp']] = factor(data[['numero_exp']])

plot <- ggplot(data, aes(x = numero_exp, y = nombre_valeurs_supp), group = 1)
plot <- plot + geom_point(size = 3)
plot <- plot + labs(x = "M�thodes compar�es", y = "Paire de clusters dont corr�lation > 0.5")

plot <- plot + theme_bw() + theme(legend.position=c(0.9, 0.75))

print(plot)

ggsave(file = "..\\..\\out\\results_stats.pdf", width=6, height=4)
