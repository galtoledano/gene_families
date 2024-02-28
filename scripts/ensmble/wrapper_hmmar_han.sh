#!/bin/bash
#PBS -S /bin/bash
#PBS -N hmmar_han
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/ensmble/hammer_han.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/ensmble/hammer_han.OUT
#PBS -p 3
#PBS -l select=1:ncpus=16
source ~/.bashrc
hostname
conda activate PorthoMCL
export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families
# variables
species="han"
parent_directory="/groups/itay_mayrose/danielzak/gene_fams/ProfilesUpdated/updProfiles/"
data_path="/groups/itay_mayrose/danielzak/gene_fams/test"
data_base="/groups/itay_mayrose/danielzak/gene_fams/ProfilesUpdated/data_base_profile.hmm"
genome="/groups/itay_mayrose/galtoledano/gene_families/data/genomes/ensmble/$species.fa"
results_path="hmm_profile/$species"
e_value_threshold=0.01
portho_path=/groups/itay_mayrose/galtoledano/gene_families/PorthoMCL
inflation=2

# step 2 - matcing profiles in the genome
bash scripts/hmm_scan.sh $data_path $data_base $genome
# step 3 - convert results formats
python3 scripts/hmm_scan_result.py $data_path/results.txt $genome $results_path $e_value_threshold
# step 4 - run classification on orphans
mkdir $results_path
mkdir $results_path/porthomcl
mkdir $results_path/porthomcl/0.input_faa
cp $results_path/orphans.faa $results_path/porthomcl/0.input_faa/.
cd /groups/itay_mayrose/galtoledano/gene_families/
bash scripts/porthomcl.sh $portho_path $results_path/porthomcl $inflation 
cat $results_path/gene_families.tsv $results_path/porthomcl/genes_families.tsv > $results_path/full_set_gene_families.tsv