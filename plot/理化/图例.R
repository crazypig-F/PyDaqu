library(ggplot2)
source("./plot/font.R")
COLOR <- c("#00529F", "#6DBE45")
data <- data.frame(x = c("A", "B"), y = c(1, 2), color = c("A", "B"))

g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = c("机械曲", "传统曲")) +
  guides(fill = guide_legend(title = "", ncol = 1, byrow = TRUE)) +
  theme(legend.text = element_text(family = "songti", size = 16, color = "black"))
ggsave(filename = "./pdf/phy/legend.pdf", g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
