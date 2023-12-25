library(ggplot2)
library(reshape2)
library(gg.gap)
library(forcats)
source("./plot/font.R")
amino <- read.csv("./data/temp/abundance/amino/traditional.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
amino$Index <- fct_inorder(amino$Index)
amino$Column <- fct_inorder(amino$Column)
COLOR <- c(
   "#1f78b4", "#33a02c", "#e31a1c", "#ff7f00"
)

g <- ggplot(amino, aes(x = Index, y = Values, fill = Column)) +
  geom_bar(stat = "identity", width = 0.7) +
  scale_fill_manual(values = COLOR) +
  scale_y_continuous(limits = c(0, 14), expand = c(0, 0), breaks = c(0, 2.5, 5, 7.5, 10, 12.5, 15)) +
  scale_x_discrete(expand = c(0.03, 0)) +
  theme_bw() +
  theme(
    axis.title.y = element_text(family = "songti", size = 12, color = "black"),
    axis.text.x = element_text(family = "sans", color = "black", size = 10, angle = 270, vjust = .5, hjust = -.1),
    axis.text.y = element_text(family = "sans", size = 10, color = "black"),
    panel.grid.major = element_line(color = "transparent"),
    panel.grid.minor = element_line(color = "transparent"),
  ) +
  # guides(fill = guide_legend(title = "", ncol = 1, byrow = TRUE)) +
  guides(fill = 'none') +
  labs(x = "", y = "氨基酸含量(mg/g)")

ggsave(filename = "./pdf/amino/stack/tradictional.pdf", g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
