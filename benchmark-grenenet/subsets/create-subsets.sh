#!/bin/bash

GRENEDALF="/home/lucas/Dropbox/GitHub/grenedalf/bin/grenedalf"

# we pick two files that are close to the average file size of our test samples.
# avg size: `ls -l *.bam | gawk '{sum += $5; n++;} END {print sum/n;}'`
# --> 1.00353e+09
bam1="/home/lucas/Projects/grenephase1/mapped/MLFH010120200420-1.sorted.bam"
bam2="/home/lucas/Projects/grenephase1/mapped/MLFH010420180518-1.sorted.bam"
FASTA="../TAIR10_chr_all.fa"

# We use the fai file of the TAIR10 reference genome to define regions to match with our expected sizes:
# 1000 2000 5000 10000 20000 50000 100000 200000 500000 1000000 2000000 5000000 10000000 20000000 50000000 100000000

# fai
#   1	30427671	71	79	80
#   2	19698289	30812975	79	80
#   3	23459830	50760682	79	80
#   4	18585056	74517544	79	80
#   5	26975502	93337926	79	80
#   mitochondria	366924	120654974	79	80
#   chloroplast	154478	121026625	79	80

# --> using script ./ref_lengths.py to get the needed region specifiers for samtools view
# this produces "ref_lengths.txt", which contains the chunk sizes and their regions that we use here.
if [ ! -f ref_lengths.txt ] ; then
    ./ref_lengths.py
fi

# sam tools needs the bams to be indexed
if [ ! -f ${bam1}.bai ] ; then
    echo "indexing ${bam1}"
    samtools index $bam1
fi
if [ ! -f ${bam2}.bai ] ; then
    echo "indexing ${bam2}"
    samtools index $bam2
fi

# create the dirs where we output stuff
# rm -rf "grenedalf-logs"
# rm -rf "samtools-logs"
# rm -rf "../subsets-bam"
# rm -rf "../subsets-mpileup"
# rm -rf "../subsets-sync"
# rm -rf "../subsets-table"
mkdir -p "grenedalf-logs"
mkdir -p "samtools-logs"
mkdir -p "../subsets-bam"
mkdir -p "../subsets-mpileup"
mkdir -p "../subsets-sync"
mkdir -p "../subsets-table"

while read -r line; do

    chunk=`echo "$line" | cut -f1`
    region=`echo "$line" | cut -f2`
    echo "processing $chunk"

    # output bam files with chunks of the data
    chunkbam1="../subsets-bam/S1-${chunk}.bam"
    chunkbam2="../subsets-bam/S2-${chunk}.bam"

    # create subset bam files with up to the chunk regions of content
    # apparently, the documented long form options do not work with my version of samtools...
    # using the unreadable shorthand instead here...
    if [ ! -f ${chunkbam1} ] ; then
        echo "    samtools view S1"
        samtools view -h -b -o "${chunkbam1}" ${bam1} ${line} \
            > "samtools-logs/view-S1-${chunk}.log" 2>&1
    fi
    if [ ! -f ${chunkbam2} ] ; then
        echo "    samtools view S2"
        samtools view -h -b -o "${chunkbam2}" ${bam2} ${line} \
            > "samtools-logs/view-S2-${chunk}.log" 2>&1
    fi

    # turn the data into mpileup, so that all of that is available for speed testing later.
    # we will also create some of these files again during the speed tests, but do that in
    # different directories, in order to have the tests be independent of their order,
    # and be able to execute them independently from each other.
    chunkmpileup1="../subsets-mpileup/S1-${chunk}.mpileup"
    chunkmpileup2="../subsets-mpileup/S2-${chunk}.mpileup"
    chunkmpileup12="../subsets-mpileup/S1S2-${chunk}.mpileup"
    if [ ! -f ${chunkmpileup1} ] ; then
        echo "    samtools mpileup S1"
        samtools mpileup -f ${FASTA} -R -B -o "${chunkmpileup1}" ${chunkbam1} \
            > "samtools-logs/mpileup-S1-${chunk}.log" 2>&1
    fi
    if [ ! -f ${chunkmpileup2} ] ; then
        echo "    samtools mpileup S2"
        samtools mpileup -f ${FASTA} -R -B -o "${chunkmpileup2}" ${chunkbam2} \
            > "samtools-logs/mpileup-S2-${chunk}.log" 2>&1
    fi
    if [ ! -f ${chunkmpileup12} ] ; then
        echo "    samtools mpileup S1S2"
        samtools mpileup -f ${FASTA} -R -B -o "${chunkmpileup12}" ${chunkbam1} ${chunkbam2} \
            > "samtools-logs/mpileup-S2-${chunk}.log" 2>&1
    fi

    # for the same reasons, also create sync files for all files.
    # here, we also combine them into one, for FST.
    chunksync1="../subsets-sync/S1-${chunk}.sync"
    chunksync2="../subsets-sync/S2-${chunk}.sync"
    chunksync12="../subsets-sync/S1S2-${chunk}.sync"
    if [ ! -f ${chunksync1} ] ; then
        echo "    grenedalf sync S1"
        ${GRENEDALF} sync-file --sam-path ${chunkbam1} --allow-file-overwriting \
            > "grenedalf-logs/sync-S1-${chunk}.log" 2>&1
        mv "counts.sync" ${chunksync1}
    fi
    if [ ! -f ${chunksync2} ] ; then
        echo "    grenedalf sync S2"
        ${GRENEDALF} sync-file --sam-path ${chunkbam2} --allow-file-overwriting \
            > "grenedalf-logs/sync-S2-${chunk}.log" 2>&1
        mv "counts.sync" ${chunksync2}
    fi
    if [ ! -f ${chunksync12} ] ; then
        echo "    grenedalf sync S1S2"
        ${GRENEDALF} sync-file --sam-path ${chunkbam1} --sam-path ${chunkbam2} \
            --allow-file-overwriting > "grenedalf-logs/sync-S1S2-${chunk}.log" 2>&1
        mv "counts.sync" ${chunksync12}
    fi

    # aaaand frequency tables, same deal
    chunktable1="../subsets-table/S1-${chunk}.csv"
    chunktable2="../subsets-table/S2-${chunk}.csv"
    chunktable12="../subsets-table/S1S2-${chunk}.csv"
    if [ ! -f ${chunktable1} ] ; then
        echo "    grenedalf table S1"
        ${GRENEDALF} frequency --write-sample-counts --sam-path ${chunkbam1} \
            --allow-file-overwriting > "grenedalf-logs/table-S1-${chunk}.log" 2>&1
        mv "frequency.csv" ${chunktable1}
    fi
    if [ ! -f ${chunktable2} ] ; then
        echo "    grenedalf table S2"
        ${GRENEDALF} frequency --write-sample-counts --sam-path ${chunkbam2} \
            --allow-file-overwriting > "grenedalf-logs/table-S2-${chunk}.log" 2>&1
        mv "frequency.csv" ${chunktable2}
    fi
    if [ ! -f ${chunktable12} ] ; then
        echo "    grenedalf table S1S2"
        ${GRENEDALF} frequency --write-sample-counts --sam-path ${chunkbam1} --sam-path ${chunkbam2} \
            --allow-file-overwriting > "grenedalf-logs/table-S1S2-${chunk}.log" 2>&1
        mv "frequency.csv" ${chunktable12}
    fi

done < ref_lengths.txt
