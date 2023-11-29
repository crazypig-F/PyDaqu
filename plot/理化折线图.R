library(ggplot2)
library(forcats)
library(reshape2)
library(forcats)
source("./plot/font.R")

mean <- read.csv("./data/temp/phy/stage/mean/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
std <- read.csv("./data/temp/phy/stage/std/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/stage/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)

mean$Phase <- fct_inorder(mapping$Phase)
mean$Group <- fct_inorder(mapping$Group)
std$Phase <- fct_inorder(mapping$Phase)
std$Group <- fct_inorder(mapping$Group)

plot <- function(item) {
  print(item)
  mean <- mean[, c(item, "Phase", "Group")]
  std <- std[, c(item, "Phase", "Group")]
  mean["std"] <- std[item]
  mean['value'] <- mean[item]

  min_val <- min(mean['value'])
  max_val <- max(mean['value'])

  y_min <- min_val * 0.9 - max(mean['std'])
  y_max <- max_val * 1.1 + max(mean['std'])


  g <- ggplot(mean, aes(x = Phase, y = value, group = Group, linetype = Group, shape = Group, color = Group)) +
    geom_line(cex = .8) +
    geom_point(size = 3) +
    # 添加误差
    geom_errorbar(aes(ymin = value - std, ymax = value + std), width = 0.15, size = .8) +
    labs(x = "", y = item) +
    guides(color = "none", shape = "none", linetype = "none") +
    ylim(y_min, y_max) +
    theme_classic() +
    theme(
      axis.title = element_text(family = "songti", size = 12, color = "black"),
      axis.text.x = element_text(family = "songti", color = "black", size = 10),
      axis.text.y = element_text(family = "sans", size = 10, color = "black"),
      legend.text = element_text(family = "songti", size = 10, color = "black"),
      panel.grid.major = element_line(color = "transparent"),
      panel.grid.minor = element_line(color = "transparent"),
      axis.line = element_line(color = "black"),
      axis.ticks = element_line(color = "black")
    )
  ggsave(filename = paste0(paste0("./pdf/phy/", unlist(strsplit(item, "\\("))[1]), ".pdf"), g, width = 10, height = 8, dpi = 600, units = "cm", device = 'pdf')
}

for (item in colnames(mean)[1:6]) {
  plot(item)
}
