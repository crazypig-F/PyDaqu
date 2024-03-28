library(ggplot2)
COLOR <- c("#F8766D", "#00BA38", "#619CFF")
data <- data.frame(x = c("A", "B", "C"), y = c(1, 2, 3), color = c("A", "B", "C"))

g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = c("A", "B", "C")) +
  guides(fill = guide_legend(title = "", ncol = 1, byrow = TRUE)) +
  theme(legend.text = element_text(family = "sans", size = 16, color = "black"))
ggsave(filename = "./pdf/ml/legend_combination.pdf", g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
