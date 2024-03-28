library(ggrepel)

plot <- function(micro, item) {
  data <- read.csv(paste0(paste0(paste0(paste0("./data/temp/pathway/MetaCyc_", micro), "_"), item), ".csv"), header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
  # logFC_t <- with(data, mean(abs(log2FC)) + 1 * sd(abs(log2FC)))
  ## 这里使用的是动态阈值，也可以自定义例如logFC=1或2这种静态阈值
  # logFC_t <- round(logFC_t, 3) # 取前三位小数，这步也可以不运行
  x_max <- max(abs(data$log2FC))
  logFC_t <- 1
  data$Change <- factor(ifelse(data$FDR < 0.05 & abs(data$log2FC) > logFC_t,
                               ifelse(data$log2FC > logFC_t, 'UP', 'DOWN'), 'STABLE'), levels = c("UP", "STABLE", "DOWN"))
  data$text <- ifelse(data$FDR < 0.01 & abs(data$log2FC) > 3 * logFC_t, row.names(data), '')
  print(data)
  write.csv(data, paste0(paste0(paste0(paste0("./data/temp/pathway/MetaCyc_select_", micro), "_"), item), ".csv"))
  g <- ggplot(data, aes(x = log2FC, y = -log10(FDR), color = Change)) +
    geom_point(alpha = 1, size = 2) +
    theme_bw(base_size = 12) +
    xlab("Log2(Fold change)") +
    ylab("-Log10(FDR)") +
    xlim(-x_max, x_max) +
    scale_colour_manual(values = c('#D30F0D', 'gray', '#1A5389')) +
    geom_hline(yintercept = -log10(0.05), lty = "dashed", size = 1) +
    geom_vline(xintercept = c(-logFC_t, logFC_t), lty = "dashed", size = 1) +
    # geom_label_repel(data = data, aes(label = label),
    #                  size = 2, box.padding = unit(0.5, "lines"),
    #                  point.padding = unit(0.8, "lines"),
    #                  segment.color = "black",
    #                  show.legend = FALSE, max.overlaps = 10000) +
    guides(color = "none") +
    theme_bw() +
    theme(
      axis.title = element_text(family = "sans", size = 18, color = "black"),
      axis.text = element_text(family = "sans", size = 16, color = "black"),
    )
  # ggsave(filename = paste0(paste0(paste0(paste0("./pdf/pathway/", micro), "_"), item), ".pdf"), g, width = 10, height = 8, dpi = 600, units = "cm", device = 'pdf')
}

plot("bacteria", "RC")
plot("bacteria", "YF")
plot("bacteria", "EF")
plot("bacteria", "CC")
plot("fungi", "RC")
plot("fungi", "YF")
plot("fungi", "EF")
plot("fungi", "CC")