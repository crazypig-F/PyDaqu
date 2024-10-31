import math

import pandas as pd
from Bio import SeqIO

from correlation import mapping_asv_select


def get_dna():
    asv = mapping_asv_select()
    seq_record_list = []
    for seq_record in SeqIO.parse("./data/raw/rep_seqs.fna", "fasta"):
        if ("B_" + seq_record.id) in asv:
            seq_record.id = "B_" + seq_record.id
            seq_record.description = ""
            seq_record_list.append(seq_record)
    SeqIO.write(seq_record_list, "./data/result/ml/dna.fasta", "fasta")


def set_length():
    min_length = math.inf
    seq_record_list = []
    for seq_record in SeqIO.parse("./data/result/ml/dna.fasta", "fasta"):
        if len(seq_record.seq) < min_length:
            min_length = len(seq_record.seq)
        seq_record_list.append(seq_record)

    for seq_record in seq_record_list:
        seq_record.seq = seq_record.seq[:min_length]

    SeqIO.write(seq_record_list, "./data/result/ml/dna.fasta", "fasta")


def fasta_anno():
    asv_mapping = pd.read_csv("./data/result/corr/asv_mapping.csv")
    asv = mapping_asv_select()
    taxonomy = [asv_mapping.loc[asv_mapping['Source'] == i, "taxonomy"].iloc[0] for i in asv]
    anno = pd.DataFrame({"asv": asv, "taxonomy": taxonomy, "node": asv})
    anno.to_csv("./data/result/ml/fasta_anno.csv", index=False)


if __name__ == '__main__':
    get_dna()
    set_length()
    fasta_anno()
