#!/bin/bash

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
OUT="S1S2-20000000"
DATA="../../benchmark-grenenet/data/subsets-sync/S1S2-20000000.sync"
OUT="S1S2-2000"
DATA="../../benchmark-grenenet/data/subsets-sync/S1S2-2000.sync"
WINDOW=$window
METHOD=$method

if [[ "$METHOD" == "karlsson" ]]; then
    METHODSTR="--karlsson-fst"
else
    METHODSTR=""
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
    --output "fst/${OUT}-${WINDOW}-${METHOD}.fst" \
    --suppress-noninformative \
    --window-size ${WINDOW} \
    --step-size ${WINDOW} \
    --pool-size 100 \
    --min-count 2 \
    --min-coverage 4 \
    --max-coverage 100 \
    --min-covered-fraction 0 \
    --suppress-noninformative \
    > logs/fst-${OUT}-${WINDOW}-${METHOD}.log 2>&1


    # the first test was with
    # --window-size 1 \

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
