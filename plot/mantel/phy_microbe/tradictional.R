library(ggplot2)
library(tidyverse)
library(vegan)
library(ggcor)
library(dplyr)
library(scales)
source("./plot/font.R")
M <- read.csv("./data/temp/microbe/chamber/merge/top/traditional.csv", header = TRUE, row.names = 1, check.names = FALSE)
P <- read.csv("./data/temp/phy/chamber/mean/traditional.csv", header = TRUE, row.names = 1, check.names = FALSE)
colnames(P) <- c("淀粉含量", "水分", "糖化力", "还原糖含量", "总酸", "总酯")
M <- M[, which(colSums(M) > 0)]
P <- P[, which(colSums(P) > 0)]

mantel <- mantel_test(M, P, spec.select = list(
  "细菌群落" = 1:20,
  "真菌群落" = 21:40
)) %>%
  mutate(
    rd = cut(
      r,
      breaks = c(-Inf, 0.2, 0.4, Inf),
      labels = c("< 0.2", "0.2 - 0.4", ">= 0.4")
    ),
    pd = cut(
      p.value,
      breaks = c(-Inf, 0.01, 0.05, Inf),
      labels = c("< 0.01", "0.01 - 0.05", ">= 0.05")
    )
  )

g <-
  quickcor(P, type = "upper") +
    geom_square() +
    anno_link(aes(colour = pd, size = rd), data = mantel) +
    scale_fill_gradientn(colours = c('#CC1118', 'white', '#024690'), limits = c(-1, 1)) +
    scale_size_manual(values = c("< 0.2" = 0.5, "0.2 - 0.4" = 1, ">= 0.4" = 2)) +
    scale_colour_manual(values = c("< 0.01" = "#D95F02", "0.01 - 0.05" = "#1B9E77", ">= 0.05" = "#A2A2A288")) +
    guides(
      size = guide_legend(
        title = "Mantel's r",
        override.aes = list(colour = "grey35"),
        order = 2
      ),
      colour = guide_legend(
        title = "Mantel's p",
        override.aes = list(size = 3),
        order = 1,
      ),
      fill = guide_colorbar(title = "Pearson's r", order = 3,)
    )
ggsave(filename = "./pdf/mantel/phy_microbe/tradictional.pdf", g, width = 20, height = 18, dpi = 600, units = "cm", device = 'pdf')
