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

# Read the tables for timing and memory,
# using the two variables over which the benchmark runs varied.
tmr_data, mem_data = prepare_tables([ "window", "size" ])
xlabel_scale = "rows"
# print(tmr_data)
# print(mem_data)

# diversity
tmr_diversity, mem_diversity = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/diversity", "popoolation/diversity", "npstat/diversity" ],
    "window": [ 1000 ],
    "size": sizes
})
plot_all_tables( "Diversity", tmr_diversity, mem_diversity, xlabel_scale, markersize=8 )

# fst, window 0 (whole genome)
tmr_fst_0, mem_fst_0 = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ 0, 100000000 ],
    "size": sizes
})
plot_all_tables("FST (whole genome)", tmr_fst_0, mem_fst_0, xlabel_scale )

# fst, window 1
tmr_fst_1, mem_fst_1 = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ 1 ],
    "size": sizes
})
plot_all_tables("FST (Window 1)", tmr_fst_1, mem_fst_1, xlabel_scale )

# fst, window 1000
tmr_fst_1000, mem_fst_1000 = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/fst", "popoolation/fst", "poolfstat/fst" ],
    "window": [ 1000, 100 ],
    "size": sizes
})
plot_all_tables("FST (Window 1000)", tmr_fst_1000, mem_fst_1000, xlabel_scale )
