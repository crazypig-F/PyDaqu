library(ggplot2)
library(forcats)
# 创建示例数据框

# 传统
# 0.9761904761904763,0.0291605921759902
# 0.755952380952381, 0.04250850255085029
# 0.9821428571428572, 0.03092947870658708

# 机械
# 0.9940476190476191, 0.010309826235529044
# 0.47023809523809523,0.0425085025508503
# 0.9940476190476191, 0.010309826235529044
data <- data.frame(
  group = fct_inorder(c("DSP", "DSP", "DSP", "DSP", "DSM", "DSM", "DSM", "DSM", "DSA", "DSA", "DSA", "DSA")),
  merit = fct_inorder(c("A", "P", "R", "F", "A", "P", "R", "F", "A", "P", "R", "F")),
  # value = c(0.7342, 0.7560, 0.7496, 0.7161, 0.7976, 0.8105, 0.8071, 0.7794, 0.8941, 0.9064, 0.9052, 0.8922)
  value = c(0.8329, 0.8342, 0.8350, 0.8147, 0.8894, 0.8996, 0.8881, 0.8767, 0.9471, 0.9462, 0.9461, 0.9384)
  # SD = c(2.92, 4.25, 3.09)
  # SD = c(1.03, 4.25, 1.03)
)

# 创建柱状图
g <- ggplot(data, aes(x = merit, y = value, fill = group)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.85), color = "black", alpha = 0.85) +
  # geom_errorbar(aes(ymin = Value - SD, ymax = Value + SD), position = position_dodge(width = 0.8), width = 0.25) +
  geom_text(aes(label = sprintf("%.2f", value)), vjust = -1, hjust = .6, position = position_dodge(width = 0.85), size = 2) +  # 显示标签
  labs(x = "", y = "Accuracy (%)") +
  # scale_y_continuous(limits = c(0.7, 1), breaks = c(0.7, 0.8, 0.9, 1)) +
  coord_cartesian(ylim = c(0.7, 1)) +
  guides(fill = "none") +
  theme_bw() +
  theme(
    axis.title.y = element_text(family = "sans", size = 12, color = "black"),
    axis.text.x = element_text(family = "sans", size = 10, color = "black"),
    axis.text.y = element_text(family = "sans", size = 10, color = "black"),
    legend.text = element_text(family = "sans", color = "black", size = 10),
    panel.grid.major = element_line(color = "transparent"),
    panel.grid.minor = element_line(color = "transparent"),
  )
ggsave(filename = "./pdf/ml/combination_mechanical1.pdf", g, width = 9, height = 8, dpi = 600, units = "cm", device = 'pdf')

