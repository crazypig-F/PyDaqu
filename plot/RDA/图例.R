library(ggplot2)
COLOR <- c(
  "#1597A5", "#FFC24B", "#FEB3AE", "#F533AD"
)
data <- data.frame(x = c("A", "B", "C", "D"), y = c(1, 2, 3, 4), color = c("A", "B", "C", "D"))

g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = c("A", "B", "C", "D")) +
  guides(fill = guide_legend(title = "", ncol = 1, byrow = TRUE))
ggsave(filename = "./pdf/rda/legend.pdf", g, width = 20, height = 8, dpi = 600, units = "cm", device = 'pdf')
