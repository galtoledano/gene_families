import pandas as pd

PATH="/groups/itay_mayrose/galtoledano/gene_families/data/plaza_families/"
SPECIES=["ath", "gma", "han", "nta", "oeu", "osa", "sly"]

def convert_plaza(species):
    data = pd.read_csv(f"{PATH}{species}.csv", sep="\t", names=["family", "gene"])
    dict_data = data.groupby("family")["gene"].apply(list).to_dict()
    with open(f"{PATH}{species}_families.tsv", 'w') as f:
        for _, gene_list in dict_data.items():
            f.write(f"{'\t'.join(gene_list)}\n")

if __name__ == "__main__":
    for s in SPECIES:
        convert_plaza(s)
