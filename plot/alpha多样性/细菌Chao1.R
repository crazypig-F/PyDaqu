library(ggpubr)
library(forcats)
library(dplyr)
library(reshape2)
source("./plot/font.R")
alpha <- read.csv("./data/temp/alpha/parallel/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/parallel/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)

alpha$Phase <- fct_inorder(mapping$Phase)
alpha$Group <- fct_inorder(mapping$Group)
item <- "细菌 Chao1"

alpha <- alpha[, c(item, "Phase", "Group")]
alpha['value'] <- alpha[item]


g <- ggboxplot(alpha, x = "Phase", y = "value", color = "Group", outlier.shape = NA) +
  labs(x = "", y = "", fill = "") +
  guides(fill = 'none') +
  labs(x = "", y = item) +
  scale_color_manual(values = c("#005C66", "#FF530D")) +
  guides(color = "none", shape = "none", linetype = "none") +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 1700)) +
  theme_bw() +
  theme(
    axis.title = element_text(family = "songti", size = 12, color = "black"),
    axis.text.x = element_text(family = "songti", color = "black", size = 10),
    axis.text.y = element_text(family = "sans", size = 10, color = "black"),
    legend.text = element_text(family = "songti", size = 10, color = "black"),
  )

ggsave(filename = "./pdf/alpha/细菌 Chao1.pdf", g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')
