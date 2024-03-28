library(ggplot2)
library(forcats)
COLOR <- c('#D30F0D', 'gray', '#1A5389')
data <- data.frame(x = c("A", "B", "C"), y = c(1, 2, 3), color = c("A", "B", "C"))

g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = c("U", "N","D")) +
  guides(fill = guide_legend(title = "", nrow = 1, byrow = TRUE)) +
  theme(legend.text = element_text(family = "sans", color = "black", size = 10))
ggsave(filename = "./pdf/pathway/legend.pdf", g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
