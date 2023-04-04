#!/usr/bin/python3

import sys, os

# Make sure we are in the script dir
os.chdir(os.path.dirname(sys.argv[0]))

# Such a cheat to import stuff in python...
# See https://stackoverflow.com/a/22956038
sys.path.insert(0, '../common')
from plot import *

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

# Read the tables for timing and memory
tmr_data, mem_data = prepare_tables([ "size" ])
xlabel_scale = "genome positions"
# print(tmr_data)
# print(mem_data)

# convert
tmr_convert, mem_convert = select_column_data( tmr_data, mem_data, {
    "tool": [
        "samtools/mpileup", "grenedalf/sync-bam", "grenedalf/sync-mpileup",
        "popoolation/sync-perl", "popoolation/sync-java"
    ],
    "size": sizes
})
plot_all_tables( "Conversions", tmr_convert, mem_convert, xlabel_scale )

# diversity
tmr_diversity, mem_diversity = select_column_data( tmr_data, mem_data, {
    "tool": [
        "grenedalf/diversity-bam", "grenedalf/diversity-mpileup", "grenedalf/diversity-sync",
        "popoolation/diversity", "npstat/diversity"
    ],
    "size": sizes
})
plot_all_tables( "Diversity", tmr_diversity, mem_diversity, xlabel_scale )

# fst
tmr_fst, mem_fst = select_column_data( tmr_data, mem_data, {
    "tool": [
        "grenedalf/fst-bam", "grenedalf/fst-mpileup", "grenedalf/fst-sync",
        "popoolation/fst", "poolfstat/fst"
    ],
    "size": sizes
})
plot_all_tables( "FST (Window 1000)", tmr_fst, mem_fst, xlabel_scale )
