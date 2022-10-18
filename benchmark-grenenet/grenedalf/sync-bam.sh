#!/bin/bash

OUT=${1}
DATA=${@:2}

GRENEDALF="/home/lucas/Dropbox/GitHub/grenedalf/bin/grenedalf"

# build command line
INPATHS=""
for D in ${DATA} ; do
    INPATHS="${INPATHS} --sam-path ${D}"
done

mkdir -p sync-bam
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF sync-file \
    ${INPATHS} \
    --out-dir "sync-bam" \
    --file-suffix "-${OUT}" \
    --threads 2 \
    --allow-file-overwriting \
    > "logs/sync-bam-${OUT}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
