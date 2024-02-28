#!/bin/bash
#PBS -S /bin/bash
#PBS -N porthomcl
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/porthomcl_osa.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/porthomcl_osa.OUT
#PBS -p 3
#PBS -l select=1:ncpus=16

source ~/.bashrc
hostname
conda activate PorthoMCL
export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families/
portho_path=/groups/itay_mayrose/galtoledano/gene_families/PorthoMCL
sample_path=/groups/itay_mayrose/galtoledano/gene_families/plaza/osa/
inflation=2

bash scripts/porthomcl.sh $portho_path $sample_path $inflation
