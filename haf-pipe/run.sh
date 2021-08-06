#!/bin/bash

cd "$(dirname $0)/"
BASEDIR=`pwd`
export PATH="${BASEDIR}/harp_linux_140925_103521/bin:$PATH"
export PATH="${BASEDIR}/HAFpipe-line-master:$PATH"
HAFPIPE="${BASEDIR}/HAFpipe-line-master/HAFpipe_wrapper.sh"

OUTDIR="out"
mkdir -p ${OUTDIR}

# cd HAFpipe-line-master

FOUNDER="/home/lucas/Projects/1001g/1001gbi.recode.vcf.gz"
SUBSET="/home/lucas/Projects/grenedalf-paper/haf-pipe/founders.txt"

REF="/home/lucas/Dropbox/GitHub/grenepipe/test/reference/TAIR10_chr_all.fa"
BAM="/home/lucas/Projects/grenedalf-paper/benchmark-real/mapped/S1-1.sorted.bam"

${HAFPIPE} \
    -t 1,2,3,4 \
    -v ${FOUNDER} \
    -u ${SUBSET} \
    -c 1 \
    -s ${OUTDIR}/founderGenotypes.segregating.snpTable \
    -i simpute \
    -b ${BAM} \
    -e sanger \
    -g 2     \
    -r ${OUTDIR}/dmel_ref_r5.39.fa \
    -o ${OUTDIR}
