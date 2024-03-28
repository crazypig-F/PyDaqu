# 导入所需的包
library(ggplot2)
library(ggsignif)

plot <- function(stage, ymin, ymax) {
  data <- read.csv(paste0(paste0("./data/temp/pathway/pathway_amino_acid_", stage), ".csv"), header = TRUE, encoding = "UTF-8", check.names = FALSE)
  COLOR <- c("#c01c2d", "#033250")

  # 开始画图
  g <- ggplot(data = data, aes(x = name, y = mean, fill = group)) +   # x，y轴数据，分组条形图下将其他离散数据传给fill
    scale_y_continuous(limits = c(ymin, ymax), expand = c(0, 0)) +
    labs(x = '', y = 'KEGG', fill = '') +  # x，y和图例标签
    geom_col(position = 'dodge', width = 0.7) +  # 分组条形组时，position = 'dodge'
    scale_fill_manual(values = COLOR) +
    guides(fill = "none") +
    # geom_errorbar(aes(x = name, ymin = mean - std, ymax = mean + std), position = position_dodge(0.5), linetype = 1, width = 0.25, size = .5) +
    theme_classic() +
    theme(
      plot.title = element_text(hjust = 0.5),
      axis.title = element_text(family = "sans", size = 12, color = "black"),
      axis.text.x = element_text(family = "sans", size = 10, color = "black", angle = 45, hjust = 1),
      axis.text.y = element_text(family = "sans", size = 10, color = "black"),
    )
  # geom_signif(y_position = c(447), xmin = c(1.88), xmax = c(2.12),  # 设置显著性说明，y_position是误差线所在y轴位置，xmin和xmax是误差线在x轴位置，可传入多个值
  #             annotation = c("*"), tip_length = 0.1, size = 0.8, textsize = 7,  # 显著性标识；显著性括号下延长度；大小设置；字体大小
  #             vjust = 0.3)  # 调整显著性标识和显著性括号之间的距离

  ggsave(filename = paste0(paste0("./pdf/pathway/pathway_amino_acid_test", stage), ".pdf"), g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
}

plot("RC", 0, 1000)
plot("YF", 0, 1000)
plot("EF", 0, 1000)
plot("CC", 0, 1000)