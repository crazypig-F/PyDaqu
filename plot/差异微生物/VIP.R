library(ggplot2)
library(egg) ##控制绘图区大小，以保证标签文字等所占空间不同时，同批图像还是同样大小
library(forcats)

plot <- function(save_name) {
  vip_select <- read.csv(paste0(paste0("./data/temp/ml/", save_name), "_vip_importent.csv"), header = TRUE, encoding = "UTF-8", check.names = FALSE)
  colnames(vip_select) <- c("name", "value")
  # vip_select <- vip_select[order(vip_select$value),]
  # vip_select$name <- fct_inorder(vip_select$name)
  if (save_name == "EF") {
    print(vip_select[1, 'name'])
    vip_select[1, 'name'] <- paste0(vip_select[1, 'name'], "AAAAAA")
  }
  g <- ggplot(vip_select, aes(name, value)) +
    geom_segment(aes(x = name, xend = name, y = 0, yend = value)) +
    geom_point(shape = 21, size = 5, color = '#008000', fill = '#008000') +
    geom_point(aes(1, 2.5), color = 'white') +
    geom_hline(yintercept = 1, linetype = 'dashed') +
    scale_y_continuous(expand = c(0, 0)) +
    labs(x = '', y = 'VIP value') +
    theme_bw() +
    theme(
      axis.title = element_text(family = "sans", size = 16, color = "black"),
      axis.text.x = element_text(family = "sans", color = "black", size = 14, angle = 270, hjust = 0, vjust = 0.5),
      axis.text.y = element_text(family = "sans", size = 14, color = "black"),
      panel.grid.major = element_line(color = "transparent"),
      panel.grid.minor = element_line(color = "transparent"),
      axis.line = element_line(color = "black"),
      axis.ticks = element_line(color = "black")
    )
  ggsave(filename = paste0(paste0("./pdf/ml/feature/", save_name), "_vip.pdf"), g, width = 12, height = 12, dpi = 600, units = "cm", device = 'pdf')
}

plot("RC")
plot("YF")
plot("EF")
plot("CC")