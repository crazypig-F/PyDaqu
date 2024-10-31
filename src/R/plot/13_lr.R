library(ggplot2)
library(ggpmisc)

predict <- read.csv("./data/result/ml/predict value.csv", header = TRUE, row.names = 1, check.names = FALSE)
measure <- read.csv("./data/result/ml/measure value.csv", header = TRUE, row.names = 1, check.names = FALSE)
score_model <- read.csv("./data/result/ml/score model.csv", header = TRUE, row.names = 1, check.names = FALSE)


plot <- function(data, col) {
  model <- lm(data$real ~ data$pred)
  print(summary(model))
  g <- ggplot(data, aes(real, pred)) +
    geom_point(color = "#17C3C8") +
    geom_smooth(method = "lm", color = "#F78179", size = 1) +
    theme_bw() +
    labs(x = "Measured (mg/g)", y = "Predicted (mg/g)", title = substitute(paste(t, " (", R^2, " = ", r, ")"), list(r = score_model[col, 'score'], t = col))
    ) +
    theme(
      panel.border = element_rect(size = 1),
      axis.ticks = element_line(size = 1),
      axis.title = element_text(family = "serif", size = 18, color = "black"),
      axis.text.x = element_text(family = "serif", size = 14, color = "black"),
      axis.text.y = element_text(family = "serif", size = 14, color = "black"),
      plot.title = element_text(family = "serif", size = 14, hjust = 0.5),
    )
  ggsave(filename = paste0("./pdf/ml/lr/", paste0(col, ".pdf")), g, width = 8, height = 7, dpi = 600, units = "cm", device = 'pdf')
}

for (col in colnames(measure)) {
  data <- data.frame(pred = predict[, col], real = measure[, col])
  plot(data, col)
}
