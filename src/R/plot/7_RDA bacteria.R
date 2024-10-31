library(vegan)
library(plyr)
library(gglayer)
library(ggplot2)
library(ggrepel)
library(forcats)
physicochemical <- read.csv("./data/result/fermentation parameters/fermentation parameters mean.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
colnames(physicochemical) <- c("starch", "RS", "TA", "moisture")
bacteria <- read.csv("./data/result/micro/mean/bacteria genus top20.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
bacteria <- bacteria[, -ncol(bacteria)]

uu <- rda(physicochemical, bacteria, scale = T) #RDA分析
ii <- summary(uu)  #查看分析结果
sp <- as.data.frame(ii$species[, 1:2]) #可根据出图结果，对画图数据做一定的放大或缩小，下同
sp$length <- sp$RDA1^2 + sp$RDA2^2
st <- as.data.frame(ii$sites[, 1:2])
yz <- as.data.frame(ii$biplot[, 1:2])
yz$length <- yz$RDA1^2 + yz$RDA2^2
grp <- fct_inorder(c(rep("RC", 14), rep("YF", 14), rep("EF", 14), rep("CC", 14))) #根据样方类型分组，“a”有3个样本，“b”有3个样本……，共16个。注意样本的顺序和个数！
st$grp <- grp
g <- ggplot() +
  geom_point(data = st, aes(RDA1, RDA2, shape = grp, fill = grp), size = 4) +
  scale_shape_manual(values = 21:25) +
  geom_segment(data = sp, aes(x = 0, y = 0, xend = RDA1, yend = RDA2),
               arrow = arrow(angle = 22.5, length = unit(0.35, "cm"),
                             type = "closed"), linetype = 1, size = 0.6, colour = "red") +
  geom_text_repel(data = sp, aes(RDA1, RDA2, label = row.names(sp)), force = T) +
  geom_segment(data = yz, aes(x = 0, y = 0, xend = RDA1, yend = RDA2),
               arrow = arrow(angle = 22.5, length = unit(0.35, "cm"),
                             type = "closed"), linetype = 1, size = 0.6, colour = "#87CEEB") +
  geom_text_repel(data = yz, aes(RDA1, RDA2, label = row.names(yz)), fontface = "italic") +
  labs(x = paste0("RDA 1 (", format(100 * ii$cont[[1]][2, 1], digits = 4), "%)", sep = ""),
       y = paste0("RDA 2 (", format(100 * ii$cont[[1]][2, 2], digits = 4), "%)", sep = "")) +
  geom_hline(yintercept = 0, linetype = 3, size = 1) +
  geom_vline(xintercept = 0, linetype = 3, size = 1) +
  guides(shape = guide_legend(title = NULL), color = guide_legend(title = NULL),
         fill = guide_legend(title = NULL)) +
  theme_bw() +
  theme(
    panel.border = element_rect(size = 1),
    axis.ticks = element_line(size = 1),
    axis.title = element_text(family = "serif", size = 18, color = "black"),
    axis.text.x = element_text(family = "serif", size = 14, color = "black"),
    axis.text.y = element_text(family = "serif", size = 14, color = "black"),
    panel.grid = element_blank()
  )

ggsave(filename = "./pdf/RDA/bacteria.pdf", g, width = 18, height = 15, dpi = 600, units = "cm", device = 'pdf')

