"""
This script normelized blsat score.
In order to run this, the blast file nust be created with the flag : -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen"
"""
import sys
import pandas as pd
import numpy as np

blast6_headers = ["qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore", "qlen", "slen"]

def normalize_score(blast6, weight_param, output_name, bin_size=500):
    blast6_df = pd.read_csv(blast6, sep='\t', names=blast6_headers)
    # calculate Lqh
    blast6_df['length_product'] = blast6_df["qlen"] * blast6_df["slen"]
    # assign hits to equal-sized bins
    n_bins = int(blast6_df.shape[0] / bin_size)
    blast6_df['length_bin'] = pd.qcut(blast6_df['length_product'].rank(method='first'), q=n_bins, labels=False)
    # add normalized score column
    blast6_df['norm_' + weight_param] = 0

    bin_dfs = []
    for lbin in blast6_df['length_bin'].unique():
        bin_df = blast6_df.loc[blast6_df['length_bin'] == lbin].copy()
        # fetch the top 5% hits
        n_top_hits = int(0.05 * bin_df.shape[0])
        bin_df_top = bin_df.nlargest(n_top_hits, weight_param)
        # fit a linear model in log-log space
        bin_df_top['log_length_product'] = np.log10(bin_df_top['length_product'])
        bin_df_top['log_' + weight_param] = np.log10(bin_df_top[weight_param])
        a, b = np.polyfit(bin_df_top['log_length_product'], bin_df_top['log_' + weight_param], 1)
        # normalize scores according to model
        bin_df['norm_' + weight_param] = bin_df[weight_param] / (10 ** b * bin_df['length_product'] ** a)
        # also normalize by q/s coverage
        bin_df['qcov'] = (bin_df['qend'] - bin_df['qstart']) / bin_df['qlen']
        bin_df['scov'] = (bin_df['send'] - bin_df['sstart']) / bin_df['slen']
        bin_df['norm_' + weight_param] = bin_df['norm_' + weight_param] * bin_df['qcov'] * bin_df['scov']

        bin_dfs.append(bin_df)

    res = pd.concat(bin_dfs)
    res.to_csv(output_name, sep='\t',header=False)


if __name__ == '__main__':
    normalize_score(blast6=sys.argv[1], weight_param="bitscore", output_name=sys.argv[2])
