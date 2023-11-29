###NMDS分析
#加载包，ape是计算bray距离的包
library(ggplot2)
library(vegan)
library(ape)
otu_raw <- read.csv("./data/temp/microbe/chamber/fungi/all/traditional.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- substr(row.names(otu_raw), 1, 2)
otu.distance <- vegdist(otu_raw)
PCoA <- cmdscale(otu.distance, eig = TRUE)
pc12 <- PCoA$points[, 1:2]
pc <- round(PCoA$eig / sum(PCoA$eig) * 100, digits = 2) #解释度
print(pc)
pc12 <- as.data.frame(pc12)
anosim_result <- anosim(otu.distance, mapping, permutations = 999)

pc12['Anosim'] <- c(anosim_result$statistic, anosim_result$signif)
colnames(pc12) <- c(paste0(paste0("PCoA1 (", pc[1]), "%)"), paste0(paste0("PCoA2(", pc[2]), "%)"), "Anosim")
write.csv(pc12, "./data/temp/beta/fungi/traditional.csv")
