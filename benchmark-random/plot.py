#!/usr/bin/python3

import sys, os

# Make sure we are in the script dir
os.chdir(os.path.dirname(sys.argv[0]))

# Such a cheat to import stuff in python...
# See https://stackoverflow.com/a/22956038
sys.path.insert(0, '../common')
from plot_benchmark import *

# ------------------------------------------------------------
#     plot aestatics
# ------------------------------------------------------------

# We use the same dataset sizes throughout the benchmarks.
# We here leave out 1k - 5k, as they are too small and not informative.
sizes = [
    10000, 20000, 50000, 100000, 200000, 500000, 1000000,
    2000000, 5000000, 10000000, 20000000, 50000000, 100000000
]

# ------------------------------------------------------------
#     read data and plot
# ------------------------------------------------------------

# Read the tables for timing and memory,
# using the two variables over which the benchmark runs varied.
tmr_data, mem_data = prepare_tables([ "window", "size" ])
xlabel_scale = "rows"
# print(tmr_data)
# print(mem_data)

# Nicer names. The "0" option is for grenedalf and poolfstat as a "whole genome" marker,
# while popoolation does not support whole genome, so we used a large window instead.
tmr_data = tmr_data.replace({"window": { 0: "WG", 100000000: "WG", 1: "SNP" }})
mem_data = mem_data.replace({"window": { 0: "WG", 100000000: "WG", 1: "SNP" }})

# # diversity
tmr_diversity, mem_diversity = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/diversity", "popoolation/diversity", "npstat/diversity" ],
    "window": [ 1000 ],
    "size": sizes
})
plot_all_tables( "Diversity", tmr_diversity, mem_diversity, xlabel_scale, markersize=8 )

# fst, window 0 (whole genome)
tmr_fst_0, mem_fst_0 = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ "WG" ],
    "size": sizes
})
plot_all_tables("FST (whole genome)", tmr_fst_0, mem_fst_0, xlabel_scale )

# fst, window 1
tmr_fst_1, mem_fst_1 = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ "SNP" ],
    "size": sizes
})
plot_all_tables("FST (single SNPs)", tmr_fst_1, mem_fst_1, xlabel_scale )

# fst, window 1000
tmr_fst_1000, mem_fst_1000 = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ 1000, 100 ],
    "size": sizes
})
plot_all_tables("FST (1000 bp / 100 SNPs windows)", tmr_fst_1000, mem_fst_1000, xlabel_scale )

# fst, window 1 and whole genome
tmr_fst_1_wg, mem_fst_1_wg = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ "SNP", "WG" ],
    "size": sizes
}, "window" )
plot_all_tables("FST (single SNPs and whole genome)", tmr_fst_1_wg, mem_fst_1_wg, xlabel_scale )
