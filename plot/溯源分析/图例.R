library(ggplot2)
library(tidyverse)
library(ggrepel)
library(vegan)
library(forcats)
source("./plot/font.R")
COLOR <- c('#87CEEB', '#8B4513', '#FFA500', '#006400', '#A9A9A9')
data <- data.frame(x = c("A", "B", "C", "D", "E"), y = c(1, 2, 3, 4, 5), color = c("A", "B", "C", "D", "E"))

g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = c("空气", "母曲", "稻草", "小麦", "未知")) +
  guides(fill = guide_legend(title = "", nrow = 1, byrow = TRUE)) +
  theme(legend.text = element_text(family = "songti", color = "black", size = 10))
ggsave(filename = "./pdf/source/legend.pdf", g, width = 20, height = 10, dpi = 600, units = "cm", device = 'pdf')
