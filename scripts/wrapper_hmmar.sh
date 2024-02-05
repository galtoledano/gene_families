#!/bin/bash
#PBS -S /bin/bash
#PBS -N hmmar
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/hammer.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/hammer.OUT
#PBS -p 3
#PBS -l select=1:ncpus=16
source ~/.bashrc
hostname
#conda activate
#export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families
# variables
parent_directory="/groups/itay_mayrose/danielz/gene_fams/ProfilesUpdated/updProfiles/"
data_path="/groups/itay_mayrose/danielz/gene_fams/test"
data_base="/groups/itay_mayrose/danielz/gene_fams/ProfilesUpdated/updProfiles/data_base_profile.hmm"
genome="/groups/itay_mayrose/danielzak/gene_fams/genomes/AthFullSeqs.fa"
portho_results="/groups/itay_mayrose/galtoledano/gene_families/hmm_runs"
results_path="hmm_profile"
e_value_threshold=0.01
portho_path=/groups/itay_mayrose/galtoledano/gene_families/PorthoMCL
inflation=2

# step 1 - do usualy one time, creating the database
bash scripts/create_profile_db.sh $parent_directory
# step 2 - matcing profiles in the genome
bash scripts/hmm_scan.sh $data_path $data_base $genome
# step 3 - convert results formats
python3 scripts/hmm_scan_result.py $data_path/results.txt $genome $results_path $e_value_threshold
# step 4 - run classification on orphans
mkdir $results_path/porthomcl/0.input_faa
cp $results_path/orphans.faa $results_path/porthomcl/0.input_faa/.
bash scripts/porthomcl.sh "$portho_path" "$results_path" "$inflation" 
cat $results_path/gene_families.tsv $results_path/porthomcl/genes_families.tsv > $results_path/full_set_gene_families.tsv

