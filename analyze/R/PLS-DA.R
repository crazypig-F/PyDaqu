library(ropls)
COLOR <- c("#C82423", "#2878B5", "#7674AC", "#4484B2", "#1C9373")
data <- read.csv("./data/temp/microbe/parallel/merge/top/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/parallel/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
data <- data[grep("^D", row.names(data)),]
mapping <- mapping[grep("^D", row.names(mapping)),]

X <- data
Y <- NULL
for (name in rownames(X)) {
  print(mapping[name, "Group"] == "传统曲")
  if (mapping[name, "Group"] == "传统曲") {
    Y <- append(Y, 0)
  }else {
    Y <- append(Y, 1)
  }
}

pdf("./pdf/ml/process/feature/CC_pls.pdf")
X.plsda <- opls(x = X, y = Y, orthoI = 0)
vipVn <- getVipVn(X.plsda)
vipVn_select <- vipVn[vipVn > 1]    #VIP>1 筛选
vipVn_select <- data.frame(names(vipVn_select), vipVn_select) #VIP>1 筛选后，并按 VIP 降序排序
names(vipVn_select)[2] <- 'VIP'
vipVn_select <- vipVn_select[order(vipVn_select$VIP, decreasing = TRUE),]
colnames(vipVn_select) <- c("name", "value")
write.csv(vipVn, "./data/temp/ml/process/CC_vip.csv")
write.csv(vipVn_select, "./data/temp/ml/process/CC_vip_importent.csv", row.names = FALSE)
dev.off()