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

# print(tmr_data)
# print(mem_data)

# Prepare nice plotting aestatics for each benchmark
markers = 'o'
dashes = {
    "grenedalf/diversity": (1,0),
    "grenedalf/fst": (1,0),
    "popoolation/fst": (5,2),
    "popoolation/diversity": (5,2),
    "npstat/diversity": (5,2),
    "poolfstat/fst": (5,2)
}
palette = {
    "grenedalf/diversity": "k",
    "grenedalf/fst": "k",
    "popoolation/fst": "C9",
    "popoolation/diversity": "C9",
    "npstat/diversity": "C7",
    "poolfstat/fst": "C3"
}
xticklabels = [
    "10K", "20K", "50K", "100K", "200K", "500K", "1M", "2M", "5M", "10M", "20M", "50M", "100M"
]

# ------------------------------------------------------------
#     read data and plot
# ------------------------------------------------------------

# Read the tables for timing and memory,
# using the two variables over which the benchmark runs varied.
tmr_data, mem_data = prepare_tables([ "window", "size" ])

# diversity
tmr_diversity, mem_diversity = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/diversity", "popoolation/diversity", "npstat/diversity" ],
    "window": [ 1000 ],
    "size": sizes
})
plot_all_tables(
    "Diversity", tmr_diversity, mem_diversity, '^', dashes, palette, xticklabels, markersize=8
)

# fst, window 0 (whole genome)
tmr_fst_0, mem_fst_0 = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ 0, 100000000 ],
    "size": sizes
})
plot_all_tables("FST (whole genome)", tmr_fst_0, mem_fst_0, 's', dashes, palette, xticklabels )

# fst, window 1
tmr_fst_1, mem_fst_1 = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ 1 ],
    "size": sizes
})
plot_all_tables("FST (Window 1)", tmr_fst_1, mem_fst_1, 's', dashes, palette, xticklabels )

# fst, window 1000
tmr_fst_1000, mem_fst_1000 = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ 1000, 100 ],
    "size": sizes
})
plot_all_tables("FST (Window 1000)", tmr_fst_1000, mem_fst_1000, 's', dashes, palette, xticklabels )
