#!/bin/bash

mkdir -p diversity
mkdir -p logs
# rm diversity/*

# Get args
FILE=$1
BASENAME=$(basename $1)
WINDOW=$2

echo "Start `date`"
START=$(date +%s.%N)

../../software/grenedalf/bin/grenedalf diversity \
    --pileup-path ${FILE} \
    --window-type sliding \
    --window-sliding-width ${WINDOW} \
    --filter-sample-min-count 2 \
    --filter-sample-min-coverage 4 \
    --filter-sample-max-coverage 1000000 \
    --pool-sizes 100 \
    --popoolation-corrected-tajimas-d \
    --out-dir diversity \
    --file-suffix "-${WINDOW}-${BASENAME}" \
    --allow-file-overwriting \
    --threads 1 \
    > logs/diversity-${WINDOW}-${BASENAME}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
