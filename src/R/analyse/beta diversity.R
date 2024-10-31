library(ggplot2)
library(vegan)

beta <- function(otu_raw) {
  mapping <- substr(row.names(otu_raw), 1, 2)
  otu.distance <- vegdist(otu_raw)
  PCoA <- cmdscale(otu.distance, eig = TRUE)
  pc12 <- PCoA$points[, 1:2]
  pc <- round(PCoA$eig / sum(PCoA$eig) * 100, digits = 2) #解释度
  pc12 <- as.data.frame(pc12)
  anosim_result <- anosim(otu.distance, mapping, permutations = 999)
  pc12['Anosim'] <- c(anosim_result$statistic, anosim_result$signif)
  colnames(pc12) <- c(paste0(paste0("PCoA1 (", pc[1]), "%)"), paste0(paste0("PCoA2(", pc[2]), "%)"), "Anosim")
  return(pc12)
}


asv_b <- read.csv('./data/result/micro/mean/bacteria asv.csv', header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
asv_f <- read.csv('./data/result/micro/mean/fungi asv.csv', header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
beta_b <- beta(asv_b)
beta_f <- beta(asv_f)
write.csv(beta_b, "./data/result/diversity/bacteria bata.csv")
write.csv(beta_f, "./data/result/diversity/fungi bata.csv")