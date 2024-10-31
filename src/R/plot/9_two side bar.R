library(ggplot2)
library(patchwork)
set.seed(123)
data <- read.csv("./data/result/corr/tax_count.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)

p1 <- ggplot(data) +
  geom_bar(aes(x = taxonomy, y = p), stat = "identity", fill = "#E64A19") +
  coord_flip() + #反转x轴和y轴
  scale_y_reverse(expand = expansion(0)) + #颠倒y轴，并将y轴与边框距离缩小为0
  ggtitle("Positive correlation") +
  theme(axis.title = element_blank(), #去除轴标题
        panel.background = element_blank(), #去除背景
        panel.grid = element_line(colour = "lightgrey"), #设置网格线颜色
        axis.text.y = element_text(family = "serif", size = 14, color = "black"),
        panel.border = element_rect(fill = NA, colour = "black", linewidth = 1), #设置背景边框
        plot.title = element_text(size = 12, hjust = 0.5)) #设置主标题字体大小并让标题居中

p2 <- ggplot(data) +
  geom_bar(aes(x = taxonomy, y = n), stat = "identity", fill = "#00BCD4") +
  coord_flip() + #反转x轴和y轴
  scale_y_continuous(expand = expansion(0)) +
  ggtitle("Negative correlation") + #添加主标题
  theme(axis.text.y = element_blank(), #去除y轴刻度文本
        axis.ticks.y = element_blank(), #去除y轴刻度
        axis.title = element_blank(),
        panel.background = element_blank(), #去除背景
        panel.grid = element_line(colour = "lightgrey"), #设置网格线颜色
        panel.border = element_rect(fill = NA, colour = "black", linewidth = 1), #设置背景边框
        plot.title = element_text(size = 12, hjust = 0.5)) #设置主标题字体大小并让标题居中

#合并图片，添加一个脚注释
g <- p1 + p2
ggsave(filename = "./pdf/corr/two size bar.pdf", g, width = 25, height = 20, dpi = 600, units = "cm", device = 'pdf')

