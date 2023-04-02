#!/bin/bash

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
DATA="../data/subsets-sync-gz/S1S2-${size}.sync.gz"
OUT=${size}-gz

GRENEDALF="../../software/grenedalf/bin/grenedalf"

# build command line
INPATHS=""
for D in ${DATA} ; do
    INPATHS="${INPATHS} --sync-path ${D}"
done

mkdir -p fst-sync
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF fst \
    ${INPATHS} \
    --window-type sliding \
    --window-sliding-width 1000 \
    --pool-sizes 100 \
    --method kofler \
    --omit-na-windows \
    --out-dir "fst-sync" \
    --file-suffix "-${OUT}" \
    --threads 1 \
    --allow-file-overwriting \
    > "logs/fst-sync-${OUT}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
