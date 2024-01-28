from Bio import SeqIO
import pandas as pd
# E_thr = 0.01

def handle_results(output_file, original_file, original_fasta_file, orphans_file, output_csv_file, E_thr=0.01):
    df = pd.read_csv(output_file, comment='#', header=None, delim_whitespace=True)
    # Extract the target, query, and E-value columns from an --tblout hmmscan file
    selected_columns = [0, 2, 4]
    selected_df = df.iloc[:, selected_columns]
    # Rename the columns - now we have a csv table containing a protein, its best match profile and their e-value
    selected_df.columns = ['Profile', 'Protein', 'E-value']
    unique_proteins = selected_df.drop_duplicates(subset='Protein', keep='first')
    unique_proteins.reset_index(drop=True)
    All_proteins = unique_proteins['Protein'].tolist()
    with open(original_file, 'r') as file:
        orig_prots = [line.strip() for line in file]
    # Find proteins unique to each list
    # unique_to_file = set(orig_prots) - set(All_proteins)
    # unique_to_other = set(All_proteins) - set(orig_prots)
    
    # # do we need pronts? 
    # print(len(unique_to_file))
    # print(len(unique_to_other))
    
    # # Create a new list containing proteins that do not appear in both lists
    # prots_lost = list(unique_to_file.union(unique_to_other))
    # lost_proteins = pd.DataFrame({'Protein': prots_lost})
    # lost_proteins.to_csv('/content/drive/MyDrive/Lab/Family classification project/Ensembl/lostProteins.csv', index=False)

    unique_proteins.loc[unique_proteins['E-value'] > E_thr, 'Profile'] = 'none'

    #drop the e-values, and group the proteins into families according to their profiles.
    df_noE = unique_proteins.copy().drop('E-value', axis=1)
    grouped_df = df_noE.copy().groupby('Profile')['Protein'].apply(list).reset_index(name='Proteins')

    # Create an empty list to store orphan proteins
    orphans = []
    # Iterate over rows in the DataFrame
    for index, row in grouped_df.iterrows():
        proteins = row['Proteins']
        # Check if there is only one protein in the row
        if len(proteins) == 1:
            orphans.append(proteins[0])

    # # Display the list of orphan proteins
    # print("Orphan Proteins:", orphans)
            
    none_group_ids = grouped_df.loc[grouped_df['Profile'] == 'none', 'Proteins'].tolist()[0]
    # print(len(none_group_ids))
    none_group_ids.extend(orphans)
    # print(none_group_ids)
    # len(none_group_ids)

    # Print record IDs from the original FASTA file
    # original_record_ids = [record.id for record in SeqIO.parse(output_file, 'fasta')]
    with open(original_fasta_file, 'r') as original_fasta, open(orphans_file, 'w') as output_fasta:
        for record in SeqIO.parse(original_fasta, 'fasta'):
            if record.id in none_group_ids:
                SeqIO.write(record, output_fasta, 'fasta')

    # print(len(none_group_ids))
    # Filter rows based on the condition
    gene_families = grouped_df[~grouped_df['Proteins'].apply(lambda x: any(item in none_group_ids for item in x))].reset_index()
    gene_families.to_csv(output_csv_file, index=False)
    print("done")

if __name__ == "__main__":
    # hmmer_output='/content/drive/MyDrive/Lab/Family classification project/Ensembl/AthNoVarsResults.txt'
    # original_ensmble='/content/drive/MyDrive/Lab/Family classification project/Ensembl/allProts.txt'
    # orphan='/content/drive/MyDrive/Lab/Family classification project/Ensembl/Orphan_seqsForBlast.fa'
    # output_path='/content/drive/MyDrive/Lab/Family classification project/Ensembl/Gene_families.csv'

    hmmer_output='/groups/itay_mayrose/danielzak/gene_fams/test/results/AthNoVarsResults.txt'
    # how i get to this file format? 
    original_ensmble='/groups/itay_mayrose/danielzak/gene_fams/genomes/allProts.txt'
    original_fasta_file='/groups/itay_mayrose/danielzak/gene_fams/genomes/AthNoVars.fa'
    orphan='hmm_profile/orphans.fa'
    output_path='hmm_profile/gene_families.csv'


    handle_results(hmmer_output, original_ensmble, original_fasta_file, orphan, output_path, 0.01)
