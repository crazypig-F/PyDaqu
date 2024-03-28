library(ropls)
data <- read.csv("./data/temp/microbe/parallel/merge/top/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
mapping <- read.csv("./data/mapping/parallel/complete.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)


plot <- function(patten, stage) {
  data <- data[grep(patten, row.names(data)),]
  mapping <- mapping[grep(patten, row.names(mapping)),]
  X <- data
  Y <- NULL
  for (name in rownames(X)) {
    print(mapping[name, "Group"] == "Traditional")
    if (mapping[name, "Group"] == "Traditional") {
      Y <- append(Y, 0)
    }else {
      Y <- append(Y, 1)
    }
  }
  pdf(paste0(paste0("./pdf/ml/feature/", stage), "_pls.pdf"))
  X.plsda <- opls(x = X, y = Y, orthoI = 0)
  vipVn <- getVipVn(X.plsda)
  vipVn_select <- vipVn[vipVn > 1]    #VIP>1 筛选
  vipVn_select <- data.frame(names(vipVn_select), vipVn_select) #VIP>1 筛选后，并按 VIP 降序排序
  names(vipVn_select)[2] <- 'VIP'
  vipVn_select <- vipVn_select[order(vipVn_select$VIP, decreasing = TRUE),]
  colnames(vipVn_select) <- c("name", "value")
  write.csv(vipVn, paste0(paste0("./data/temp/ml/", stage), "_vip.csv"))
  write.csv(vipVn_select, paste0(paste0("./data/temp/ml/", stage), "_vip_importent.csv"), row.names = FALSE)
  dev.off()
}

plot("^A","RC")
plot("^B","YF")
plot("^C","EF")
plot("^D","CC")

