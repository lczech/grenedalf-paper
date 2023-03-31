#!/bin/bash

####################################################################################################
#     Main Loop
####################################################################################################

# Change to test dir. This ensures that the script can be called from any directory.
cd "$(dirname "$0")"

GRENEDALF="../software/grenedalf/bin/grenedalf"
mkdir -p "grenedalf-logs"

# directory with the samples we are using
MAPPED="/home/lucas/Projects/grenephase1/mapped"

mkdir -p "sample-sync"

# we create the sync files on the fly, and might delete them afterwards,
# as they otherwise take up too much disk space for my poor little laptop ;-)
# that is a bit wasteful when repeating the measurement, but we can live with it.
for NUMSAM in `seq 2 5` ; do
    echo `date`" - creating sync for ${NUMSAM} samples"

    # select the first n samples, and create a sync file from them
    DATA=`ls ${MAPPED}/*.bam | sort | head -n ${NUMSAM}`
    
    # build command line for grenedalf
    INPATHS=""
    for D in ${DATA} ; do
        INPATHS="${INPATHS} --sam-path ${D}"
    done

    # run grenedalf to get a sync file
    if [ ! -f "sample-sync/counts-${NUMSAM}.sync" ] ; then
        ${GRENEDALF} sync-file ${INPATHS} --allow-file-overwriting --out-dir "sample-sync" --file-suffix "-${NUMSAM}" \
            > "grenedalf-logs/sync-samples-${NUMSAM}.log" 2>&1
    fi
done

