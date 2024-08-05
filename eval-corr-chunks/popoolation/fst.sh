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
DATA="../chunks_sync/split_${chunk}"
WINDOW=$window
METHOD=$method

if [[ "$METHOD" == "karlsson" ]]; then
    METHODSTR="--karlsson-fst"
else
    METHODSTR=""
fi
if [[ "$WINDOW" == "1" ]]; then
    OMITSTR="--suppress-noninformative"
else
    OMITSTR=""
fi

POPOOL="../../software/popoolation2"

mkdir -p fst
mkdir -p logs
# rm fst/*

echo "Start `date`"
START=$(date +%s.%N)

perl ${POPOOL}/fst-sliding.pl \
    --input ${DATA} \
    ${METHODSTR} \
    ${OMITSTR} \
    --output "fst/${OUT}-${WINDOW}-${METHOD}.fst" \
    --window-size ${WINDOW} \
    --step-size ${WINDOW} \
    --pool-size 100 \
    --min-count 2 \
    --min-coverage 4 \
    --max-coverage 100 \
    --min-covered-fraction 0 \
    > logs/fst-${OUT}-${WINDOW}-${METHOD}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
