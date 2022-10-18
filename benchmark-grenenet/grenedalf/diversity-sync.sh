#!/bin/bash

OUT=${1}
DATA=${@:2}

GRENEDALF="/home/lucas/Dropbox/GitHub/grenedalf/bin/grenedalf"

# build command line
INPATHS=""
for D in ${DATA} ; do
    INPATHS="${INPATHS} --sync-path ${D}"
done

mkdir -p diversity-sync
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF diversity \
    ${INPATHS} \
    --window-type sliding \
    --window-sliding-width 1000 \
    --pool-sizes 100 \
    --popoolation-corrected-tajimas-d \
    --out-dir "diversity-sync" \
    --file-suffix "-${OUT}" \
    --threads 2 \
    --allow-file-overwriting \
    > "logs/diversity-sync-${OUT}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
