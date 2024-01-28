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
# todo: add parnt directory
bash scripts/create_profile_db.sh
# todo: add parmaters
bash scripts/hmm_scan.sh

