#!/bin/bash
#PBS -S /bin/bash
#PBS -N porthomcl_sly
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/error_logs/porthomcl_sly.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/error_logs/porthomcl_sly.OUT
#PBS -p 3
#PBS -l select=1:ncpus=16
source ~/.bashrc
hostname
conda activate PorthoMCL
export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families/
portho_path=/groups/itay_mayrose/galtoledano/gene_families/PorthoMCL
sample_path=/groups/itay_mayrose/galtoledano/gene_families/plaza/sly/
inflation=2
# bash scripts/porthomcl.sh $portho_path $sample_path $inflation

for i in 1.2 1.5 2 2.5 3 3.5 4 4.5 5
do
    bash scripts/porthomcl.sh $portho_path $sample_path $i
done