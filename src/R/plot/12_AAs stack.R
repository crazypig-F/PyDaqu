library(ggplot2)
library(reshape2)
library(forcats)
COLOR <- c(
  "#1f78b4", "#33a02c", "#e31a1c", "#ff7f00"
)

plot <- function() {
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
      panel.border = element_rect(linewidth = 1),
      axis.ticks = element_line(size = 1),
      axis.title.y = element_text(family = "serif", size = 16, color = "black"),
      axis.text.x = element_text(family = "serif", color = "black", size = 12, angle = 45, vjust = .4, hjust = 0),
      axis.text.y = element_text(family = "serif", size = 12, color = "black"),
      panel.grid.major = element_line(color = "transparent"),
      panel.grid.minor = element_line(color = "transparent"),
    ) +
    guides(fill = 'none') +
    labs(x = "", y = "Amino acid (mg/g)")
  ggsave(filename = './pdf/AAs stack.pdf', g, width = 12, height = 9, dpi = 600, units = "cm", device = 'pdf')
}

amino <- read.csv('./data/result/abundance/AAs.csv', header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
plot()
