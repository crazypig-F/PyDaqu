library(ggplot2)
COLOR <- c("#c01c2d", "#033250")
data <- data.frame(x = c("A", "B"), y = c(1, 2), color = c("A", "B"))

g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = c("M", "T")) +
  guides(fill = guide_legend(title = "", ncol = 1, byrow = TRUE)) +
  theme(legend.text = element_text(family = "sans", size = 16, color = "black"))
ggsave(filename = "./pdf/pathway/amino_legend.pdf", g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
