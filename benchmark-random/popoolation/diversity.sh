#!/bin/bash

# We use the same script for all measures in PoPoolation, for simplicity
DATA=$1
MEASURE=$2

mkdir -p ${MEASURE}
# rm ${MEASURE}/*

START=$(date +%s.%N)
echo "Start `date`"

perl ../../software/popoolation/Variance-sliding.pl \
    --input ${DATA} \
    --output "${MEASURE}/$(basename ${DATA}).${MEASURE}" \
    --measure ${MEASURE} \
    --fastq-type sanger \
    --window-size 1000 \
    --step-size 1000 \
    --pool-size 100 \
    --min-count 2 \
    --min-coverage 4 \
    --max-coverage 1000000 \
    --min-qual 0 \
    > ${MEASURE}/$(basename ${DATA}).log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
