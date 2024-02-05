#!/bin/bash
#PBS -S /bin/bash
#PBS -N porthomcl_gma
#PBS -r y
#PBS -q itaym
#PBS -V
#PBS -e /groups/itay_mayrose/galtoledano/gene_families/error_logs/error_logs/porthomcl_gma.ERR
#PBS -o /groups/itay_mayrose/galtoledano/gene_families/error_logs/error_logs/porthomcl_gma.OUT
#PBS -p 3
#PBS -l select=1:ncpus=16
source ~/.bashrc
hostname
conda activate PorthoMCL
export PATH=$CONDA_PREFIX/bin:$PATH

cd /groups/itay_mayrose/galtoledano/gene_families/
portho_path=/groups/itay_mayrose/galtoledano/gene_families/PorthoMCL
sample_path=/groups/itay_mayrose/galtoledano/gene_families/plaza/gma/
inflation=2
bash scripts/porthomcl.sh $portho_path $sample_path $inflation

# sample_base_path=/groups/itay_mayrose/galtoledano/gene_families/hmm_runs
# error_logs_path=/groups/itay_mayrose/galtoledano/gene_families/error_logs
# profile_families=/groups/itay_mayrose/danielz/gene_fams/test/results.txt
# inflation_values=(1.2 1.5 2 2.5 3 3.5 4 4.5 5) 

# sample_path="${sample_base_path}_I${inflation}"
    # echo $sample_path
    # mkdir $sample_path
    # cp -r /groups/itay_mayrose/galtoledano/gene_families/data/hmm_referance/0.input_faa $sample_path

    # Run the command with the updated sample_path
    # bash scripts/porthomcl.sh "$portho_path" "$sample_path" "$inflation" > "$error_logs_path/ensmble_porthomcl_I${inflation}.out" 2> "$error_logs_path/ensmle_porthomcl_I${inflation}.err"
# cat $profile_families $sample_path/genes_families.tsv > $sample_path/full_set_gene_families.tsv

