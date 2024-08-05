#!/bin/bash

MPILEUP="../benchmark-grenenet/data/subsets-mpileup/S1-20000000.mpileup"
SYNC="../benchmark-grenenet/data/subsets-sync/S1S2-20000000.sync"

mkdir chunks_mpileup
mkdir chunks_sync

# Create chunks of 1000 lines
split -l 1000 -a 4 ${MPILEUP} chunks_mpileup/split_
split -l 1000 -a 4 ${SYNC} chunks_sync/split_

# We now need to adjust the positions in the files... the files do not contain all lines,
# and gaps throw off the interval window counting of the downstream tools, so that sometimes
# there are two windows with data... we avoid that by simply reassigning consecutive numbers.

cd chunks_mpileup
for f in `ls split_*` ; do
    cat $f | awk -v OFS='\t' -v n=0 '{$2=++n} {print}' > tmp
    rm $f
    mv tmp $f
done
cd -

cd chunks_sync
for f in `ls split_*` ; do
    cat $f | awk -v OFS='\t' -v n=0 '{$2=++n} {print}' > tmp
    rm $f
    mv tmp $f
done
cd -
