#!/usr/bin/env python3

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

# Number of samples for the scaling tests.
# We are on an 8-core system, so that's how far we go.
samples = [ 1, 2, 3, 4, 5, 6, 7, 8 ]

xlabel_scale = "Threads"
xticklabels = samples

all_markers = {
    "grenedalf/diversity-strong-bam": '>',
    "grenedalf/diversity-strong-sync": 's',
    "grenedalf/fst-strong-bam": '>',
    "grenedalf/fst-strong-sync": 's',
    "grenedalf/diversity-weak-bam": '>',
    "grenedalf/diversity-weak-sync": 's',
    "grenedalf/fst-weak-bam": '>',
    "grenedalf/fst-weak-sync": 's',
    "ideal": '.',
}
all_dashes = {
    "grenedalf/diversity-strong-bam": (1,1),
    "grenedalf/diversity-strong-sync": (1,1),
    "grenedalf/fst-strong-bam": (1,0),
    "grenedalf/fst-strong-sync": (1,0),
    "grenedalf/diversity-weak-bam": (1,1),
    "grenedalf/diversity-weak-sync": (1,1),
    "grenedalf/fst-weak-bam": (1,0),
    "grenedalf/fst-weak-sync": (1,0),
    "ideal": (1,0),
}
all_palette = {
    "grenedalf/diversity-strong-bam": "k",
    "grenedalf/diversity-strong-sync": "k",
    "grenedalf/fst-strong-bam": "k",
    "grenedalf/fst-strong-sync": "k",
    "grenedalf/diversity-weak-bam": "k",
    "grenedalf/diversity-weak-sync": "k",
    "grenedalf/fst-weak-bam": "k",
    "grenedalf/fst-weak-sync": "k",
    "ideal": 'C2',
}

# ------------------------------------------------------------
#     read data and plot
# ------------------------------------------------------------

# Read the tables for timing and memory
tmr_data, mem_data = prepare_tables([ "type", "size" ])
# print(tmr_data)
# print(mem_data)

# Add the ideal lines to it.
def add_ideal_line( time_data, measure ):
    # print(time_data)
    if measure == "strong":
        time_data['ideal'] = samples
    elif measure == "weak":
        time_data['ideal'] = [ 1 for x in samples ]
    return time_data

# Resources:
# https://hpc-wiki.info/hpc/Scaling

# -------------------------------
#     strong scaling
# -------------------------------

tmr_strong, mem_strong = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/diversity-strong", "grenedalf/fst-strong" ],
    "size": samples
}, "type" )

# Plot the raw time data
plot_all_tables(
    "Strong scaling", tmr_strong, mem_strong, xlabel_scale, xticklabels,
    markers=all_markers, dashes=all_dashes, palette=all_palette
)

# Compute the scaling: normalize to first row, i.e., single core.
for col in tmr_strong:
    tmr_strong[col] = tmr_strong[col][0] / tmr_strong[col]
tmr_strong = add_ideal_line( tmr_strong, "strong" )

# Plot the speedup
plot_all_tables(
    "Strong scaling speedup", tmr_strong, mem_strong, xlabel_scale, xticklabels,
    markers=all_markers, dashes=all_dashes, palette=all_palette, measure_1="strong"
)

# -------------------------------
#     weak scaling
# -------------------------------

tmr_weak, mem_weak = select_column_data( tmr_data, mem_data, {
    "tool": [ "grenedalf/diversity-weak", "grenedalf/fst-weak" ],
    "size": samples
}, "type" )

# Plot the raw time data
plot_all_tables(
    "Weak scaling", tmr_weak, mem_weak, xlabel_scale, xticklabels,
    markers=all_markers, dashes=all_dashes, palette=all_palette
)

# Compute the scaling: normalize to first row, i.e., single core, for diversity.
# For fst, which is computed _between_ populations, the first real case is 2 samples.
for col in tmr_weak:
    if tmr_weak[col][0] > 0.0:
        tmr_weak[col] = tmr_weak[col][0] / tmr_weak[col]
    else:
        tmr_weak[col] = tmr_weak[col][1] / tmr_weak[col]
tmr_weak = add_ideal_line( tmr_weak, "weak" )

# Plot the efficiency
plot_all_tables(
    "Weak scaling efficiency", tmr_weak, mem_weak, xlabel_scale, xticklabels,
    markers=all_markers, dashes=all_dashes, palette=all_palette, measure_1="weak"
)
