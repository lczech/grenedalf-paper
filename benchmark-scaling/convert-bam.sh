#!/bin/bash

GRENEDALF="../software/grenedalf/bin/grenedalf"

# Input files
DATADIR="/home/lucas/Projects/grenephase1/mapped"
DATA=$'MLFH010220180423-1.sorted.bam\nMLFH010120190429-2.sorted.bam\nMLFH010120180409-1.sorted.bam\nMLFH010120180423-2.sorted.bam\nMLFH010520180507-1.sorted.bam\nMLFH010420180507-1.sorted.bam\nMLFH010220190429-2.sorted.bam\nMLFH010220190513-1.sorted.bam'

mkdir -p logs

# Genome ref for mpileup
FASTA="../benchmark-grenenet/TAIR10_chr_all.fa"

# Convert - all at once, because why not
for FILE in $DATA ; do
    echo "`date` grenedalf sync ${FILE}"
    ${GRENEDALF} sync-file \
        --sam-path ${DATADIR}/${FILE} \
        --reference-genome-file ${FASTA} \
        --out-dir "sync" \
        --file-suffix "-${FILE}" \
        --allow-file-overwriting \
        > "logs/sync-${FILE}.log" 2>&1 &
done
