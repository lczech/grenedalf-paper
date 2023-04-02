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
OUT=${size}
DATA="../data/subsets-mpileup/S1-${size}.mpileup"

echo "Start `date`"
START=$(date +%s.%N)

# setting the max cov to a max that kinda works.
# npstat precomputes the denomiator tables;
# any larger values will hence take ages to process :-(

../../software/npstat/npstat \
    -n 100 \
    -l 1000 \
    -maxcov 1000 \
    -minqual 0 \
    ${DATA} \
    > logs/diversity-${OUT}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"

# npstat just produces the file where the original is.
# let's move it to a better place.
mv ${DATA}.stats diversity/diversity-${OUT}.stats
