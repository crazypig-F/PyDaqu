library(ggpubr)
library(forcats)
library(dplyr)
library(reshape2)

plot <- function(item, ylim_1, ylim_2) {
  data <- data[, c(item, "Phase")]
  data['value'] <- data[item]
  g <- ggplot(data, aes(x = Phase, y = value, fill = Phase)) +
    stat_boxplot(geom = "errorbar", width = 0.15, color = "black") + #由于自带的箱形图没有胡须末端没有短横线，使用误差条的方式补上
    geom_boxplot(size = 0.5, fill = "white", outlier.fill = "white", outlier.color = "white") + #size设置箱线图的边框线和胡须的线宽度，fill设置填充颜色，outlier.fill和outlier.color设置异常点的属性
    geom_jitter(aes(fill = Phase), width = 0.2, shape = 21, size = 2.5) + #设置为向水平方向抖动的散点图，width指定了向水平方向抖动，不改变纵轴的值
    scale_fill_manual(values = COLOR) +  #设置填充的颜色
    scale_color_manual(values = c("black", "black", "black", "black")) + #设置散点图的圆圈的颜色为黑色

    labs(x = "", y = item) +
    scale_color_manual(values = COLOR) +
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

data <- read.csv("./data/result/fermentation parameters/fermentation parameters mean.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
data$Phase <- fct_inorder(substring(row.names(data), 1, 2))
COLOR <- c("#FF6F61", "#4B0082", "#FF1493", "#1E90FF")

g <- plot("Starch (%)", 60, 90)
ggsave(filename = "./pdf/fermentation parameters/Starch.pdf", g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("Reducing sugars (g/100g)", 0, 5)
ggsave(filename = "./pdf/fermentation parameters/Reducing sugars.pdf", g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("Total acids (g/100g)", 0, 0.6)
ggsave(filename = "./pdf/fermentation parameters/Total acids.pdf", g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("Moisture (%)", 0, 50)
ggsave(filename = "./pdf/fermentation parameters/Moisture.pdf", g, width = 10, height = 9, dpi = 600, units = "cm", device = 'pdf')
