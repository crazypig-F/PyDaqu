library(reshape2)
library(ggplot2)
library(forcats)

data <- read.csv("./data/result/function/amino_ec_value.csv", header = TRUE, encoding = "UTF-8", check.names = FALSE)

data$ec <- fct_inorder(data$ec)
p <- ggplot(data, aes(x = sequence, y = ec, size = abs(value), fill = map_ko)) +
  geom_point(shape = 21, alpha = 0.3, color = "black") +
  scale_size("Value", range = c(1, 12)) +
  theme_bw() +
  theme(
    axis.title = element_text(family = "serif", size = 18, color = "black"),
    axis.text.y = element_text(size = 5, family = "serif", hjust = 0),
    axis.text.x = element_text(size = 8, angle = 45, hjust = 1, vjust = 1, family = "serif"),
    plot.margin = margin(5, 5, 5, 15)
  )
p <- p + xlab(NULL) + ylab(NULL)

ggsave("./pdf/function.pdf", plot = p, width = 15, height = 15, unit = "cm")
