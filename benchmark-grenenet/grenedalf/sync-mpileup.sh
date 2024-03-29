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
DATA="../data/subsets-mpileup/S1S2-${size}.mpileup"

GRENEDALF="../../software/grenedalf/bin/grenedalf"

# build command line
INPATHS=""
for D in ${DATA} ; do
    INPATHS="${INPATHS} --pileup-path ${D}"
done

mkdir -p sync-mpileup
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF sync-file \
    ${INPATHS} \
    --out-dir "sync-mpileup" \
    --file-suffix "-${OUT}" \
    --threads 1 \
    --allow-file-overwriting \
    > "logs/sync-mpileup-${OUT}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
