library(ggplot2)
library(reshape2)
library(forcats)
COLOR <- c('#87CEEB', '#8B4513', '#FFA500', '#006400', '#A9A9A9')

plot <- function(micro, group) {
  data <- read.table(paste0(paste0("./data/temp/source/", micro), paste0(paste0("_", group), "_source_contributions_matrix.txt")))
  data['Sample'] <- row.names(data)
  data$Sample <- substr(data$Sample, 1, 4)
  data$Sample <- fct_inorder(data$Sample)

  data_melt <- melt(data, id.vars = "Sample")
  names(data_melt) <- c("Sinks", 'Sources', 'Value')
  g <- ggplot(data_melt, aes(x = Sinks, y = Sources, size = Value, color = Sources)) +
    geom_point() +
    labs(x = '', y = '') +
    scale_y_discrete(labels = c("Air", "Muqu", "Straw", "Wheat", "Unknow")) +
    scale_color_manual(values = COLOR) +
    guides(color = 'none', size = 'none') +
    theme_bw() +
    theme(
      axis.text.x = element_text(family = "sans", color = "black", size = 10, angle = 270, vjust = .5),
      axis.text.y = element_text(family = "sans", size = 10, color = "black"),
    )

  ggsave(filename = paste0(paste0("./pdf/source/", micro), paste0(paste0("_", group), "_sources.pdf")), g, width = 10, height = 6, dpi = 600, units = "cm", device = 'pdf')
}


plot("bacteria", "Y")
plot("bacteria", "Z")
plot("fungi", "Y")
plot("fungi", "Z")