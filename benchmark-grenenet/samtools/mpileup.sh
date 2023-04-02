#!/bin/bash

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
OUT=${size}
DATA="../data/subsets-bam/S1-${size}.bam ../data/subsets-bam/S2-${size}.bam"

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
    -o mpileup/${OUT}.pileup \
    ${DATA} \
    > logs/mpileup-${OUT}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
