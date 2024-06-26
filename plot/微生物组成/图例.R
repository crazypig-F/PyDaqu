library(ggplot2)
library(forcats)

COLOR <- c(
  "#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a",
  "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6",
  "#008080", "#e9967a", "#b15928", "#8dd3c7", "#ffffb3",
  "#b3de69", "#bebada", "#ffed6f", "#bc80bd", "#ff8c00"
)
COLOR_END <- "#9E9E9E"
COLOR <- append(COLOR, COLOR_END)
bacteria <- read.csv("./data/temp/abundance/fungi/traditional.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
Column <- fct_inorder(bacteria$Column)
data <- data.frame(x = rep(1, 21), y = rep(1, 21), color = COLOR)


g <- ggplot(data = data, aes(x = x, y = y, fill = color)) +
  geom_bar(stat = "identity", width = 1) +
  scale_fill_manual(values = COLOR, labels = Column) +
  guides(fill = guide_legend(title = "", ncol = 1, byrow = TRUE)) +
  theme(legend.text = element_text(family = "sans", color = "black", size = 10))
ggsave(filename = "./pdf/abundance/fungi/legend.pdf", g, width = 30, height = 50, dpi = 600, units = "cm", device = 'pdf')
