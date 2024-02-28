import pandas as pd
import csv

PLAZA_PATH="/groups/itay_mayrose/galtoledano/gene_families/data/plaza_families/"
ENSMBLE_PATH="/groups/itay_mayrose/galtoledano/gene_families/data/ensmle_families/"
SPECIES=["ath", "nta","gma", "han", "oeu", "osa", "sly"]

def convert_plaza(species):
    data = pd.read_csv(f"{PLAZA_PATH}{species}.csv", sep="\t", names=["family", "gene"])
    dict_data = data.groupby("family")["gene"].apply(list).to_dict()
    with open(f"{PLAZA_PATH}{species}_families.tsv", 'w') as f:
        for _, gene_list in dict_data.items():
            f.write(f"{'\t'.join(gene_list)}\n")


def convert_ensmble(species):
    df = pd.read_csv(f"{ENSMBLE_PATH}{species}.csv")
    df['paralogs'] = df['paralogs'].str.replace("'", "").str.replace('"', '')
    df['paralogs'] = df['paralogs'].apply(lambda x: x.strip("{}").split(", "))
    df['paralogs'] = df['paralogs'].apply(lambda x: '\t'.join(filter(lambda elem: not elem.startswith("ENSRNA"), x)))
    df = df[df["paralogs"] != ""]
    df['paralogs'].to_csv(f"{ENSMBLE_PATH}{species}_families.tsv", sep='\t', index=False, header=False, quoting = csv.QUOTE_NONE, escapechar = ' ')


if __name__ == "__main__":
    for s in SPECIES[2:]:
        convert_ensmble(s)
