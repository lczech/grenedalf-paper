#!/usr/bin/python3

# libraries
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import seaborn as sns
import os
from matplotlib.ticker import FuncFormatter

# Create dirs for results
if not os.path.exists("figures_png"):
    os.makedirs("figures_png")
if not os.path.exists("figures_svg"):
    os.makedirs("figures_svg")

# Read data
tmr_file = "measure_time.csv"
mem_file = "measure_memory.csv"
tmr_data = pd.read_csv( tmr_file, sep="\t", header=None ) #, index_col=0 )
mem_data = pd.read_csv( mem_file, sep="\t", header=None ) #, index_col=0 )
#print tmr_data
#print mem_data

# Types of tests that we have. Dict from name (title of the plot)
# to the lines in the measure scripts that we need to look for.
testcases = {
    "diversity": [ "grenedalf/diversity", "popoolation/pi", "popoolation/theta", "popoolation/d" ],
    "fst": [ "grenedalf/fst", "popoolation/fst" ]
}

# Prepare fixed colors for each tool
line_colors = {
    "grenedalf/diversity": "k",
    "grenedalf/fst": "k",
    "popoolation/pi": "C2",
    "popoolation/theta": "C1",
    "popoolation/d": "C0",
    "popoolation/fst": "C6"
}

plotnum = 1
def plot_test(testname, data, measure, scale):
    global testcases
    global line_colors
    global plotnum

    min_x = 3 # first element. 0 based
    max_x = 16 # past the last element. 0 based
    title = testname
    if measure == "tmr":
        title += "  " + "(Runtime)"
    else:
        title += "  " + "(Memory)"

    # Make a new dataframe with just the needed content.
    sub_data = pd.DataFrame()
    line_styles = list()
    grenedalf_index = -1
    for index, row in data.iterrows():
        found = False
        for tool in testcases[testname]:
            if tool in row[0]:
                found = True
        if not found:
            continue

        name = row[0].split(".")[0]
        data = list(row[min_x+1:max_x+1])

        # Scale to minutes or hours in linear case
        if measure == "tmr" and scale == "lin":
            data = [ d / 60.0 for d in data ]
            if testname == "diversity":
                data = [ d / 60.0 for d in data ]

        sub_data[name] = data

        # Make a special style for grenedalf: solid line at the front of the list,
        # because we are going to move the grenedalf column to the front as well.
        # All other tools get a dashed line.
        if "grenedalf" in name:
            line_styles.insert(0, "")
            grenedalf_index = len(list(sub_data))-1
        else:
            line_styles.append((5,2))
            # if "fst" in name:
            #     line_styles.append((5,2))
            # else:
            #     # Small ink elements, with a sum of 9, so that we can divithe the offset in threes.
            #     # We do the offset in Inkscape though, as Seaborn/Matplotlib refuse to do that.
            #     line_styles.append((2,7))

    # Move grenedalf column to front. It's the one we are interested in here.
    cols = list(sub_data)
    cols.insert(0, cols.pop(grenedalf_index))
    sub_data = sub_data.loc[:, cols]

    # Store row names, and rename them later. Seaborn does not want renaming upfront.
    # size_names = [ "10K", "20K", "50K", "100K", "200K", "500K", "1M", "2M", "5M", "10M" ]
    size_names = [ "1K", "2K", "5K", "10K", "20K", "50K", "100K", "200K", "500K", "1M", "2M", "5M", "10M", "20M", "50M", "100M" ]
    size_names = size_names[min_x:max_x]

    # Make the plot. Our data set sizes are roughly exponential,
    # so the x-axis already is kind of log scaled. Do the same for the y-axis.
    plt.figure( plotnum )
    ax = sns.lineplot( data=sub_data, marker="o", dashes=line_styles, palette=line_colors )
    #dashes=False
    if scale == "log":
        ax.set_yscale('log')
    elif scale != "lin":
        raise Exception( "Invalid scale" )
    ax.yaxis.grid(True, which='major')
    # plt.tight_layout()

    # # Why is it so damn complicated to just set an offset to the dashes?!
    # Screw it, using Inkscape for that!
    # for l in ax.lines:
    #     l.set_dashes(line_styles)
        # l.set_linestyle("--")

    # Nameing the plot and the axis.
    ax.set_title( title )
    #ax.set_xlabel('Dataset Size  [bytes]')
    ax.set_xlabel('Dataset Size  [rows]')
    if measure == "tmr":
        ax.set_ylabel('Runtime  [s]')

        # Scale to minutes in linear case
        if scale == "lin":
            if testname == "diversity":
                ax.set_ylabel('Runtime  [h]')
            else:
                ax.set_ylabel('Runtime  [min]')

    else:
    	ax.set_ylabel('Memory  [MB]')

    # Set correct x axis labels. Nightmare.
    ax.set_xticks(list(), minor=False)
    ax.set_xticklabels('', minor=False)
    ax.set_xticks(list(range(max_x-min_x)), minor=True)
    ax.set_xticklabels(size_names, minor=True)
    #ax.xaxis.grid(False, which='minor')

    # Save to files
    plt.savefig("figures_png/" + measure + "_" + testname + "_" + scale + ".png", format='png')
    plt.savefig("figures_svg/" + measure + "_" + testname + "_" + scale + ".svg", format='svg')
    plt.close( plotnum )
    plotnum += 1

for testname in testcases:
    print( "Running", testname )

    plot_test(testname, tmr_data, "tmr", "lin")
    plot_test(testname, mem_data, "mem", "lin")
    plot_test(testname, tmr_data, "tmr", "log")
    plot_test(testname, mem_data, "mem", "log")
