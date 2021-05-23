#!/bin/bash

mkdir -p fst
# rm fst/*

START=$(date +%s.%N)
echo "Start `date`"

../software/grenedalf/bin/grenedalf fst \
    --threads 1 \
    --allow-file-overwriting \
    --out-dir fst \
    --file-suffix "_$(basename $1)" \
    --sync-file $1 \
    --pool-sizes 100,100 \
    --window-width 1 \
    --omit-na-windows \
    > fst/fst_$(basename $1).log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
