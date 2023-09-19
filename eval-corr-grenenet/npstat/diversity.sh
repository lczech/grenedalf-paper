#!/bin/bash

mkdir -p diversity
mkdir -p logs

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
OUT="S1-20000000"
DATA="../../benchmark-grenenet/data/subsets-mpileup/S1-20000000.mpileup"
WINDOW=$window

echo "Start `date`"
START=$(date +%s.%N)

# setting the max cov to a max that kinda works.
# npstat precomputes the denomiator tables;
# any larger values will hence take ages to process :-(

../../software/npstat/npstat \
    -n 100 \
    -l ${WINDOW} \
    -nolowfreq 2 \
    -mincov 4 \
    -maxcov 1000 \
    -minqual 10 \
    ${DATA} \
    > logs/diversity-${OUT}-${WINDOW}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"

# npstat just produces the file where the original is.
# let's move it to a better place.
mv ${DATA}.stats diversity/diversity-${OUT}-${WINDOW}.stats
