#!/bin/bash

# we use a simple test file here with a window that contains all the data at once,
# as a hacky way to get popoolation to compute a whole genome fst value.

#FILE="counts.sync"
#WINDOW=51648
#WINDOW=1000

FILE="line2.txt"
WINDOW=1

echo "Start `date`"
START=$(date +%s.%N)

perl ../../software/popoolation2/fst-sliding.pl \
    --input ${FILE} \
    --output "fst.txt" \
    --suppress-noninformative \
    --window-size ${WINDOW} \
    --step-size ${WINDOW} \
    --pool-size 100 \
    --max-coverage 200 \
    > fst.log 2>&1

    # --min-coverage 50 \
    # --min-count 6 \
    # --min-covered-fraction 1 \

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
