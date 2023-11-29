import pandas as pd

from analyse.statistics.characteristics import NumCharacteristics

df = pd.read_csv("../../data/raw/bacteria_otu_all.csv", index_col=0).T
nct = NumCharacteristics(df)
df = nct.get_mean(save_type="int")
process = "Y"
sinks = df.loc[df.index.str.startswith("A" + process), :]
# E:空气，M:母曲，R:稻草，W:小麦
sources_condition = (df.index.str.startswith("E" + process) |
                     df.index.str.startswith("M" + process) |
                     df.index.str.startswith("R" + process) |
                     df.index.str.startswith("W" + process))
sources = df.loc[sources_condition, :]
sinks_sources = pd.concat([sinks, sources])
sinks_sources.T.iloc[:10000, :].to_csv("../../data/temp/sinks_sources.txt", sep='\t')

with open("../../data/temp/metadata.txt", 'w') as f:
    f.write('SampleID\tEnv\tSourceSink\tid\n')
    for idx, line in enumerate(sinks_sources.index):
        if line[0] == 'A':
            source_sink = "sink"
            sink_id = str(idx+1)
        else:
            source_sink = 'source'
            sink_id = ''
        f.write(f"{line}\t{line[0]}\t{source_sink}\t{sink_id}\n")
