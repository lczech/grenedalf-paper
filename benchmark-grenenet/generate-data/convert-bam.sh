#!/bin/bash

# Simple test to check what one typical bam file from GrENE-net turns into
# when converting it to mpileup and sync, to see how much additional disk space is needed.

GRENEDALF="/home/lucas/Dropbox/GitHub/grenedalf/bin/grenedalf"

# Input file and output files
bam1="/home/lucas/Projects/grenephase1/mapped/MLFH010120200420-1.sorted.bam"
mpileup1="MLFH010120200420.mpileup"
sync1="MLFH010120200420.sync"

# Genome ref for mpileup
FASTA="../TAIR10_chr_all.fa"

# sam tools needs the bams to be indexed
if [ ! -f ${bam1}.bai ] ; then
    echo "indexing ${bam1}"
    samtools index $bam1
fi

if [ ! -f ${mpileup1} ] ; then
    echo "samtools mpileup MLFH010120200420"
    samtools mpileup -f ${FASTA} -R -B -o "${mpileup1}" ${bam1} 
fi

if [ ! -f ${sync1} ] ; then
    echo "grenedalf sync MLFH010120200420"
    ${GRENEDALF} sync-file --sam-path ${bam1} --allow-file-overwriting
    mv "counts.sync" ${sync1}
fi

if [ ! -f ${sync1}.gz ] ; then
    echo "gzip MLFH010120200420"
    cat ${sync1} | gzip > ${sync1}.gz
fi

