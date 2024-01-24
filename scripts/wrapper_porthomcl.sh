#!/bin/bash
#PBS -S /bin/bash
#PBS -N porthomcl
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/porthomcl.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/porthomcl.OUT
#PBS -p 3
#PBS -l select=1:ncpus=16

# source ~/.bashrc
# hostname
# conda activate 
# export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families/

portho_path=/groups/itay_mayrose/galtoledano/gene_families/PorthoMCL
sample_path=/groups/itay_mayrose/galtoledano/gene_families/test_sample
inflation=3

bash scripts/porthomcl.sh $portho_path $sample_path $inflation > /groups/itay_mayrose/galtoledano/gene_families/error_logs/porthomcl.out 2> /groups/itay_mayrose/galtoledano/gene_families/error_logs/porthomcl.err
