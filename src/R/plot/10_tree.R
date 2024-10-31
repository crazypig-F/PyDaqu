library(ggtreeExtra)
library(ggtree)
library(dplyr)
library(ape)
library(phangorn)
library(ggstar)
library(ggplot2)
library(ggnewscale)
test_dna <- read.dna('./data/result/ml/dna.fasta', format = 'fasta')
# 计算序列数据之间的距离矩阵
distance_matrix <- dist.dna(test_dna)
anno <- read.csv("./data/result/ml/fasta_anno.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
# 使用UPGMA算法构建进化树
tree <- upgma(distance_matrix)

g <- ggtree(tree, layout = 'circular', branch.length = 'none') +
  geom_fruit(
    data = anno,
    geom = geom_star,
    mapping = aes(y = node, fill = taxonomy, size = 1, starshape = taxonomy),
    position = "identity",
    starstroke = 0.1
  ) +
  scale_size_continuous(
    guide = "none"
  ) +
  geom_tiplab(hjust = -.2, size = 2.8, color = "#6D6FFF")
ggsave(filename = "./pdf/corr/tree.pdf", g, width = 14, height = 14, dpi = 600, units = "cm", device = 'pdf')
