library(ggplot2)
library(forcats)
source("./plot/font.R")
data <- read.csv("./data/temp/abundance/bacteria/traditional.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
data <- data[grep("^A", data[,1]),]
data$Index <- fct_inorder(data$Index)
data$Column <- fct_inorder(data$Column)
COLOR <- c(
  "#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a",
  "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6",
  "#008080", "#e9967a", "#b15928", "#8dd3c7", "#ffffb3",
  "#b3de69", "#bebada", "#ffed6f", "#bc80bd", "#ff8c00"
)
COLOR_END <- "#9E9E9E"
COLOR <- COLOR[1:nlevels(data$Column) - 1]
COLOR <- append(COLOR, COLOR_END)

g <- ggplot(data, aes(x = Index, y = Values, fill = Column)) +
  geom_bar(stat = "identity", width = 0.7) +
  scale_fill_manual(values = COLOR) +
  scale_y_continuous(limits = c(-.1, 100.1), expand = c(0, 0)) +
  scale_x_discrete(expand = c(0, 0)) +
  theme_bw() +
  theme(
    axis.title.y = element_text(family = "songti", size = 12, color = "black"),
    axis.text.x = element_text(family = "sans", color = "black", size = 10, angle = 270, vjust = .5),
    axis.text.y = element_text(family = "sans", size = 10, color = "black"),
  ) +
  # guides(fill = guide_legend(title = "", ncol = 1, byrow = TRUE)) +
  guides(fill = 'none') +
  labs(x = "", y = "相对丰度 (%)")
ggsave(filename = "./pdf/abundance/bacteria/tradictional/RC.pdf", g, width = 14, height = 8, dpi = 600, units = "cm", device = 'pdf')
