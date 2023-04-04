#!/bin/bash

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
GRENEDALF="../../software/grenedalf/bin/grenedalf"

# We need both runs, for comparing with npstat and with popoolation
if [[ -z "$bugs" ]]; then
    BUGS=""
    OUT="${OUT}-nobugs"
else
    BUGS="--popoolation-corrected-tajimas-d"
    OUT="${OUT}-popoolation"
fi

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
    $BUGS \
    --window-type sliding \
    --window-sliding-width 1000 \
    --filter-sample-min-count 2 \
    --filter-sample-min-coverage 4 \
    --filter-sample-max-coverage 1000 \
    --pileup-min-base-qual 10 \
    --pool-sizes 100 \
    --out-dir "diversity-mpileup" \
    --file-suffix "-${OUT}" \
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
