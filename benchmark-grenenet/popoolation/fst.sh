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
DATA="../data/subsets-sync/S1S2-${size}.sync"

POPOOL="../../software/popoolation2"

mkdir -p fst
mkdir -p logs
# rm fst/*

echo "Start `date`"
START=$(date +%s.%N)

perl ${POPOOL}/fst-sliding.pl \
    --input ${DATA} \
    --output "fst/${OUT}.fst" \
    --suppress-noninformative \
    --window-size 1000 \
    --step-size 1 \
    --pool-size 100 \
    --max-coverage 200 \
    > logs/fst-${OUT}.log 2>&1

    # --min-count 6 \
    # --min-coverage 50 \
    # --min-covered-fraction 1 \

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
