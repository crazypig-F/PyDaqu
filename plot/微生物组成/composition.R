library(ggplot2)
library(forcats)
COLOR <- c(
  "#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a",
  "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6",
  "#008080", "#e9967a", "#b15928", "#8dd3c7", "#ffffb3",
  "#b3de69", "#bebada", "#ffed6f", "#bc80bd", "#ff8c00"
)
COLOR_END <- "#9E9E9E"

plot <- function(micro, group, phase) {
  data <- read.csv(paste0(paste0(paste0(paste0("./data/temp/abundance/", micro), "/"), group), ".csv"), header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
  data <- data[grep(paste0("^", phase), data[, 1]),]
  data$Index <- fct_inorder(data$Index)
  data$Column <- fct_inorder(data$Column)
  COLOR <- COLOR[1:nlevels(data$Column) - 1]
  COLOR <- append(COLOR, COLOR_END)
  g <- ggplot(data, aes(x = Index, y = Values, fill = Column)) +
    geom_bar(stat = "identity", width = 0.7) +
    scale_fill_manual(values = COLOR) +
    scale_y_continuous(limits = c(-.1, 100.1), expand = c(0, 0)) +
    scale_x_discrete(expand = c(0, 0)) +
    theme_bw() +
    theme(
      axis.title.y = element_text(family = "sans", size = 18, color = "black"),
      axis.text.x = element_text(family = "sans", color = "black", size = 10, angle = 270, vjust = .5),
      axis.text.y = element_text(family = "sans", size = 16, color = "black"),
    ) +
    guides(fill = 'none') +
    labs(x = "", y = "Relative abundance (%)")
  ggsave(filename = paste0(paste0(paste0(paste0("./pdf/abundance/", micro), "/"), group), paste0("/", paste0(phase, ".pdf"))), g, width = 15, height = 9, dpi = 600, units = "cm", device = 'pdf')
}

# plot("bacteria", "traditional", "A")
# plot("bacteria", "traditional", "B")
# plot("bacteria", "traditional", "C")
# plot("bacteria", "traditional", "D")
# plot("bacteria", "mechanical", "A")
# plot("bacteria", "mechanical", "B")
# plot("bacteria", "mechanical", "C")
# plot("bacteria", "mechanical", "D")

# plot("fungi", "traditional", "A")
# plot("fungi", "traditional", "B")
# plot("fungi", "traditional", "C")
# plot("fungi", "traditional", "D")
# plot("fungi", "mechanical", "A")
# plot("fungi", "mechanical", "B")
plot("fungi", "mechanical", "C")
# plot("fungi", "mechanical", "D")

