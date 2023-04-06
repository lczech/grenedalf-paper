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
GRENEDALF="../../software/grenedalf/bin/grenedalf"
WINDOW=$window
METHOD=$method

# Hard coding here, super dirty. For window 100, we want SNP windows,
# so that we can compare with poolfstat.
if [[ ${WINDOW} == "100" ]]; then
    WINDOWSTR="--window-type queue --window-queue-count ${WINDOW}"
else
    WINDOWSTR="--window-type sliding --window-sliding-width ${WINDOW}"
fi
if [[ "$WINDOW" == "1" ]]; then
    OMITSTR="--omit-na-windows"
else
    OMITSTR=""
fi

# build command line
INPATHS=""
for D in ${DATA} ; do
    INPATHS="${INPATHS} --sync-path ${D}"
done

mkdir -p fst
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF fst \
    ${INPATHS} \
    ${WINDOWSTR} \
    ${OMITSTR} \
    --pool-sizes 100 \
    --method ${METHOD} \
    --out-dir "fst" \
    --file-suffix "-${OUT}-${WINDOW}-${METHOD}" \
    --filter-sample-min-count 2 \
    --filter-sample-min-coverage 4 \
    --filter-sample-max-coverage 100 \
    --na-entry nan \
    --allow-file-overwriting \
    > "logs/fst-${OUT}-${WINDOW}-${METHOD}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
