#!/bin/bash
#PBS -S /bin/bash
#PBS -N porthomcl_ath
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/plaza/porthomcl_ath.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/plaza/porthomcl_ath.OUT
#PBS -p 3
#PBS -l select=1:ncpus=16
source ~/.bashrc
hostname
conda activate PorthoMCL
export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families/

portho_path=/groups/itay_mayrose/galtoledano/gene_families/PorthoMCL
sample_path=/groups/itay_mayrose/galtoledano/gene_families/plaza/ath/
inflation=2

bash scripts/porthomcl.sh $portho_path $sample_path $inflation


