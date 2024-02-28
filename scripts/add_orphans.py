import os
import sys
from Bio import SeqIO

def edit_families_file(families_file, output_path):
    with open(families_file, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            genes = line.strip().split('\t')
            for field in genes:
                gene_name = field.split('|')[-1]
                last_dot_index = gene_name.rfind('.')
                gene_name = gene_name[:last_dot_index] if last_dot_index > -1 else gene_name
                outfile.write(f"{gene_name}\t")
            outfile.write("\n")


def extract_original_gene_names(fasta_file):
    gene_names = set()
    with open(fasta_file, "r") as file:
        for record in SeqIO.parse(file, "fasta"):
            last_dot_index = record.id.rfind('.')
            gene_name = record.id[:last_dot_index] if last_dot_index > -1 else record.id
            gene_names.add(gene_name)
    return gene_names


def extract_families_gene_names(file_path):
    gene_families = set()
    with open(file_path, "r") as file:
        for line in file:
            genes = line.strip().split("\t")
            for gene in genes:
                gene_families.add(gene)
    return gene_families


def add_orphans(original_file, families_file):
    output_path = os.path.dirname(families_file) + os.path.sep + f"genes_families_{families_file.split("_")[-1]}.tsv"
    edit_families_file(families_file, output_path)
    original_gene_names = extract_original_gene_names(original_file)
    families_gene_names = extract_families_gene_names(output_path)
    orphans= original_gene_names ^ families_gene_names
    with open(output_path, "a") as f:
        for gene in orphans:
            f.write(gene + "\n")

if __name__ == "__main__":
    original_file = sys.argv[1]
    families_file = sys.argv[2]
    add_orphans(original_file, families_file)
    # SPECIES=["ath", "gma", "han", "nta", "oeu", "osa", "sly", "c.elegans", "human", "mouse", "zebrafish"]
    # for s in SPECIES:
    #     original_file=f"/groups/itay_mayrose/galtoledano/gene_families/plaza/{s}/0.input_faa/{s}.fasta"
    #     families_file=f"/groups/itay_mayrose/galtoledano/gene_families/plaza/{s}/8.all.par.group"
    #     add_orphans(original_file, families_file)
    # print("DONE")
