#!/bin/bash

DATA=$1

mkdir -p fst
# rm fst/*

START=$(date +%s.%N)
echo "Start `date`"

perl ../../software/popoolation2/fst-sliding.pl \
    --input ${DATA} \
    --output "fst/$(basename ${DATA}).fst" \
    --suppress-noninformative \
    --min-count 6 \
    --min-coverage 4 \
    --max-coverage 1000 \
    --min-covered-fraction 1 \
    --window-size 1 \
    --step-size 1 \
    --pool-size 100
    > fst/$(basename ${DATA}).log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
