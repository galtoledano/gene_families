#!/bin/bash
# # This code run hmm scan on the profile database

data_path=$1
data_base=$2
genome=$3
species=$4

timestamp=$(date +%F_%T)
echo $timestamp

cd $data_path
hmmscan --cpu 25 --tblout $data_path/results_$species.txt $data_base $genome

timestamp=$(date +%F_%T)
echo $timestamp

