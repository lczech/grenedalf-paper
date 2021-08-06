#!/bin/bash

mkdir -p pileup
GRENEDALF="../../software/grenedalf/bin/grenedalf"

# Generate pileup files with one sample each
for s in 1000 2000 5000 10000 20000 50000 100000 200000 500000 1000000 2000000 5000000 10000000 20000000 50000000 100000000; do

	echo "At size $s"
	${GRENEDALF} simulate --format pileup --coverages "10/500" --length $s --mutation-rate 1e-1 --with-quality-scores > /dev/null
	mv "simulate.pileup" "pileup/random-${s}.pileup"

done
