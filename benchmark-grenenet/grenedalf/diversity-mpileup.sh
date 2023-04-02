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

GRENEDALF="../../software/grenedalf/bin/grenedalf"

# build command line
INPATHS=""
for D in ${DATA} ; do
    INPATHS="${INPATHS} --pileup-path ${D}"
done

mkdir -p diversity-mpileup
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF diversity \
    ${INPATHS} \
    --window-type sliding \
    --window-sliding-width 1000 \
    --filter-sample-min-count 2 \
    --filter-sample-min-coverage 4 \
    --filter-sample-max-coverage 1000 \
    --pool-sizes 100 \
    --popoolation-corrected-tajimas-d \
    --out-dir "diversity-mpileup" \
    --file-suffix "-${OUT}" \
    --threads 1 \
    --allow-file-overwriting \
    > "logs/diversity-mpileup-${OUT}.log" 2>&1

# grenedalf can easily use the higher coverage,
# but in order for a fair comparison, we use the same value here
# that works for the other two tools ;-)
# --filter-sample-max-coverage 1000000 \

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
