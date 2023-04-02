#!/bin/bash

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
OUT=${size}
DATA="../data/subsets-mpileup/S1S2-${size}.mpileup"

POPOOL="../../software/popoolation2"

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
