#!/bin/bash

# Parse the args.
# Dirty: we use the key to set a variable named that way.
for arg in "$@"; do
    key=${arg%%=*}
    val=${arg#*=}
    eval "$key"='$val'
done

# Set the args that we need here
OUT="${type}-${scaling}-${size}"
GRENEDALF="../../software/grenedalf/bin/grenedalf"

# See diversity.sh for the selection of the files.
DATADIR="/home/lucas/Projects/grenephase1/mapped"
DATA=$'MLFH010220180423-1.sorted.bam\nMLFH010120190429-2.sorted.bam\nMLFH010120180409-1.sorted.bam\nMLFH010120180423-2.sorted.bam\nMLFH010520180507-1.sorted.bam\nMLFH010420180507-1.sorted.bam\nMLFH010220190429-2.sorted.bam\nMLFH010220190513-1.sorted.bam'

# For sync scaling, use the converted data instead
if [[ "${type}" == "sync" ]]; then
    DATADIR="../sync"
    DATA=$'counts-MLFH010220180423-1.sorted.bam.sync\ncounts-MLFH010120190429-2.sorted.bam.sync\ncounts-MLFH010120180409-1.sorted.bam.sync\ncounts-MLFH010120180423-2.sorted.bam.sync\ncounts-MLFH010520180507-1.sorted.bam.sync\ncounts-MLFH010420180507-1.sorted.bam.sync\ncounts-MLFH010220190429-2.sorted.bam.sync\ncounts-MLFH010220190513-1.sorted.bam.sync'
fi

# For weak scaling, select as many samples as we need for this test run.
# Bash needs the quotes in the inner ${DATA}... otherwise the new lines don't work. WTF.
if [[ "$scaling" == "weak" ]]; then
    DATA=`echo -e "${DATA}" | head -n ${size}`
fi

# build command line
INPATHS=""
for D in ${DATA} ; do
    if [[ "${type}" == "sync" ]]; then
        INPATHS="${INPATHS} --sync-path ${DATADIR}/${D}"
    else
        INPATHS="${INPATHS} --sam-path ${DATADIR}/${D}"
    fi
done

mkdir -p fst-${scaling}
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF fst \
    ${INPATHS} \
    --window-type genome \
    --window-average-policy valid-snps \
    --pool-sizes 100 \
    --method unbiased-nei \
    --no-nan-windows \
    --out-dir "fst-${scaling}" \
    --file-suffix "-${OUT}" \
    --threads ${size} \
    --allow-file-overwriting \
    > "logs/fst-${OUT}.log" 2>&1

#    --window-interval-width 1000 \

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
