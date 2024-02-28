#!/bin/bash
#PBS -S /bin/bash
#PBS -N c.elegans_porthomcl
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/plaza/porthomcl_c.ele.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/plaza/porthomcl_c.ele.OUT
#PBS -p 3
#PBS -l select=1:ncpus=16
source ~/.bashrc
hostname
conda activate PorthoMCL
export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families/
portho_path=/groups/itay_mayrose/galtoledano/gene_families/PorthoMCL
sample_path=/groups/itay_mayrose/galtoledano/gene_families/plaza/c.elegans/
# inflation=2
for i in 1.2 1.5 2 2.5 3 3.5 4 4.5 5
do
    bash scripts/porthomcl.sh $portho_path $sample_path $i
done