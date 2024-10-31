library(linkET)
library(ggplot2)
library(ggtext)
library(dplyr)
library(RColorBrewer)
library(cols4all)
library(tidyverse)

bacteria <- read.csv("./data/result/micro/mean/bacteria genus top20.csv", header = TRUE, row.names = 1, check.names = FALSE)
bacteria <- bacteria[, -ncol(bacteria)]
fungi <- read.csv("./data/result/micro/mean/fungi genus top20.csv", header = TRUE, row.names = 1, check.names = FALSE)
fungi <- fungi[, -ncol(fungi)]
M <- cbind(bacteria, fungi)

P <- read.csv("./data/result/fermentation parameters/fermentation parameters mean.csv", header = TRUE, row.names = 1, check.names = FALSE)
colnames(P) <- c("Starch", "RS", "TA", "Moisture")
M <- M[, which(colSums(M) > 0)]
P <- P[, which(colSums(P) > 0)]


cor2 <- correlate(P)
corr2 <- cor2 %>% as_md_tbl()
#mantel test
mantel <- mantel_test(M, P,
                      mantel_fun = 'mantel', #支持4种："mantel"使用vegan::mantel()；"mantel.randtest"使用ade4::mantel.randtest()；"mantel.rtest"使用ade4::mantel.rtest()；"mantel.partial"使用vegan::mantel.partial()
                      spec_select = list(bacieria = 1:20,
                                         fungi = 21:40
                      )) #这里分组为随机指定，具体实操需按自己的实际数据分组


#对mantel的r和P值重新赋值（设置绘图标签）：
mantel2 <- mantel %>%
  mutate(r = cut(r, breaks = c(-Inf, 0.25, 0.5, Inf),
                 labels = c("<0.25", "0.25-0.5", ">=0.5")),
         p = cut(p, breaks = c(-Inf, 0.001, 0.01, 0.05, Inf),
                 labels = c("<0.001", "0.001-0.01", "0.01-0.05", ">= 0.05")))

p4 <- qcorrplot(cor2,
                grid_col = "#00468BFF","white", "#42B540FF",
                grid_size = 0.2,
                type = "upper",
                diag = FALSE) +
  geom_square() +
  scale_fill_gradientn(colours = c("#00468BFF",
                                   "white", "#42B540FF"),
                       limits = c(-1, 1))


#添加显著性标签：
p5 <- p4 +
  geom_mark(size = 4,
            only_mark = T,
            sig_level = c(0.05, 0.01, 0.001),
            sig_thres = 0.05,
            colour = 'white')
#在相关性热图上添加mantel连线：
p6 <- p5 +
  geom_couple(data = mantel2,
              aes(colour = p, size = r),
              curvature = nice_curvature())
#继续美化连线：
p7 <- p6 +
  scale_size_manual(values = c(1, 2, 3)) + #连线粗细
  scale_colour_manual(values = c4a('brewer.set2', 4)) + #连线配色
  #修改图例：
  guides(size = guide_legend(title = "Mantel's r",
                             override.aes = list(colour = "grey35"),
                             order = 2),
         colour = guide_legend(title = "Mantel's p",
                               override.aes = list(size = 5),
                               order = 1),
         fill = guide_colorbar(title = "Pearson's r", order = 3)) +
  theme(
    text = element_text(size = 16, family = "serif"),
    plot.title = element_text(size = 16, colour = "black", hjust = 0.5),
    legend.title = element_text(color = "black", size = 16),
    legend.text = element_text(color = "black", size = 16),
    axis.text.y = element_text(size = 16, color = "black", vjust = 0.5, hjust = 1, angle = 0),
    axis.text.x = element_text(size = 16, color = "black", vjust = 0.5, hjust = 0.5, angle = 0)
  )
ggsave(filename = "./pdf/mantel test.pdf", p7, width = 20, height = 15, dpi = 600, units = "cm", device = 'pdf')


