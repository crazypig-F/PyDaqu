library(ggplot2)
library(forcats)


plot <- function(micro, phase) {
  data <- read.csv(paste0(paste0("./data/result/abundance/", micro), ".csv"), header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
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
      panel.border = element_rect(size = 1),
      axis.ticks = element_line(size = 1),
      axis.title = element_text(family = "serif", size = 18, color = "black"),
      axis.text.x = element_text(family = "serif", size = 14, color = "black", angle = 270),
      axis.text.y = element_text(family = "serif", size = 14, color = "black"),
    ) +
    guides(fill = 'none') +
    labs(x = "", y = "Relative abundance (%)")
  return(g)
}

COLOR <- c(
  "#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a",
  "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6",
  "#008080", "#e9967a", "#b15928", "#8dd3c7", "#ffffb3",
  "#b3de69", "#bebada", "#ffed6f", "#bc80bd", "#ff8c00"
)
COLOR_END <- "#9E9E9E"

g <- plot("bacteria", "RC")
ggsave(filename = "./pdf/abundance/bactrie RC.pdf", g, width = 15, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("bacteria", "YF")
ggsave(filename = "./pdf/abundance/bactrie YF.pdf", g, width = 15, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("bacteria", "EF")
ggsave(filename = "./pdf/abundance/bactrie EF.pdf", g, width = 15, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("bacteria", "CC")
ggsave(filename = "./pdf/abundance/bactrie CC.pdf", g, width = 15, height = 9, dpi = 600, units = "cm", device = 'pdf')


g <- plot("fungi", "RC")
ggsave(filename = "./pdf/abundance/fungi RC.pdf", g, width = 15, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("fungi", "YF")
ggsave(filename = "./pdf/abundance/fungi YF.pdf", g, width = 15, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("fungi", "EF")
ggsave(filename = "./pdf/abundance/fungi EF.pdf", g, width = 15, height = 9, dpi = 600, units = "cm", device = 'pdf')

g <- plot("fungi", "CC")
ggsave(filename = "./pdf/abundance/fungi CC.pdf", g, width = 15, height = 9, dpi = 600, units = "cm", device = 'pdf')

