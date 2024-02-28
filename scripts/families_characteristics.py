import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

SPECIES = {"plants": ["ath", "gma", "han", "nta", "oeu", "osa", "sly"], "animal":[ "c.elegans", "human", "mouse", "zebrafish"]}
SPECIES2 = {"plants": ["ath", "gma", "han", "nta", "oeu", "osa", "sly"]}


def count_familes(species):
    with open(f"plaza/{species}/genes_families.tsv", 'r') as file:
        return sum(1 for line in file)
    

def number_of_families():
    data = [{'category': category, 'species': species} for category, species_list in SPECIES.items() for species in species_list]
    df = pd.DataFrame(data)
    df["families"] = df["species"].apply(lambda x: count_familes(x))
    ax=sns.histplot(data=df, x='families', hue='category', element='step', stat='count', common_norm=False, bins=20)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.title("Amount of Families Per Species")
    plt.xlabel("Sum(Families)")
    plt.ylabel("")
    plt.yticks(range(3))
    plt.xticks(range(4000, 16001, 2000))
    plt.tight_layout()
    plt.savefig("results_and_figures/families_sizes.png")

def bar_plot_number_of_families():
    data = [{'category': category, 'species': species} for category, species_list in SPECIES.items() for species in species_list]
    df = pd.DataFrame(data)
    df["families"] = df["species"].apply(lambda x: count_familes(x))
    ax=sns.barplot(data=df, x='species', y='families', hue='category')
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.title("Amount of Families Per Species")
    plt.xticks(rotation=90)
    plt.ylabel("Sum(Families)")
    plt.tight_layout()
    plt.savefig("results_and_figures/bar_plot_families_sizes.png")

def genomesize(species):
    return sum(len(line.strip().split('\t')) for line in open(f"plaza/{species}/genes_families.tsv", 'r'))
        
def normelized_bar_plot_number_of_families():
    data = [{'category': category, 'species': species} for category, species_list in SPECIES.items() for species in species_list]
    df = pd.DataFrame(data)
    df["families"] = df["species"].apply(lambda x: count_familes(x))
    df['genome_size'] = df["species"].apply(lambda x: genomesize(x))
    df['normelized_family'] = df['families'] / df["genome_size"]

    ax=sns.barplot(data=df, x='species', y='normelized_family', hue='category')
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.title("% of Families From the Gnome Per Species")
    plt.xticks(rotation=90)
    # plt.ylabel("Sum(Families)")
    plt.tight_layout()
    plt.savefig("results_and_figures/normelzed_bar_plot_families_sizes.png")


def calculate_percentage_mapped_to_families(file_name):
    with open(file_name, 'r') as file:
        total_genes = mapped_genes = 0
        for line in file:
            genes_in_row = line.strip().split('\t')
            total_genes += len(genes_in_row)
            mapped_genes += 0 if len(genes_in_row) == 1 else len(genes_in_row)         
    if total_genes == 0: return 0  
    return (mapped_genes / total_genes) * 100

def plot_families_genes():
    data = [{'category': category, 'species': species} for category, species_list in SPECIES.items() for species in species_list]
    df = pd.DataFrame(data)
    df["families"] = df["species"].apply(lambda x: calculate_percentage_mapped_to_families(f"plaza/{x}/genes_families.tsv"))
    ax=sns.barplot(data=df, x='species', y='families', hue='category', palette='colorblind')
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    
    plt.title("Genes Mapped Into Families")
    plt.xticks(rotation=90)
    plt.ylabel("% of Genes in families")
    plt.xlabel("")
    plt.tight_layout()
    plt.savefig("results_and_figures/mapped_genes.png")

def plot_orphans():
    data = [{'category': category, 'species': species} for category, species_list in SPECIES.items() for species in species_list]
    df = pd.DataFrame(data)
    df["families"] = df["species"].apply(lambda x: 100-calculate_percentage_mapped_to_families(f"plaza/{x}/genes_families2.tsv"))
    ax=sns.barplot(data=df, x='species', y='families', hue='category', palette='colorblind')
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    
    plt.title("Orpthan in Families")
    plt.xticks(rotation=90)
    plt.ylabel("% of Orphans Genes")
    plt.xlabel("")
    plt.tight_layout()
    plt.savefig("results_and_figures/orphans_nobug.png")


def plot_families_genes_next_to_original():
    data = [{'category': category, 'species': species} for category, species_list in SPECIES2.items() for species in species_list]
    df = pd.DataFrame(data)
    df["plaza"] = df["species"].apply(lambda x: calculate_percentage_mapped_to_families(f"data/plaza_families/{x}_families.tsv"))
    df["porthoMCL"] = df["species"].apply(lambda x: calculate_percentage_mapped_to_families(f"plaza/{x}/genes_families.tsv"))
    print(df)
    df_melted = pd.melt(df, id_vars=['category', 'species'], value_vars=['plaza', 'porthoMCL'], var_name='method', value_name='percentage')
    ax = sns.barplot(data=df_melted, x='species', y='percentage', hue='method', palette={'plaza': sns.color_palette()[4], 'porthoMCL': sns.color_palette()[0]})
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1)) 
    plt.title("Genes Mapped Into Families With Plaza and PrthoMCL")
    plt.ylabel("% of Genes in families")
    plt.tight_layout()
    plt.savefig("results_and_figures/mapped_genes_plaza_vs_portho.png")

def count_family_sizes(s):
    with open(f"plaza/{s}/genes_families.tsv", 'r') as file:
        family_sizes = [len(line.strip().split('\t')) for line in file]
    return family_sizes


def plot_family_size_histogram(s):
    family_sizes = count_family_sizes(s)
    plt.hist(family_sizes, edgecolor='black', bins=50)
    plt.xlabel('Family Size')
    plt.ylabel('')
    plt.title(f'Histogram of Gene Family Size in {s}')
    plt.tight_layout()
    plt.savefig(f"results_and_figures/family_sizes_histograms/{s}_family_size.png")
    plt.close()

def plot_family_sizes_box_plot():
    data = [{'category': category, 'species': species} for category, species_list in SPECIES.items() for species in species_list]
    df = pd.DataFrame(data)
    df["families_count"] = df["species"].apply(lambda x: count_family_sizes(x))
    print(df)
    df_melted = df.explode('families_count')
    ax=sns.boxplot(x='species', y='families_count', data=df_melted, hue='category', palette='colorblind', fliersize=3)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.xticks(rotation=90)
    plt.title("Box Plot Families Sizes In Species Zoomed In")
    plt.ylabel("")
    plt.ylim(0, 10) 
    plt.tight_layout()
    plt.savefig(f"results_and_figures/box_plot_family_sizes_zoom_in.png")
    plt.close()

if __name__ == '__main__':
    # plot_families_genes()
    # bar_plot_number_of_families()
    # normelized_bar_plot_number_of_families()
    # plot_families_genes_next_to_original()
    # plot_family_size_histogram("nta")
    # for s in SPECIES['plants']:
    #     plot_family_size_histogram(s)
    # for s in SPECIES['animal']:
    #     plot_family_size_histogram(s)
    # plot_family_sizes_box_plot()
    plot_families_genes_next_to_original()
    # plot_orphans()
    # print(genomesize("ath"))
    