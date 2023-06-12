#!/bin/bash

for CHR in `seq 1 5` ; do
  for THREADS in `seq 1 16` ; do
    for RUN in `seq 1 3`; do

        # we reserve some more cpus, just so that there are enough for async reading etc
        CPUS=$(( THREADS + 4 ))

        echo "chr ${CHR} threads ${THREADS}"
        cat template-fst-threads.sh | sed "s/#THREADS#/${THREADS}/g" | sed "s/#CPUS#/${CPUS}/g" | sed "s/#CHR#/${CHR}/g" | sed "s/#RUN#/${RUN}/g" > fst-threads-${CHR}-${THREADS}-${RUN}.sh
        chmod +x fst-threads-${CHR}-${THREADS}-${RUN}.sh
        sbatch fst-threads-${CHR}-${THREADS}-${RUN}.sh

    done
  done
done

