library(ggplot2)
library(tidyverse)
library(ggrepel)
library(vegan)
library(forcats)

plot <- function(micro) {
  data <- read.csv(paste0(paste0("./data/result/diversity/", micro), " bata.csv"), header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
  data$Phase <- fct_inorder(substring(row.names(data), 1, 2))
  x_label <- colnames(data)[1]
  y_label <- colnames(data)[2]
  data <- data[, -3]
  colnames(data)[1:2] <- c("V1", "V2")
  g <- ggplot(data = data, aes(x = V1, y = V2, color = Phase)) +
    geom_vline(xintercept = 0, lty = "dashed", size = 1) +
    geom_hline(yintercept = 0, lty = "dashed", size = 1) +
    geom_point(size = 2) +
    scale_color_manual(values = COLOR) +
    labs(x = x_label, y = y_label) +
    stat_ellipse(linetype = 2, level = 0.8, size = .8) +
    theme_bw() +
    guides(color = 'none') +
    theme(
      panel.border = element_rect(size = 1),
      axis.ticks = element_line(size = 1),
      axis.title = element_text(family = "serif", size = 18, color = "black"),
      axis.text.x = element_text(family = "serif", size = 14, color = "black"),
      axis.text.y = element_text(family = "serif", size = 14, color = "black"),
    )
  return(g)
}

COLOR <- c("#FF6F61", "#4B0082", "#FF1493", "#1E90FF")
g <- plot("bacteria")
ggsave(filename = "./pdf/beta/bacteria beta.pdf", g, width = 9, height = 8, dpi = 600, units = "cm", device = 'pdf')

g <- plot("fungi")
ggsave(filename = "./pdf/beta/fungi beta.pdf", g, width = 9, height = 8, dpi = 600, units = "cm", device = 'pdf')

