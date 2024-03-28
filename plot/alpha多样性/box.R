library(ggpubr)
library(forcats)
library(dplyr)
library(reshape2)
alpha <- read.csv("./data/temp/alpha/parallel/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/parallel/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)

alpha$Phase <- fct_inorder(mapping$Phase)
alpha$Group <- fct_inorder(mapping$Group)

plot <- function(item, ylim_1, ylim_2) {
  alpha <- alpha[, c(item, "Phase", "Group")]
  alpha['value'] <- alpha[item]
  print(alpha)
  g <- ggboxplot(alpha, x = "Phase", y = "value", color = "Group", outlier.shape = NA) +
    labs(x = "", y = "", fill = "") +
    guides(fill = 'none') +
    labs(x = "", y = item) +
    scale_color_manual(values = c("#005C66", "#FF530D")) +
    guides(color = "none", shape = "none", linetype = "none") +
    scale_y_continuous(expand = c(0, 0), limits = c(ylim_1, ylim_2)) +
    theme_bw() +
    theme(
      axis.title = element_text(family = "sans", size = 18, color = "black"),
      axis.text.x = element_text(family = "sans", color = "black", size = 14),
      axis.text.y = element_text(family = "sans", size = 14, color = "black"),
    )
  ggsave(filename = paste0(paste0("./pdf/alpha/", item), "1.pdf"), g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')
}

plot("Bacteria Chao1", 0, 1700)
plot("Fungi Chao1", 0, 350)
plot("Bacteria Shannon", 0, 9)
plot("Fungi Shannon", 0, 7)