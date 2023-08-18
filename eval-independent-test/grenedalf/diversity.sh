#!/bin/bash

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
GRENEDALF="../../software/grenedalf/bin/grenedalf"

mkdir -p diversity
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

${GRENEDALF} diversity \
    --pileup-path ${fileid} \
    --window-type sliding \
    --window-sliding-width ${windowsize} \
    --filter-sample-min-count 2 \
    --filter-sample-min-coverage 2 \
    --pileup-min-base-qual 0 \
    --pool-sizes ${poolsize} \
    --measure "all" \
    --out-dir "diversity" \
    --file-suffix "-${outid}" \
    --na-entry nan \
    --allow-file-overwriting \
    > "logs/diversity-${outid}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
