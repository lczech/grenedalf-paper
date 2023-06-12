#!/bin/bash

OUTFILE="collect.csv"

echo -e "Chr\tThreads\tTime" > ${OUTFILE}
for c in `seq 1 5`; do
        for i in `seq 1 16` ; do

                echo -ne "${c}\t${i}" >> ${OUTFILE}
                for run in `seq 1 3` ; do

                        echo -ne "\t" >> ${OUTFILE}
                        f="slurm-out-chr-${c}-threads-${i}-run-${run}.log"
                        cat ${f} | grep "Elapsed (wall clock) time (h:mm:ss or m:ss):" | sed "s/.* //g" | tr -d '\n' >> ${OUTFILE}

                done
                echo >> ${OUTFILE}
        done
done

