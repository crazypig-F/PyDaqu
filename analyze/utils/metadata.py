import pandas as pd

from analyze.characteristics import NumCharacteristics

micro = "bacteria"
process = "Y"
phase = "A"

df = pd.read_csv(f"../../data/raw/{micro}_filtered.csv", index_col=0)
df = df.iloc[:, :-1].T
nct = NumCharacteristics(df)
df = nct.get_mean(save_type="int")
sinks = df.loc[df.index.str.startswith(phase + process), :]
# E:空气，M:母曲，R:稻草，W:小麦
sources_condition = (df.index.str.startswith("E" + process) |
                     df.index.str.startswith("M" + process) |
                     df.index.str.startswith("R" + process) |
                     df.index.str.startswith("W" + process))
sources = df.loc[sources_condition, :]
sinks_sources = pd.concat([sinks, sources])
sinks_sources.T.to_csv(f"../../data/temp/source/out_{micro}_{process}_{phase}.txt", sep='\t')

with open(f"../../data/temp/source/metadata_{micro}_{process}_{phase}.txt", 'w') as f:
    f.write('SampleID\tEnv\tSourceSink\tid\n')
    for idx, line in enumerate(sinks_sources.index):
        if line[0] == phase:
            source_sink = "sink"
            sink_id = str(idx + 1)
        else:
            source_sink = 'source tracker'
            sink_id = ''
        f.write(f"{line}\t{line[0]}\t{source_sink}\t{sink_id}\n")
