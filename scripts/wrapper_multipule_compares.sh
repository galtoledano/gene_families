#!/bin/bash
#PBS -S /bin/bash
#PBS -N Comparison
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/inflations.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/inflations.OUT
#PBS -p 3
#PBS -l select=1:ncpus=4
source ~/.bashrc
hostname
conda activate PorthoMCL
export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families/
python3 scripts/compare_portho_parmeters.py > error_logs/inflations.out 2> error_logs/inflations.err
