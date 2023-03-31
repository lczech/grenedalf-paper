#!/bin/bash

mkdir -p fst
mkdir -p logs
# rm fst/*

# Get args
FILE=$1
BASENAME=$(basename $1)
WINDOW=$2

echo "Start `date`"
START=$(date +%s.%N)

if [[ ${WINDOW} == 0 ]]; then

    ../../software/grenedalf/bin/grenedalf fst \
        --sync-path ${FILE} \
        --window-type genome \
        --pool-sizes 100,100 \
        --method kofler \
        --omit-na-windows \
        --out-dir fst \
        --file-suffix "-${WINDOW}-${BASENAME}" \
        --allow-file-overwriting \
        --threads 1 \
        > logs/fst-${WINDOW}-${BASENAME}.log 2>&1

else

    ../../software/grenedalf/bin/grenedalf fst \
        --sync-path ${FILE} \
        --window-type sliding \
        --window-sliding-width ${WINDOW} \
        --pool-sizes 100,100 \
        --method kofler \
        --omit-na-windows \
        --out-dir fst \
        --file-suffix "-${WINDOW}-${BASENAME}" \
        --allow-file-overwriting \
        --threads 1 \
        > logs/fst-${WINDOW}-${BASENAME}.log 2>&1

fi

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
