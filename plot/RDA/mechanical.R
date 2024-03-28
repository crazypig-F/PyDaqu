library(vegan)
library(ggrepel)
library(ggplot2)
library(forcats)

bacteria <- read.csv("./data/temp/microbe/chamber/merge/top/mechanical.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
physicochemical <- read.csv("./data/temp/phy/chamber/mean/mechanical.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/chamber/mechanical.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)

#根据DCA1的Axis Lengths值进行选择，如果>4.0选CCA；如果在3.0-4.0之间，选RDA和CCA都可以；如果<3.0, 选择RDA分析即可。
print(decorana(bacteria))

RDA <- rda(bacteria, physicochemical, scale = T)
#提取样本得分
df_rda <- data.frame(RDA$CCA$u[, 1:2], rownames(physicochemical))
colnames(df_rda) <- c("RDA1", "RDA2", "Samples")
# 提取物种得分
df_rda_species <- data.frame(RDA$CCA$v[, 1:2])
#提取环境因子得分
df_rda_env <- RDA$CCA$biplot[, 1:2]
df_rda_env <- as.data.frame(df_rda_env)

#计算轴标签数据（=轴特征值/sum(所有轴的特征值)）
RDA1 <- round(RDA$CCA$eig[1] / sum(RDA$CCA$eig) * 100, 2)
RDA2 <- round(RDA$CCA$eig[2] / sum(RDA$CCA$eig) * 100, 2)
df_rda$Group <- fct_inorder(mapping$Phase)
df_rda_env["name"] <- c("starch", "moisture", "SP", "RS", "TA", "TE")
color <- c("#1597A5", "#FFC24B", "#FEB3AE", "#F533AD") #颜色变量

g <- ggplot() +
  geom_point(data = df_rda, aes(x = RDA1, y = RDA2, color = Group), size = 1, shape = 16) +
  # stat_ellipse(data = df_rda,
  #              aes(RDA1, RDA2, color = Group),
  #              level = 0.95,
  #              linetype = 2, linewidth = 1,
  #              show.legend = F) +
  geom_segment(data = df_rda_env, aes(x = 0, y = 0, xend = df_rda_env[, 1], yend = df_rda_env[, 2]),
               color = "#E8252B", linetype = 1, linewidth = .5, arrow = arrow(angle = 35, length = unit(0.3, "cm"))) +
  geom_text_repel(data = df_rda_env,
                  aes(RDA1, RDA2, label = name), size = 3.5,
                  box.padding = 0.2, #字到点的距离
                  point.padding = 0.2, #字到点的距离，点周围的空白宽度
                  min.segment.length = 0.5, #短线段可以省略
                  segment.color = "#E8252B",
                  segment.size = 0.4,
                  force = T,
                  family = "sans",
                  fontface = "bold",
                  color = "#E8252B"
  ) +
  geom_point(data = df_rda_species, aes(RDA1, RDA2), color = "#605399", size = .3) +
  geom_text_repel(data = df_rda_species,
                  aes(RDA1, RDA2, label = rownames(df_rda_species)), size = 2,
                  box.padding = 0.2, #字到点的距离
                  point.padding = 0.2, #字到点的距离，点周围的空白宽度
                  min.segment.length = 0.5, #短线段可以省略
                  segment.color = "#545454",
                  segment.size = 0.4,
                  force = T,
                  fontface = "italic",
                  family = "sans",
                  color = "#2D5C86"
  ) +
  scale_color_manual(values = color) + #点的颜色设置
  scale_fill_manual(values = color) +
  labs(x = paste0("RDA1 (", RDA1, "%)"),
       y = paste0("RDA2 (", RDA2, "%)")) + #将x、y轴标题改为贡献度
  geom_vline(xintercept = 0, lty = "dashed") +
  geom_hline(yintercept = 0, lty = "dashed") +
  theme_bw() +
  theme(
    axis.title = element_text(family = "sans", size = 12, color = "black"),
    axis.text = element_text(family = "sans", size = 10, color = "black"),
    legend.title = element_text(family = "sans", size = 12, color = "black"),
    legend.text = element_text(family = "sans", size = 10, color = "black"),
  ) +
  guides(color = "none")
ggsave(filename = "./pdf/rda/mechanical.pdf", g, width = 9, height = 8, dpi = 600, units = "cm", device = 'pdf')
