#!/bin/bash

echo "Start `date`"

GRENEDALF="../software/grenedalf/bin/grenedalf"
DATA="data"
TAJIMA="tajima-d"
WINDIR="windows"
# ERRLOG="debug"

mkdir -p ${WINDIR}
# mkdir -p ${ERRLOG}
rm -f "${WINDIR}/window-*.csv"
rm -f "${WINDIR}/window-*.pdf"

POOLSIZES="10 20 50 100 200 500 1000"
MINCOVS="2 4 8 16 32"
# WINDOWS="10 100 1000 10000"
WINDOWS="5 10 20 50 100 200 500 1000"
PDFS=""

# Simulate different scenarios of variable combinations that are relevent in the context of the bug.
for poolsize in ${POOLSIZES} ; do
    echo "At pool size ${poolsize}"

    # Generate random date to test
    ${GRENEDALF} simulate \
    --pool-sizes ${poolsize} \
    --length 1000000 \
    --mutation-rate 1e-1 \
    --with-quality-scores \
    --format sync \
    --file-suffix "-${poolsize}" \
    --out-dir ${DATA} \
    --allow-file-overwriting \
    > /dev/null
done

# Go through the data in the other loop order,
# to produce the result table with the desired column order.
for window in ${WINDOWS} ; do
    echo "At window ${window}"
    for mincov in ${MINCOVS} ; do
        for poolsize in ${POOLSIZES} ; do
            if [ "$(( mincov * 3 ))" -ge "${poolsize}" ] ; then
                continue
            fi

            # Run with the bugs
            ${GRENEDALF} diversity \
                --sync-file "${DATA}/simulate-${poolsize}.sync" \
                --popoolation-corrected-tajimas-d \
                --pool-sizes ${poolsize} \
                --measure tajimas-d \
                --min-coverage ${mincov} \
                --window-width ${window} \
                --popoolation-format \
                --file-suffix "-${window}-${mincov}-${poolsize}-bug" \
                --out-dir ${TAJIMA} \
                --allow-file-overwriting \
                > /dev/null
                # 2> ${ERRLOG}/${window}-${mincov}-${poolsize}-bug.log

            # Run without the bugs
            ${GRENEDALF} diversity \
                --sync-file "${DATA}/simulate-${poolsize}.sync" \
                --pool-sizes ${poolsize} \
                --measure tajimas-d \
                --min-coverage ${mincov} \
                --window-width ${window} \
                --popoolation-format \
                --file-suffix "-${window}-${mincov}-${poolsize}-fix" \
                --out-dir ${TAJIMA} \
                --allow-file-overwriting \
                > /dev/null
                # 2> ${ERRLOG}/${window}-${mincov}-${poolsize}-fix.log

            # Extract the interesting columns of both and put them in one table.
            # Unfortunately, paste cannot work on the same input and output file...
            cut -f 5 "${TAJIMA}/diversity-1-tajimas-d-${window}-${mincov}-${poolsize}-bug.csv" > bug.csv
            cut -f 5 "${TAJIMA}/diversity-1-tajimas-d-${window}-${mincov}-${poolsize}-fix.csv" > fix.csv
            paste bug.csv fix.csv > raw.csv

            # Compute the element wise quotient of bug/fix.
            echo "${mincov};${poolsize}" > div.csv
            # awk '{ print $1/$2 }' raw.csv >> div.csv 2> /dev/null
            awk '{ if ( $2 == 0.0 || $2 == "na" ) print "NaN"; else print $1/$2; }' raw.csv >> div.csv
            # LINES=`cat div.csv | wc -l`
            # if [[ "${LINES}" != "100001" ]]; then
            #     echo "fail"
            #     exit
            # fi

            # Add the column to the results.
            # We need a bit of trickery to get paste to work for adding things to an existing file...
            if [ -f "${WINDIR}/window-${window}.csv" ]; then
                paste ${WINDIR}/window-${window}.csv div.csv > ${WINDIR}/window-${window}.tmp
                rm ${WINDIR}/window-${window}.csv
                mv ${WINDIR}/window-${window}.tmp ${WINDIR}/window-${window}.csv
            else
                cp div.csv ${WINDIR}/window-${window}.csv
            fi

            # Remove our intermediate files again.
            rm bug.csv fix.csv raw.csv div.csv

        done
    done

    # Run the plot tool
    ./plot.py ${WINDIR}/window-${window}.csv

    # Prepare the list of pdfs in order
    PDFS="${PDFS} ${WINDIR}/window-${window}.pdf"
done

# Make one pdf with all of them
pdftk ${PDFS} cat output results.pdf

echo "End `date`"
