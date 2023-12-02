import pandas as pd

from analyze.characteristics import NumCharacteristics

df = pd.read_csv("../../data/raw/fungi_filtered.csv", index_col=0)
df = df.iloc[:, :-1].T
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
sinks_sources.T.to_csv("../../data/temp/溯源分析/out_fungi_t.txt", sep='\t')

with open(f"../../data/temp/source/metadata_fungi_t.txt", 'w') as f:
    f.write('SampleID\tEnv\tSourceSink\tid\n')
    for idx, line in enumerate(sinks_sources.index):
        if line[0] == 'A':
            source_sink = "sink"
            sink_id = str(idx + 1)
        else:
            source_sink = '溯源分析'
            sink_id = ''
        f.write(f"{line}\t{line[0]}\t{source_sink}\t{sink_id}\n")
