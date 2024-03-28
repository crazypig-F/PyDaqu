library(ggplot2)
library(forcats)
COLOR <- c("#005C66", "#FF530D")
data <- data.frame(x = c("A", "B"), y = c(1, 2), color = c("A", "B"))

g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = c("T", "M")) +
  guides(fill = guide_legend(title = "", nrow = 1, byrow = TRUE)) +
  theme(legend.text = element_text(family = "sans", color = "black", size = 10))
ggsave(filename = "./pdf/alpha/legend.pdf", g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
