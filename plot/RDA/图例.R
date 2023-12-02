library(ggplot2)
source("./plot/font.R")
COLOR <- c(
  "#1597A5", "#FFC24B", "#FEB3AE", "#F533AD"
)
data <- data.frame(x = c("A", "B", "C", "D"), y = c(1, 2, 3, 4), color = c("A", "B", "C", "D"))

g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = c("入仓", "一翻", "二翻", "出仓")) +
  guides(fill = guide_legend(title = "", ncol = 1, byrow = TRUE)) +
  theme(legend.text = element_text(family = "songti", color = "black", size = 10))
ggsave(filename = "./pdf/rda/legend.pdf", g, width = 20, height = 8, dpi = 600, units = "cm", device = 'pdf')
