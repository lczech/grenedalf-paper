#!/bin/bash

S1=/home/lucas/Projects/grenephase1/mapped/MLFH010120180409-1.sorted.bam
S2=/home/lucas/Projects/grenephase1/mapped/MLFH010120180409-2.sorted.bam

/bin/grenedalf sync-file --sam-path $S1 $S2 --filter-region "1"
