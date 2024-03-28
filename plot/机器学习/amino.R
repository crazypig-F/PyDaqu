library(ggplot2)
library(ggpmisc)

plot <- function(group) {
  predict <- read.csv(paste0(paste0("./data/temp/ml/predict_amino_", group), ".csv"), header = TRUE, row.names = 1, check.names = FALSE)
  real <- read.csv(paste0(paste0("./data/temp/ml/real_amino_", group), ".csv"), header = TRUE, row.names = 1, check.names = FALSE)
  score <- read.csv(paste0(paste0("./data/temp/ml/predict_amino_score_", group), ".csv"), header = TRUE, row.names = 1, check.names = FALSE)

  f <- function(data, col) {
    model <- lm(data$real ~ data$pred)

    s <- as.character(round(score[col,], 2))
    print(summary(model))
    g <- ggplot(data, aes(real, pred)) +
      geom_point(color = "#17C3C8") +
      geom_smooth(method = "lm", color = "#F78179", size = 1) +
      # stat_poly_eq(aes(label = paste(..adj.rr.label.., ..p.value.label.., sep = '~~')), formula = y ~ x, parse = T) + #添加回归方程和调整R方
      stat_poly_eq(aes(label = paste0("R^2==", s)), formula = y ~ x, parse = T) + #添加回归方程和调整R方
      theme_bw() +
      labs(x = "", y = "", title = col) +
      # labs(x = "Measured (mg/g)", y = "Predicted (mg/g)", title = col) +
      theme(
        plot.title = element_text(hjust = 0.5),
        axis.title = element_text(family = "sans", size = 12, color = "black"),
        axis.text = element_text(family = "sans", size = 10, color = "black"),
      )
    ggsave(filename = paste0(paste0("./pdf/ml/amino/", group), paste0(paste0("_", col), ".pdf")), g, width = 6, height = 5, dpi = 600, units = "cm", device = 'pdf')
  }


  for (col in colnames(real)) {
    data <- data.frame(pred = predict[, col], real = real[, col])
    f(data, col)
  }
}

plot("traditional")
plot("mechanical")
