#!/bin/bash

OUT=${1}
DATA=${@:2}

POPOOL="/home/lucas/Dropbox/GitHub/popoolation2"

mkdir -p sync-perl
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

perl ${POPOOL}/mpileup2sync.pl \
    --input ${DATA} \
    --output "sync-perl/${OUT}.sync" \
    --fastq-type sanger \
    > "logs/sync-perl-${OUT}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
