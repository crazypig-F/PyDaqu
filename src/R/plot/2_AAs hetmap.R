library(pheatmap)
library(vegan)
library(ggplot2)
library(psych)

data <- read.csv("./data/result/AAs/AAs mean.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)


g <-
  pheatmap(t(data), scale = "row",
           color = colorRampPalette(c("#063F7B", "white", "#990622"))(8),
           cluster_cols = FALSE,
           cluster_rows = TRUE,
           #fontsize_number = 15,
           border_color = "black",
           #display_numbers = TRUE,         #热图格子中显示相应的数
           number_color = "black",         #字体颜色为黑色
           #fontsize_row =16,                    #字体大小为10
           #fontsize_col =13,                    #字体大小为10
           #number_format = "%.2f" ,
           angle_col = 45,
           fontfamily = "serif",
           gaps_col = c(14, 28, 42)
  )

ggsave(filename = "./pdf/AAs heatmap.pdf", g, width = 25, height = 15, units = "cm", device = "pdf")