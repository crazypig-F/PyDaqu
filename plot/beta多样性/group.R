library(ggplot2)
library(tidyverse)
library(ggrepel)
library(vegan)
library(forcats)
COLOR <- c("#FF6F61", "#1E90FF")

plot <- function(micro, phase) {
  data <- read.csv(paste0(paste0("./data/temp/beta/", micro), paste0(paste0("/", phase), ".csv")), header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
  mapping <- read.csv("./data/mapping/chamber/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
  mapping <- mapping[grep(paste0("^", phase), row.names(mapping)),]
  data$Phase <- fct_inorder(mapping$Phase)
  data$Group <- fct_inorder(mapping$Group)
  x_label <- colnames(data)[1]
  y_label <- colnames(data)[2]
  data <- data[, -3]
  colnames(data)[1:2] <- c("V1", "V2")

  g <- ggplot(data = data, aes(x = V1, y = V2, color = Group)) +
    geom_vline(xintercept = 0, lty = "dashed", size = 1) +
    geom_hline(yintercept = 0, lty = "dashed", size = 1) +
    geom_point(size = 2) +
    scale_color_manual(values = COLOR) +
    labs(x = x_label, y = y_label) +
    stat_ellipse(linetype = 2, level = 0.8, size = .8) +
    theme_bw() +
    guides(color = 'none') +
    theme(
      axis.title = element_text(family = "sans", size = 14, color = "black"),
      axis.text = element_text(family = "sans", size = 12, color = "black"),
    )
  ggsave(filename = paste0(paste0("./pdf/beta/", micro), paste0(paste0("/", phase), ".pdf")), g, width = 9, height = 8, dpi = 600, units = "cm", device = 'pdf')
}

plot("bacteria", "A")
plot("bacteria", "B")
plot("bacteria", "C")
plot("bacteria", "D")

plot("fungi", "A")
plot("fungi", "B")
plot("fungi", "C")
plot("fungi", "D")
