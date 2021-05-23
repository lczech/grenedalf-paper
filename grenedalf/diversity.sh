#!/bin/bash

mkdir -p diversity
# rm diversity/*

START=$(date +%s.%N)
echo "Start `date`"

../software/grenedalf/bin/grenedalf diversity \
    --threads 1 \
    --allow-file-overwriting \
    --out-dir diversity \
    --file-suffix "_$(basename $1)" \
    --pileup-file $1 \
    --pool-sizes 100 \
    --window-width 1000 \
    --popoolation-corrected-tajimas-d \
    > diversity/diversity_$(basename $1).log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
