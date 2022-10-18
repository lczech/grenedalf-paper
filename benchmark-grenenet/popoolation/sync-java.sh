#!/bin/bash

OUT=${1}
DATA=${@:2}

POPOOL="/home/lucas/Dropbox/GitHub/popoolation2"

mkdir -p sync-java
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

java -ea -Xmx7g -jar ${POPOOL}/mpileup2sync.jar \
    --input ${DATA} \
    --output "sync-java/${OUT}.sync" \
    --fastq-type sanger \
    > "logs/sync-java-${OUT}.log" 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
