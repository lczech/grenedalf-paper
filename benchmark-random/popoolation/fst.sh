#!/bin/bash

mkdir -p fst
mkdir -p logs
# rm fst/*

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
FILE="../data/sync/random-${size}.sync"
BASENAME=$(basename $FILE)
WINDOW=$window

echo "Start `date`"
START=$(date +%s.%N)

perl ../../software/popoolation2/fst-sliding.pl \
    --input ${FILE} \
    --output "fst/fst-${WINDOW}-${BASENAME}.fst" \
    --suppress-noninformative \
    --window-size ${WINDOW} \
    --step-size ${WINDOW} \
    --pool-size 100 \
    --max-coverage 200 \
    > logs/fst-${WINDOW}-${BASENAME}.log 2>&1

    # --min-coverage 50 \
    # --min-count 6 \
    # --min-covered-fraction 1 \

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
