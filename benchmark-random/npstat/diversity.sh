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
FILE="../data/pileup/random-${size}.pileup"
BASENAME=$(basename $FILE)
WINDOW=$window

echo "Start `date`"
START=$(date +%s.%N)

# setting the max cov to the max that we have in the data.
# npstat precomputes the denomiator tables;
# any larger values will hence take ages to compute :-(

../../software/npstat/npstat \
    -n 100 \
    -l ${WINDOW} \
    -maxcov 500 \
    -minqual 0 \
    ${FILE} \
    > logs/diversity-${WINDOW}-${BASENAME}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"

# npstat just produces the file where the original is.
# let's move it to a better place.
mv ${FILE}.stats diversity/diversity-${WINDOW}-${BASENAME}.stats
