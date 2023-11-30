library(ggplot2)
library(reshape2)
library(gg.gap)
library(forcats)
source("./plot/font.R")
amino <- read.csv("./data/temp/amino/stage/mean/traditional.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/stage/traditional.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping$Phase <- fct_inorder(mapping$Phase)
amino["Phase"] <- mapping["Phase"]
data <- melt(amino, id = 'Phase')
g <- ggplot(data, aes(x = variable, fill = Phase, y = value)) +
  geom_bar(stat = "identity", position = position_dodge(0.85), width = 1) +
  theme_classic() +
  labs(x = "", y = "氨基酸含量 (mg/g)") +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 6)) +
  scale_fill_manual(values = c("#66c2a5", "#ffb82e", "#4575b4", "#e78ac3")) +
  guides(fill = "none") +
  theme(
    axis.title.y = element_text(family = "songti", size = 12, color = "black"),
    axis.text.x = element_text(family = "sans", size = 10, color = "black", angle = 40, hjust = 0.75),
    axis.text.y = element_text(family = "sans", size = 10, color = "black"),
    legend.text = element_text(family = "sans", color = "black", size = 10),
    panel.grid.major = element_line(color = "transparent"),
    panel.grid.minor = element_line(color = "transparent"),
    axis.line = element_line(color = "black"),
    axis.ticks = element_line(color = "black")
  )

ggsave(filename = "./pdf/amino/traditional.pdf", g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
