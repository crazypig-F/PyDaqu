Sys.setlocale(category = 'LC_ALL', locale = 'English_United States.1252')
library(FEAST)
metadata <- Load_metadata(metadata_path = "./metadata_fungi_t.txt")
otus <- Load_CountMatrix(CountMatrix_path = "./out_fungi_t.txt")

FEAST_output <- FEAST(C = otus, metadata = metadata, different_sources_flag = 0, dir_path = "./", outfile = "fungi_tradictional")
