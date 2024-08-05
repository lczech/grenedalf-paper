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

# Random selection of files:
# ls | sort -R | head -n 8
    # -rw-rw-r-- 1 lucas lucas 1284896664 Jul 22  2022 MLFH010220180423-1.sorted.bam
    # -rw-rw-r-- 1 lucas lucas 1070659932 Jul 22  2022 MLFH010120190429-2.sorted.bam
    # -rw-rw-r-- 1 lucas lucas 1246495519 Jul 22  2022 MLFH010120180409-1.sorted.bam
    # -rw-rw-r-- 1 lucas lucas 1177283339 Jul 22  2022 MLFH010120180423-2.sorted.bam
    # -rw-rw-r-- 1 lucas lucas  680730139 Jul 22  2022 MLFH010520180507-1.sorted.bam
    # -rw-rw-r-- 1 lucas lucas  821496849 Jul 22  2022 MLFH010420180507-1.sorted.bam
    # -rw-rw-r-- 1 lucas lucas 1423138742 Jul 22  2022 MLFH010220190429-2.sorted.bam
    # -rw-rw-r-- 1 lucas lucas 1205595851 Jul 22  2022 MLFH010220190513-1.sorted.bam
# (but then pasted here for repeatability)

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

mkdir -p diversity-${scaling}
mkdir -p logs

echo "Start `date`"
START=$(date +%s.%N)

$GRENEDALF diversity \
    ${INPATHS} \
    --window-type genome \
    --filter-sample-min-count 2 \
    --filter-sample-min-read-depth 4 \
    --filter-sample-max-read-depth 1000 \
    --window-average-policy valid-snps \
    --pool-sizes 100 \
    --out-dir "diversity-${scaling}" \
    --file-suffix "-${OUT}" \
    --threads ${size} \
    --allow-file-overwriting \
    > "logs/diversity-${OUT}.log" 2>&1

#     --window-interval-width 1000 \

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
