"""
This scripts compare between two classifications and prints the average Jaccard score.
The classification file MUST be in this form only: a row for each family and genes separated by tabs.
To convert files from profile analysis use this shell command : cut -f 7 INPUT > | sed 's/,/\t/g' > OUTPUT
To run this sctipt:
python compare_classifications.py <CLASSIFICATION1> <CLASSIFICATION2>
"""

import sys
import pandas as pd
from itertools import product


def prep_files(file):
    data = pd.read_csv(file, names=['gene_families'])
    data = data.apply(lambda x: x.str.split("\t"), axis=1)
    data['gene_families'] = data['gene_families'].apply(lambda x: [y.split("|")[1].split(".")[0] for y in x] if "|" in x else x)
    return data

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


def compare_families(file1, file2):
    gene_families_1 = [set(family) for family in file1["gene_families"]]
    gene_families_2 = [set(family) for family in file2["gene_families"]]

    total_similarity, perfect_match, total_weighted_similarity, total_weights = 0, 0, 0, 0

    for set_f1 in gene_families_1:
        max_sim, max_weight = max((jaccard_similarity(set_f1, set_f2), len(set_f1)) for set_f2 in gene_families_2)
        if max_sim == 1:
            perfect_match += 1
        total_similarity += max_sim
        total_weighted_similarity += max_sim * max_weight
        total_weights += max_weight

    average_similarity = total_similarity / len(gene_families_1) if gene_families_1 else 0
    weighted_average_similarity = total_weighted_similarity / total_weights if total_weights != 0 else 0

    print(f"Average Jaccard Similarity: {average_similarity}")
    print(f"Weighted Average Jaccard Similarity: {weighted_average_similarity}")
    print(f"% of Groups that Perfectly Matched {perfect_match / len(gene_families_1) if gene_families_1 else 0}")


if __name__ == '__main__':
    file1 = prep_files(sys.argv[1])
    file2 = prep_files(sys.argv[2])
    compare_families(file1, file2)

