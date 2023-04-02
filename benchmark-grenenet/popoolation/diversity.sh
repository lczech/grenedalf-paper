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
DATA="../data/subsets-mpileup/S1-${size}.mpileup"

# We use the same script for all measures in PoPoolation, for simplicity
MEASURE=$measure

POPOOL="../../software/popoolation"

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
    --max-coverage 1000 \
    > logs/${MEASURE}-${OUT}.log 2>&1

# The default value of PoPoolation for max cov is way to high compared to what it
# actually can reasonably compute... for our data here, with the default,
# we'd have hours and hours of runtime once we hit parts in our data with higher
# coverages. so we limit it here, in order to be able to run the benchmarks at all.

    # --max-coverage 1000000 \
    # --min-count 2 \
    # --min-coverage 4 \
    # --min-qual 0 \

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
