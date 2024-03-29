#!/bin/bash

OUT=${1}
DATA=${@:2}

GRENEDALF="/home/lucas/Dropbox/GitHub/grenedalf/bin/grenedalf"

# build command line
INPATHS=""
for D in ${DATA} ; do
    INPATHS="${INPATHS} --sync-path ${D}"
done

mkdir -p fst-sync
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF fst \
    ${INPATHS} \
    --window-type sliding \
    --window-sliding-width 1000 \
    --pool-sizes 100 \
    --method kofler \
    --omit-na-windows \
    --out-dir "fst-sync" \
    --file-suffix "-${OUT}" \
    --threads 2 \
    --allow-file-overwriting \
    > "logs/fst-sync-${OUT}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
