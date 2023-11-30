library(ggplot2)
library(tidyverse)
library(ggrepel)
library(vegan)
library(forcats)
COLOR <- c("#FF1493", "#87CEEB")

data <- read.csv("./data/temp/beta/bacteria/RC.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/chamber/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- mapping[grep("^A", row.names(mapping)),]
data$Phase <- fct_inorder(mapping$Phase)
data$Group <- fct_inorder(mapping$Group)
x_label <- colnames(data)[1]
y_label <- colnames(data)[2]
anosim.statistic <- data$Anosim[1]
anosim.p <- data$Anosim[2]
data <- data[, -3]
colnames(data)[1:2] <- c("V1", "V2")
min_x <- min(data["V1"])
min_y <- min(data["V2"])

g <- ggplot(data = data, aes(x = V1, y = V2, color = Group)) +
  geom_vline(xintercept = 0, lty = "dashed", size = 1) +
  geom_hline(yintercept = 0, lty = "dashed", size = 1) +
  geom_point(size = 2) +
  scale_color_manual(values = COLOR) +
  labs(x = x_label, y = y_label) +
  stat_ellipse(linetype = 2, level = 0.8, size = .8) +
  # annotate("text", x = min_x + 0.2, y = min_y, label = paste0("Anosim: p=",  anosim.p), col = "red", size = 5) +
  theme_bw() +
  # guides(fill = guide_legend(title = "Genus", ncol = 1, byrow = TRUE)) +
  guides(color = 'none') +
  theme(axis.title = element_text(family = "sans", size = 12, color = "black"),
        axis.text = element_text(family = "sans", size = 10, color = "black"),
        legend.title = element_text(family = "sans", size = 12, color = "black"),
        legend.text = element_text(family = "sans", color = "black", size = 10)
  )
ggsave(filename = "./pdf/beta/bacteria/RC.pdf", g, width = 9, height = 8, dpi = 600, units = "cm", device = 'pdf')
