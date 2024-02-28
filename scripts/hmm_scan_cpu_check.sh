#!/bin/bash
#PBS -S /bin/bash
#PBS -N 60_hammer
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/cpus/60.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/cpus/60.OUT
#PBS -p 3
#PBS -l nodes=compute-0-203:ncpus=60
hostname
conda activate PorthoMCL
export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families
# variables
cpus=60
species="ath"
data_path="/groups/itay_mayrose/danielzak/gene_fams/test"
data_base="/groups/itay_mayrose/danielzak/gene_fams/ProfilesUpdated/data_base_profile.hmm"
genome="/groups/itay_mayrose/galtoledano/gene_families/data/genomes/ensmble/$species.fa"


# step 2 - matcing profiles in the genome
bash scripts/hmm_scan.sh $data_path $data_base $genome $cpus
