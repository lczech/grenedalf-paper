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

# Number of threads used in this scaling tests.
threads = list(range(1,17))
xlabel_scale = "Threads"
xticklabels = threads

all_markers = {
    "Chr1": 's',
    "Chr2": 's',
    "Chr3": 's',
    "Chr4": 's',
    "Chr5": 's',
    "ideal": '.',
}
all_dashes = {
    "Chr1": (1,0),
    "Chr2": (1,0),
    "Chr3": (1,0),
    "Chr4": (1,0),
    "Chr5": (1,0),
    "ideal": (1,0),
}

pal = sns.color_palette('crest_r', 8)
all_palette = {
    "Chr1": pal[0],
    "Chr2": pal[1],
    "Chr3": pal[2],
    "Chr4": pal[3],
    "Chr5": pal[4],
    "ideal": 'C2',
}

# ------------------------------------------------------------
#     read data and plot
# ------------------------------------------------------------

data = pd.read_csv( "times.csv", sep="\t" ).drop(columns="Threads")
# print(data)

# -------------------------------
#     strong scaling
# -------------------------------

# Plot the time data
plot_table(
    "Strong scaling", data, "scaling-tmr", xlabel_scale, "lin", xticklabels,
    markers=all_markers, dashes=all_dashes, palette=all_palette
)

# Compute the scaling: normalize to first row, i.e., single core.
for col in data:
    data[col] = data[col][0] / data[col]

# Add the ideal lines to it.
data['ideal'] = threads

# Plot the speedup
plot_table(
    "Strong scaling speedup", data, "strong", xlabel_scale, "lin", xticklabels,
    markers=all_markers, dashes=all_dashes, palette=all_palette
)
