import sys
import pandas as pd
from Bio import SeqIO


def manipulate_results(hmmer_results, e_value_threshold):
    df = pd.read_csv(hmmer_results, comment='#', header=None, delim_whitespace=True)
    selected_columns = [0, 2, 4]
    selected_df = df.iloc[:, selected_columns]
    # Rename the columns - now we have a csv table containing a protein, its best match profile and their e-value
    selected_df.columns = ['Profile', 'Protein', 'E-value']
    unique_proteins = selected_df.drop_duplicates(subset='Protein', keep='first')
    unique_proteins.reset_index(drop=True)
    unique_proteins.loc[unique_proteins['E-value'] > e_value_threshold, 'Profile'] = 'none'
    #drop the e-values, and group the proteins into families according to their profiles.
    df_noE = unique_proteins.copy().drop('E-value', axis=1)
    grouped_df = df_noE.copy().groupby('Profile')['Protein'].apply(list).reset_index(name='Proteins')
    return grouped_df


def find_orphans(original_fasta_file, results_path, grouped_df):
    orphans = []
    for _ , row in grouped_df.iterrows():
        proteins = row['Proteins']
        if len(proteins) == 1:
            orphans.append(proteins[0])     

    none_group_ids = grouped_df.loc[grouped_df['Profile'] == 'none', 'Proteins'].tolist()[0]
    none_group_ids.extend(orphans)

    with open(original_fasta_file, 'r') as original_fasta, open(f"{results_path}/orphans.faa", 'w') as output_fasta:
        for record in SeqIO.parse(original_fasta, 'fasta'):
            if record.id in none_group_ids:
                SeqIO.write(record, output_fasta, 'fasta')
    return none_group_ids


def handle_results(hmmer_results, original_fasta_file, results_path, e_value_threshold=0.01):
    # Extract the target, query, and E-value columns from an --tblout hmmscan file
    grouped_df = manipulate_results(hmmer_results, e_value_threshold)

    none_group_ids = find_orphans(original_fasta_file, results_path, grouped_df)

    gene_families = grouped_df[~grouped_df['Proteins'].apply(lambda x: any(item in none_group_ids for item in x))].reset_index()
    gene_families['families'] = gene_families['Proteins'].apply(lambda x: '\t'.join(map(str, x)))
    gene_families['families'].to_csv(f"{results_path}\gene_families.tsv", index=False, sep=',', header=False)


if __name__ == "__main__":
    # hmmer_output='/groups/itay_mayrose/danielz/gene_fams/test/results.txt'
    # original_fasta_file='/groups/itay_mayrose/danielzak/gene_fams/genomes/AthNoVars.fa'
    # e_value_threshold=0.01
    hmmer_output=sys.argv[1]
    original_fasta_file=sys.argv[2]
    results_path=sys.argv[3]
    e_value_threshold=sys.argv[4]

    handle_results(hmmer_output, original_fasta_file, results_path, e_value_threshold)
