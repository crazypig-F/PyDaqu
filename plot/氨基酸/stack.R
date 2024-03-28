library(ggplot2)
library(reshape2)
library(gg.gap)
library(forcats)
COLOR <- c(
  "#1f78b4", "#33a02c", "#e31a1c", "#ff7f00"
)

plot <- function(group) {
  amino <- read.csv(paste0(paste0("./data/temp/abundance/amino/", group), ".csv"), header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
  amino$Index <- fct_inorder(amino$Index)
  amino$Column <- fct_inorder(amino$Column)
  g <- ggplot(amino, aes(x = Index, y = Values, fill = Column)) +
    # geom_bar(stat = "identity", width = 0.7) +
    geom_bar(stat = 'identity', position = 'dodge') +
    scale_fill_manual(values = COLOR) +
    scale_y_continuous(limits = c(0, 6), expand = c(0, 0)) +
    scale_x_discrete(expand = c(0.03, 0)) +
    theme_bw() +
    theme(
      axis.title.y = element_text(family = "sans", size = 12, color = "black"),
      axis.text.x = element_text(family = "sans", color = "black", size = 10, angle = 270, vjust = .5, hjust = -.1),
      axis.text.y = element_text(family = "sans", size = 10, color = "black"),
      panel.grid.major = element_line(color = "transparent"),
      panel.grid.minor = element_line(color = "transparent"),
    ) +
    guides(fill = 'none') +
    labs(x = "", y = "Amino acid (mg/g)")
  ggsave(filename = paste0(paste0("./pdf/amino/stack/", group), ".pdf"), g, width = 12, height = 8, dpi = 600, units = "cm", device = 'pdf')
}

plot("traditional")
plot("mechanical")