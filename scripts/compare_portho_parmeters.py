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

def compate_inflation():
    res = {}
    inflation_values=[1.2, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    for i in inflation_values:
        print(f"working on inflation {i}")
        #porthoMCL
        # local_classification = f"porthomcl_runs/arabidopsis_I{i}/genes_families.tsv"
        # db_classification = "data/plaza_families.tsv"
        #HMM
        local_classification=f"hmm_runs_I{i}/full_set_gene_families.tsv"
        db_classification="data/ensble_families.tsv"
        average_similarity, weighted_average_similarity , perfect = compare_classifiactions.main(local_classification, db_classification)
        res[i] = (average_similarity, weighted_average_similarity, perfect)
    
    with open('hmm_porhomcl_runs_infation.json', 'w') as json_file:
        json.dump(res, json_file)


def create_figure():
    with open('hmm_porhomcl_runs_infation.json', 'r') as json_file:
        res = json.load(json_file)
    values = [tup[1] for tup in res.values()]
    plt.plot(list(res.keys()), values)
    plt.xlabel("Infltation Values")
    plt.ylabel("Weighted Average Similarity To Database")
    plt.savefig("porthomcl_runs/hmm_inflations_weighted_average.png")


if __name__ == "__main__":
    # edit_row_data_from_plaza("data/plaza.csv", "data/plaza_families.tsv")
    compate_inflation()
    create_figure()
