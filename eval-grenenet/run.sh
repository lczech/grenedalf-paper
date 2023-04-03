#!/bin/bash

cd grenedalf

echo "Run Fst"
./fst.sh "../sync/all_counts.sync"

echo "Run d on S1"
./diversity.sh "../mpileup/S1.mpileup"

echo "Run d on S2"
./diversity.sh "../mpileup/S2.mpileup"

cd ../popoolation

echo "Run Fst"
./fst.sh "../sync/all_counts.sync"

echo "Run d on S1"
./diversity.sh "../mpileup/S1.mpileup" "d"

echo "Run d on S2"
./diversity.sh "../mpileup/S2.mpileup" "d"

