#!/bin/bash

mkdir -p diversity
mkdir -p logs
# rm diversity/*

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
FILE="../data/pileup/random-${size}.pileup"
BASENAME=$(basename $FILE)
WINDOW=$window

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
