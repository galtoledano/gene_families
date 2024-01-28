#!/bin/bash
# # This code run hmm scan on the profile database

# data_path=$1
# data_base=$2
# genome=$3

data_path="/groups/itay_mayrose/danielz/gene_fams/test/"
data_base="/groups/itay_mayrose/danielz/gene_fams/ProfilesUpdated/updProfiles/data_base_profile.hmm"
genome="/groups/itay_mayrose/danielzak/gene_fams/genomes/AthAvailable.fa"

cd $data_path
hmmscan --cpu 20 --tblout $data_path/results.txt $data_base  $genome
