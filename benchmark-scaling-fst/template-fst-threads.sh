#!/bin/bash
#SBATCH --cpus-per-task=#CPUS#
#SBATCH --nodes=1
#SBATCH --ntasks 1
#SBATCH --time=7-0
#SBATCH --mem=20G
#SBATCH --output=slurm-out-chr-#CHR#-threads-#THREADS#-run-#RUN#.log
#SBATCH --constraint=skylake

lscpu

RUN=#RUN#
THREADS=#THREADS#
CHR=#CHR#

GRENEDALF=/central/home/lczech/software/grenedalf-latest/bin/grenedalf
SAMPLES=/central/groups/carnegie_poc/lczech/grenephase1/hafpipe-231-fst-all/scaling-chromosomes-avg/chr-${CHR}

echo "threads ${THREADS}"

date
/usr/bin/time -v ${GRENEDALF} fst --sync-path ${SAMPLES} --filter-region "${CHR}" --window-type genome --method unbiased-nei --pool-sizes 100 --threads ${THREADS} --log-file fst-${CHR}-${THREADS}-${RUN}.log --allow-file-overwriting --file-suffix "-${CHR}-${THREADS}-${RUN}"
date


