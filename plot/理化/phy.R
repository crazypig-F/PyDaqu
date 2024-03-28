library(ggplot2)
library(forcats)
library(reshape2)
library(forcats)
COLOR <- c("#00529F", "#6DBE45")

fmt_dcimals <- function(decimals = 0) {
  function(x) format(x, nsmall = decimals, scientific = FALSE)
}

mean <- read.csv("./data/temp/phy/stage/mean/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
std <- read.csv("./data/temp/phy/stage/std/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/stage/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)

plot <- function(ylim_1, ylim_2, item, save_name) {
  mean$Phase <- fct_inorder(mapping$Phase)
  mean$Group <- fct_inorder(mapping$Group)
  std$Phase <- fct_inorder(mapping$Phase)
  std$Group <- fct_inorder(mapping$Group)
  mean <- mean[, c(item, "Phase", "Group")]
  std <- std[, c(item, "Phase", "Group")]
  mean["std"] <- std[item]
  mean['value'] <- mean[item]

  g <- ggplot(mean, aes(x = Phase, y = value, group = Group, linetype = Group, shape = Group, color = Group)) +
    geom_line(cex = .8) +
    geom_point(size = 3) +
    # 添加误差
    geom_errorbar(aes(ymin = value - std, ymax = value + std), linetype = 1, width = 0.15, size = .5) +
    labs(x = "", y = item) +
    guides(color = "none", shape = "none", linetype = "none") +
    scale_y_continuous(expand = c(0, 0), limits = c(ylim_1, ylim_2), labels = fmt_dcimals(1)) +
    scale_color_manual(values = COLOR) +
    theme_classic() +
    theme(
      axis.title = element_text(family = "sans", size = 16, color = "black"),
      axis.text.x = element_text(family = "sans", color = "black", size = 14),
      axis.text.y = element_text(family = "sans", size = 14, color = "black"),
      # panel.grid.major = element_line(color = "transparent"),
      # panel.grid.minor = element_line(color = "transparent"),
      axis.line = element_line(color = "black"),
      axis.ticks = element_line(color = "black"),
    )
  ggsave(filename = paste0(paste0("./pdf/phy/新_", save_name), ".pdf"), g, width = 8, height = 7, dpi = 600, units = "cm", device = 'pdf')
}

# 淀粉
plot(60, 80, "Starch (%)", "淀粉")
# 水分
plot(0, 50, "Moisture (%)", "水分")
# 糖化力
plot(-1, 15, "Saccharification power (U/100g)", "糖化力")
# 还原糖
plot(0, 5, "Reducing sugars (g/100g)", "还原糖1")
# 总酸
plot(0, 0.5, "Total acids (g/100g)", "总酸1")
# 总酯
plot(0, 5, "Total esters (g/100g)", "总酯1")