#!/bin/bash

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
OUT="split_${chunk}"
DATA="../chunks_mpileup/split_${chunk}"

# We use the same script for all measures in PoPoolation, for simplicity
MEASURE=$measure
if [[ -z $MEASURE ]]; then
    MEASURE="d"
fi

POPOOL="../../software/popoolation"

mkdir -p diversity
mkdir -p logs
# rm ${MEASURE}/*

START=$(date +%s.%N)
echo "Start `date`"

perl ${POPOOL}/Variance-sliding.pl \
    --input ${DATA} \
    --output "diversity/${OUT}.${MEASURE}" \
    --measure ${MEASURE} \
    --window-size 1000 \
    --step-size 1000 \
    --fastq-type sanger \
    --min-qual 10 \
    --pool-size 100 \
    --min-count 2 \
    --min-coverage 4 \
    --max-coverage 500 \
    --min-covered-fraction 0.0 \
    --no-discard-deletions \
    > logs/${MEASURE}-${OUT}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
