import sys
from Bio import SeqIO

def filter_longest_variants(input_fasta, output_fasta, delim):
    records = list(SeqIO.parse(input_fasta, "fasta"))
    # Group records by sequence ID
    print(len(records))
    grouped_records = {}
    for record in records:
        seq_id = record.id.split(delim)[0]
        if seq_id not in grouped_records or len(record.seq) > len(grouped_records[seq_id].seq):
            if str(record.seq).endswith("*"):
                record.seq = record.seq[:-1]
            grouped_records[seq_id] = record
    # Write the longest variants to the output file
            
    with open(output_fasta, "w") as output_handle:
        SeqIO.write(grouped_records.values(), output_handle, "fasta")
    print(len(grouped_records))

def check_variants(fasta_file):
    sequence_ids = []
    with open(fasta_file, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            sequence_ids.append(record.id.split(".")[0])

    print(f'total variants {len(sequence_ids)}, number of genes {len(set(sequence_ids))}')



def remove_unavilable(input_file, available_output_file, unavailable_sequence):
    count=0
    with open(available_output_file, 'w') as available_outfile:
        for record in SeqIO.parse(input_file, 'fasta'):
            if str(record.seq) != unavailable_sequence:
                SeqIO.write(record, available_outfile, 'fasta')
                count += 1
    print(f"number of avilable: {count}")


if __name__ == "__main__":
    # input_file=sys.argv[1]
    # output_file=sys.argv[2]
    # delim=sys.argv[3]
    # ensmble=sys.argv[4]
    ensmble=True
    # s=["ath", "han", "gma", "oeu", "osa", "sly"]
    s=["human", "mouse", "zebrafish"]
    for species in s:
        input_file=f"/groups/itay_mayrose/galtoledano/gene_families/data/genomes/ensmble/original/{species}.fasta"
        filter_output_file=f"/groups/itay_mayrose/galtoledano/gene_families/data/genomes/ensmble/filter/{species}.fa"
        available_output_file = f"/groups/itay_mayrose/galtoledano/gene_families/data/genomes/ensmble/{species}.faa"
        unavailable_sequence = "Sequenceunavailable"
        filter_longest_variants(input_file, filter_output_file, ".")
        if ensmble:
            remove_unavilable(filter_output_file, available_output_file, unavailable_sequence)
    