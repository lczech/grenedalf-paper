#!/bin/bash

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

POPOOL="../../software/popoolation"

mkdir -p diversity
mkdir -p logs
# rm ${MEASURE}/*

START=$(date +%s.%N)
echo "Start `date`"

perl ${POPOOL}/Variance-sliding.pl \
    --input ${fileid} \
    --output "diversity/${outid}" \
    --measure ${measure} \
    --window-size ${windowsize} \
    --step-size ${windowsize} \
    --fastq-type sanger \
    --min-qual 0 \
    --pool-size ${poolsize} \
    --min-count 2 \
    --min-coverage 4 \
    --max-coverage 500 \
    --min-covered-fraction 0.0 \
    --no-discard-deletions \
    > logs/${outid}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
