library(ggplot2)

plot <- function(group) {
  data <- read.csv(paste0(paste0("./data/temp/pathway/", group), ".csv"), header = TRUE, encoding = "UTF-8", check.names = FALSE)
  colnames(data) <- c("Pathway", "Value")
  g <- ggplot(data, aes(x = Value, y = reorder(Pathway, Value))) +
    geom_point(size = 6, pch = 21, fill = "#9ACD32", color = "#9ACD32") +
    geom_segment(aes(yend = Pathway), xend = 0, size = 3, color = "#9ACD32") +
    theme_classic() +
    labs(x = "Number of genes", y = "") +
    theme(
      axis.title.y = element_text(family = "sans", size = 12, color = "black"),
      axis.text.x = element_text(family = "sans", size = 10, color = "black", angle = 40, hjust = 0.75),
      axis.text.y = element_text(family = "sans", size = 10, color = "black"),
      legend.text = element_text(family = "sans", color = "black", size = 10),
      panel.grid.major = element_line(color = "transparent"),
      panel.grid.minor = element_line(color = "transparent"),
      axis.line = element_line(color = "black"),
      axis.ticks = element_line(color = "black")
    )
  ggsave(filename = paste0(paste0("./pdf/pathway/", group), ".pdf"), g, width = 20, height = 8, dpi = 600, units = "cm", device = 'pdf')
}

plot("traditional")
plot("mechanical")

