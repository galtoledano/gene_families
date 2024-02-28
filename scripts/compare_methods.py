import compare_classifiactions
import pandas as pd
import matplotlib.pyplot as plt
import json

SPECIES=["ath", "gma", "han", "nta", "oeu", "osa", "sly"]

def compate_plaza():
    res = {}
    for s in SPECIES:
        print(f"working on {s}")
        local_classification=f"/groups/itay_mayrose/galtoledano/gene_families/plaza/{s}/genes_families.tsv"
        db_classification=f"/groups/itay_mayrose/galtoledano/gene_families/data/plaza_families/{s}_families.tsv"
        average_similarity, weighted_average_similarity , perfect = compare_classifiactions.main(local_classification, db_classification)
        res[s] = (average_similarity, weighted_average_similarity, perfect)
    
    with open('/groups/itay_mayrose/galtoledano/gene_families/results_and_figures/plaza_values.json', 'w') as json_file:
        json.dump(res, json_file)


def create_figure():
    with open('/groups/itay_mayrose/galtoledano/gene_families/results_and_figures/plaza_values.json', 'r') as json_file:
        res = json.load(json_file)
    values = [tup[0] for tup in res.values()]
    plt.plot(list(res.keys()), values)
    plt.xlabel("Infltation Values")
    plt.ylabel("Average Similarity To Database")
    plt.savefig("/groups/itay_mayrose/galtoledano/gene_families/results_and_figures/plaza_average.png")


if __name__ == "__main__":
    # compate_plaza()
    create_figure()
