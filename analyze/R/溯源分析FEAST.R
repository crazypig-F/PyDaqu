Sys.setlocale(category = 'LC_ALL', locale = 'English_United States.1252')
library(FEAST)
micro <- "fungi"
group <- "Y"
phase <- "A"

metadata <- Load_metadata(metadata_path = paste0(paste0(paste0(paste0(paste0(paste0("./data/temp/source/metadata_", micro), "_"), group), "_"), phase), ".txt"))
otus <- Load_CountMatrix(CountMatrix_path = paste0(paste0(paste0(paste0(paste0(paste0("./data/temp/source/out_", micro), "_"), group), "_"), phase), ".txt"))

FEAST_output <- FEAST(C = otus, metadata = metadata, different_sources_flag = 0, dir_path = "./data/temp/source", outfile = paste0(paste0(micro, "_"), group))
