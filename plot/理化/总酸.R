library(ggplot2)
library(forcats)
library(reshape2)
library(forcats)
source("./plot/font.R")
COLOR <- c("#00529F", "#6DBE45")
mean <- read.csv("./data/temp/phy/stage/mean/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
std <- read.csv("./data/temp/phy/stage/std/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/stage/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)

mean$Phase <- fct_inorder(mapping$Phase)
mean$Group <- fct_inorder(mapping$Group)
std$Phase <- fct_inorder(mapping$Phase)
std$Group <- fct_inorder(mapping$Group)
item <- "总酸 (g/100g)"


mean <- mean[, c(item, "Phase", "Group")]
std <- std[, c(item, "Phase", "Group")]
mean["std"] <- std[item]
mean['value'] <- mean[item]

min_val <- min(mean['value'])
max_val <- max(mean['value'])


g <- ggplot(mean, aes(x = Phase, y = value, group = Group, linetype = Group, shape = Group, color = Group)) +
  geom_line(cex = .8) +
  geom_point(size = 3) +
  # 添加误差
  geom_errorbar(aes(ymin = value - std, ymax = value + std), linetype = 1, width = 0.15, size = .5) +
  labs(x = "", y = item) +
  guides(color = "none", shape = "none", linetype = "none") +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 0.5)) +
  scale_color_manual(values = COLOR)+
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
ggsave(filename = "./pdf/phy/总酸.pdf", g, width = 8, height = 7, dpi = 600, units = "cm", device = 'pdf')
