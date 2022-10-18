#!/bin/bash

# We use the same script for all measures in PoPoolation, for simplicity
MEASURE=$1
OUT=$2
DATA=${@:3}

POPOOL="/home/lucas/Dropbox/GitHub/popoolation"

mkdir -p ${MEASURE}
mkdir -p logs
# rm ${MEASURE}/*

START=$(date +%s.%N)
echo "Start `date`"

perl ${POPOOL}/Variance-sliding.pl \
    --input ${DATA} \
    --output "${MEASURE}/${OUT}.${MEASURE}" \
    --measure ${MEASURE} \
    --fastq-type sanger \
    --window-size 1000 \
    --step-size 1000 \
    --pool-size 100 \
    > logs/${MEASURE}-${OUT}.log 2>&1

    # --min-count 2 \
    # --min-coverage 4 \
    # --max-coverage 1000000 \
    # --min-qual 0 \

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
