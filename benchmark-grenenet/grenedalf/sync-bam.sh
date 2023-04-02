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
DATA="../data/subsets-bam/S1-${size}.bam ../data/subsets-bam/S2-${size}.bam"

GRENEDALF="../../software/grenedalf/bin/grenedalf"

# build command line
INPATHS=""
for D in ${DATA} ; do
    INPATHS="${INPATHS} --sam-path ${D}"
done

mkdir -p sync-bam
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF sync-file \
    ${INPATHS} \
    --out-dir "sync-bam" \
    --file-suffix "-${OUT}" \
    --threads 1 \
    --allow-file-overwriting \
    > "logs/sync-bam-${OUT}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
