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

if __name__ == "__main__":
    species="sly"
    input_file=f"/groups/itay_mayrose/galtoledano/gene_families/data/genomes/proteome.all_transcripts.{species}.fasta"
    output_file=f"/groups/itay_mayrose/galtoledano/gene_families/plaza/{species}/0.input_faa/{species}.fasta"
    delim="."
    # input_file=sys.argv[1]
    # output_file=sys.argv[2]
    # delim=sys.argv[3]
    filter_longest_variants(input_file, output_file, delim)