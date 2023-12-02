library(linkET)
library(ggplot2)
library(ggtext)
library(dplyr)
library(corrplot)

merge <- read.csv("./data/temp/microbe/chamber/merge/top/traditional.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
amino <- read.csv("./data/temp/amino/chamber/mean/traditional.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
data <- cbind(merge, amino)

#计算相关性系数及P值：
cor <- correlate(
  data,
  method = "spearman", #pearson", "kendall" or "spearman"
  adjust = TRUE,
  adjust_method = "fdr"
)

corr <- cor$r[colnames(amino), colnames(merge)]
p <- cor$p[colnames(amino), colnames(merge)]

mycol <- colorRampPalette(c("#06a7cd", "white", "#e74a32"), alpha = TRUE)
# mycol2 <- colorRampPalette(c("#0AA1FF", "white", "#F5CC16"), alpha = TRUE)
pdf("./pdf/corr/microbe_amino_traditional.pdf", width = 20, height = 10, family = "sans")
corrplot(corr,
         method = "ellipse",
         col = mycol(100),
         outline = 'grey',
         diag = TRUE,
         tl.cex = 1.5,
         tl.col = 'black',
         # addCoef.col = 'black', #在现有样式中添加相关性系数数字，并指定颜色
         # number.cex = 0.8, #相关性系数数字标签大小)
         p.mat = p,
         sig.level = c(.001, .01, .05),
         insig = "label_sig", #显著性标注样式："pch", "p-value", "blank", "n", "label_sig"
         pch.cex = 1.5, #显著性标记大小
         pch.col = 'black', #显著性标记颜色
         cl.pos = 'n'
)
dev.off()
