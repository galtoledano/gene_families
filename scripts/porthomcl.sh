
#!/bin/bash
# # Running the PorthoMCL pipeline.
# # Pay attention that this script requires 16 CPUs. If you want to use fewer, please change the parameter.
# # The script takes 3 parameters:
# # 1. Path to the folder with PorthoMCL code.
# # 2. Path to the input, the sample on which we want to run the pipeline. This is a directory that contains a subdirectory named "0.input_faa" with the input FASTA file inside.
# # 3. Inflation parameter for creating clusters with the MCL algorithm.
# # To run this script, use:
# # bash porthomcl.sh <PATH_TO_PORTHOMCL> <PATH_TO_SAMPLE> <INFLATION>

portho_location=$1
sample_name=$2
inflation=$3
cpus=16

#1-2
$portho_location/porthomcl.sh -e 2 $sample_name

#3
makeblastdb -in $sample_name/2.filteredFasta/goodProteins.fasta  -dbtype prot
mkdir $sample_name/3.blastdb
mv $sample_name/2.filteredFasta/goodProteins.fasta.* $sample_name/3.blastdb/
mkdir $sample_name/3.blastquery 
$portho_location/porthomclSplitFasta.py -i $sample_name/2.filteredFasta/goodProteins.fasta  -o $sample_name/3.blastquery 
cd $sample_name
mkdir 3.blastres 
blastp -query 3.blastquery/*.fasta -db 3.blastdb/goodProteins.fasta  -seg yes  -dbsize 100000000 -evalue 1e-5 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen" -num_threads $cpus -out 3.blastres/proteome_ath_longest.tab
cd ../..

#normalize_score
#python normelize_score.py $sample_name/3.blastres/proteome_ath_longest1.tab $sample_name/3.blastres/proteome_ath_longest.tab

#4
mkdir $sample_name/4.splitSimSeq
$portho_location/porthomclBlastParser $sample_name/3.blastres/proteome_ath_longest.tab $sample_name/1.compliantFasta >> $sample_name/4.splitSimSeq/proteome_ath_longest.ss.tsv

#5
mkdir $sample_name/5.paralogTemp
mkdir $sample_name/5.besthit
$portho_location/porthomclPairsBestHit.py -t $sample_name/taxon_list -s $sample_name/4.splitSimSeq -b $sample_name/5.besthit -q $sample_name/5.paralogTemp -x 1

#6
echo $sample_name
mkdir $sample_name/6.orthologs
$portho_location/porthomclPairsOrthologs.py -t $sample_name/taxon_list -b $sample_name/5.besthit -o $sample_name/6.orthologs -x 1

#7
cd $sample_name
mkdir 7.ogenes
# genes in the second column
awk -F'[|\t]' '{print $4 >> ("7.ogenes/"$3".og.tsv")}' 6.orthologs/*.ort.tsv
# genes in the first column
awk -F'[|\t]' '{print $2 >> ("7.ogenes/"$1".og.tsv")}' 6.orthologs/*.ort.tsv
cd ../..
mkdir $sample_name/7.paralogs
$portho_location/porthomclPairsInParalogs.py -t $sample_name/taxon_list -q $sample_name/5.paralogTemp -o $sample_name/7.ogenes -p $sample_name/7.paralogs -x 1

#8
cat $sample_name/7.paralogs/*.tsv >> $sample_name/8.all.par.tsv
mcl $sample_name/8.all.par.tsv  --abc -I $inflation -t 4 -o $sample_name/8.all.par.group

# add orphans
python /groups/itay_mayrose/galtoledano/gene_families/scripts/add_orphans.py $sample_name/0.input_faa/*.faa $sample_name/8.all.par.group