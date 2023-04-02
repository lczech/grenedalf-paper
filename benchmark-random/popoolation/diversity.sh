#!/bin/bash

mkdir -p diversity
mkdir -p logs
# rm ${MEASURE}/*

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
MEASURE=$measure

echo "Start `date`"
START=$(date +%s.%N)

perl ../../software/popoolation/Variance-sliding.pl \
    --input ${FILE} \
    --output "diversity/${MEASURE}-${WINDOW}-${BASENAME}.txt" \
    --measure ${MEASURE} \
    --fastq-type sanger \
    --window-size ${WINDOW} \
    --step-size ${WINDOW} \
    --pool-size 100 \
    --min-count 2 \
    --min-coverage 4 \
    --max-coverage 1000000 \
    --min-qual 0 \
    > logs/${MEASURE}-${WINDOW}-${BASENAME}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
