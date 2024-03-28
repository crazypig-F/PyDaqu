library(vegan)


bacteria <- read.csv("./data/select/大曲细菌OTU.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
bacteria <- bacteria[, -dim(bacteria)[2]]
bacteria <- t(bacteria)
Chao1_b <- estimateR(bacteria)[2,]

#Shannon 指数,通常使用2、e作为底数
Shannon_b <- diversity(bacteria, index = 'shannon', base = 2)


fungi <- read.csv("./data/select/大曲真菌OTU.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
fungi <- fungi[, -dim(fungi)[2]]
fungi <- t(fungi)
Chao1_f <- estimateR(fungi)[2,]

#Shannon 指数,通常使用2、e作为底数
Shannon_f <- diversity(fungi, index = 'shannon', base = 2)

alpha <- data.frame(Chao1_b, Chao1_f, Shannon_b, Shannon_f)
colnames(alpha) <- c("Bacteria Chao1", "Fungi Chao1", "Bacteria Shannon", "Fungi Shannon")
write.csv(alpha, "./data/微生物/alpha.csv")
