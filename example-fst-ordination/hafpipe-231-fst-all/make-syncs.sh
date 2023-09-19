#!/bin/bash

find /central/groups/carnegie_poc/lczech/grenephase1/hafpipe-231/samples/ -name *.csv > samples.txt
split -l 805 samples.txt

GRENEDALF=/central/home/lczech/software/grenedalf-latest/bin/grenedalf
REFGENOME=/central/groups/carnegie_poc/lczech/grenephase1/reference/TAIR10_chr_all.fa

for chunk in `ls xa*` ; do

	$GRENEDALF sync-file --frequency-table-path `cat $chunk | tr '\n' ' '` --reference-genome-file $REFGENOME --file-suffix "-${chunk}" --log-file "sync-${chunk}.log" --frequency-table-int-factor 1000 --compress

done


