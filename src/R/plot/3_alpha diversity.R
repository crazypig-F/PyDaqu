library(ggpubr)
library(forcats)
library(dplyr)
library(reshape2)

plot <- function(item, ylim_1, ylim_2) {
  data <- alpha[, c(item, "Phase")]
  data['value'] <- data[item]
  g <- ggviolin(data, x="Phase", y="value", fill = "Phase", add = "boxplot", add.params = list(fill = "white"))+
    labs(x = "", y = item) +
    guides(color = "none", shape = "none", linetype = "none", fill = 'none') +
    scale_y_continuous(expand = c(0, 0), limits = c(ylim_1, ylim_2)) +
    theme_bw() +
    theme(
      panel.border = element_rect(size = 1),
      axis.ticks = element_line(size = 1),
      axis.title = element_text(family = "serif", size = 18, color = "black"),
      axis.text.x = element_text(family = "serif", size = 14, color = "black"),
      axis.text.y = element_text(family = "serif", size = 14, color = "black"),
    )
  return(g)
}

alpha <- read.csv("./data/result/diversity/alpha.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
alpha$Phase <- fct_inorder(substring(row.names(alpha), 1, 2))

g <- plot("Bacteria Chao1", 0, 650)
ggsave(filename = "./pdf/alpha/Bacteria Chao1.pdf", g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("Fungi Chao1", -10, 250)
ggsave(filename = "./pdf/alpha/Fungi Chao1.pdf", g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("Bacteria Shannon", -.5, 8.5)
ggsave(filename = "./pdf/alpha/Bacteria Shannon.pdf", g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("Fungi Shannon", -1.8, 7.5)
ggsave(filename = "./pdf/alpha/Fungi Shannon.pdf", g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')
