#!/bin/bash

for d in /groups/itay_mayrose/galtoledano/gene_families/plaza/*
do
species=$(basename $d)
echo $species
gunzip -cd /groups/itay_mayrose/galtoledano/gene_families/data/plaza_families/genefamily_data.ORTHOFAM.csv.gz | grep $species | cut -f 1,3 > /groups/itay_mayrose/galtoledano/gene_families/data/plaza_families/$species.csv
done