library(ggplot2)
library(tidyverse)
library(ggrepel)
library(vegan)
library(forcats)
COLOR <- c("#FF6F61", "#1E90FF")
data <- data.frame(x = c("A", "B"), y = c(1, 2), color = c("A", "B"))

g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = c("T", "M")) +
  guides(fill = guide_legend(title = "", ncol = 1, byrow = TRUE)) +
  theme(legend.text = element_text(family = "sans", color = "black", size = 10))
ggsave(filename = "./pdf/beta/process_legend.pdf", g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
