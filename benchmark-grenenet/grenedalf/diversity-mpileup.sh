#!/bin/bash

OUT=${1}
DATA=${@:2}

GRENEDALF="/home/lucas/Dropbox/GitHub/grenedalf/bin/grenedalf"

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
    --window-type sliding \
    --window-sliding-width 1000 \
    --pool-sizes 100 \
    --popoolation-corrected-tajimas-d \
    --out-dir "diversity-mpileup" \
    --file-suffix "-${OUT}" \
    --threads 2 \
    --allow-file-overwriting \
    > "logs/diversity-mpileup-${OUT}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
