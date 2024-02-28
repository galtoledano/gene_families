import compare_classifiactions
import pandas as pd
import matplotlib.pyplot as plt
import json

def edit_row_data_from_plaza(file, output_name):
    data = pd.read_csv(file, sep='\t', names=['family', 'gene'])
    dict_data=data.groupby("family")["gene"].apply(list).to_dict()
    with open(output_name, 'w') as f:
        for item in dict_data.items():
            f.write('\t'.join(map(str, item[1])))
            f.write('\n')

def compate_inflation(species):
    res = {}
    inflation_values=[1.2, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    for i in inflation_values:
        print(f"working on inflation {i}")
        #porthoMCL
        local_classification = f"plaza/{species}/genes_families_{i}.tsv"
        db_classification = f"data/plaza_families/{species}_families.tsv"
        #HMM
        # local_classification=f"hmm_runs_I{i}/full_set_gene_families.tsv"
        # db_classification="data/ensble_families.tsv"
        average_similarity, weighted_average_similarity , perfect = compare_classifiactions.main(local_classification, db_classification)
        res[i] = (average_similarity, weighted_average_similarity, perfect)
    
    with open(f'inflations/inflation_{species}.json', 'w') as json_file:
        json.dump(res, json_file)


def create_figure(species):
    with open(f'inflations/inflation_{species}.json', 'r') as json_file:
        res = json.load(json_file)
    values = [tup[0] for tup in res.values()]
    plt.plot(list(res.keys()), values)
    plt.xlabel("Infltation Values")
    plt.ylabel(f"Average Similarity To Database {species}")
    plt.savefig(f"inflations/inflation_{species}.png")
    plt.close()

    values = [tup[1] for tup in res.values()]
    plt.plot(list(res.keys()), values)
    plt.xlabel("Infltation Values")
    plt.ylabel(f"Weighted Average Similarity To Database {species}")
    plt.savefig(f"inflations/inflation_weighted_{species}.png")


if __name__ == "__main__":
    # edit_row_data_from_plaza("data/plaza.csv", "data/plaza_families.tsv")
    # todo - "c.elegans", "human", "mouse", "zebrafish"
    # for s in ["nta", "oeu", "osa", "sly"]:
    #     compate_inflation(s)
    for s in ["gma", "han"]:
        create_figure(s)
