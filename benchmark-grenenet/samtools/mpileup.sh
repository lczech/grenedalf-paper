#!/bin/bash

OUT=${1}
DATA=${@:2}

# Fasta ref file for ref bases in the mpileup
FASTA="../TAIR10_chr_all.fa"

mkdir -p mpileup
mkdir -p logs
# rm mpileup/*

echo "Start `date`"
START=$(date +%s.%N)

samtools mpileup \
    -f ${FASTA} \
    -R -B \
    -o mpileup/${OUT} \
    ${DATA} \
    > logs/mpileup-${OUT}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
