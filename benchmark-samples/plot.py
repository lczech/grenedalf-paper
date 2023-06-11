#!/usr/bin/env python3

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
tmr_file = "measure_time_transposed.csv"
mem_file = "measure_memory_transposed.csv"
tmr_data = pd.read_csv( tmr_file, sep="\t" ) #, index_col=0 )
mem_data = pd.read_csv( mem_file, sep="\t" ) #, index_col=0 )
#print tmr_data
#print mem_data

# Sort here. Grenedalf luckily is the first in the alphabet, so this is easy.
tmr_data = tmr_data.sort_values(tmr_data.columns[0])
mem_data = mem_data.sort_values(mem_data.columns[0])

# Types of tests that we have. Dict from name (title of the plot)
# to the lines in the measure scripts that we need to look for.
testcases = {
    "fst": [ "grenedalf", "poolfstat", "popoolation" ]
}

# Prepare fixed colors for each tool
line_colors = {
    "grenedalf": "k",
    "poolfstat": "C0",
    "popoolation2": "C3"
}

plotnum = 1
def plot_test(testname, data, measure, scale):
    global testcases
    global line_colors
    global plotnum

    min_x = 0 # first element. 0 based
    max_x = 4 # past the last element. 0 based
    title = testname
    if measure == "tmr":
        title += "  " + "(Runtime)"
    else:
        title += "  " + "(Memory)"

    # Make a new dataframe with just the needed content.
    sub_data = pd.DataFrame()
    line_styles = list()
    markers = list()
    grenedalf_indices = []
    for index, row in data.iterrows():
        found = False
        for tool in testcases[testname]:
            if tool in row[0]:
                found = True
        if not found:
            continue

        name = row[0].split(".")[0]
        data = list(row[min_x+1:max_x+1])
        # print(name)
        # print(data)

        # Scale to minutes or hours in linear case
        if measure == "tmr" and scale == "lin":
            data = [ d / 60.0 for d in data ]
            if testname == "diversity":
                data = [ d / 60.0 for d in data ]

        sub_data[name] = data

        # Make a special style for grenedalf: solid line.
        # All other tools get a dashed line.
        if "grenedalf" in name:
            line_styles.append("")
            # line_styles.insert(0, "")
            grenedalf_indices.append(len(list(sub_data))-1)
        else:
            line_styles.append((5,2))
            # if "fst" in name:
            #     line_styles.append((5,2))
            # else:
            #     # Small ink elements, with a sum of 9, so that we can divithe the offset in threes.
            #     # We do the offset in Inkscape though, as Seaborn/Matplotlib refuse to do that.
            #     line_styles.append((2,7))

        # Different marker types for different input file types or processing tools.
        # Bit messy, but gets the job done.
        if "-sync" in name:
            markers.append('s')
        elif "-mpileup" in name:
            markers.append('^')
        elif "-bam" in name:
            markers.append('>')
        elif "-java" in name:
            markers.append('D')
        elif "-perl" in name:
            markers.append('o')
        else:
            markers.append('o')

    # print(sub_data)
    # print(line_styles)

    # Move grenedalf column to front. It's the one we are interested in here.
    # --> Nope, too tricky to reorder the dashes and markers as well... we just sort the table
    #     in the beginning instead!
    # for grenedalf_index in grenedalf_indices:
    #     cols = list(sub_data)
    #     cols.insert(0, cols.pop(grenedalf_index))
    #     sub_data = sub_data.loc[:, cols]

    # Store row names, and rename them later. Seaborn does not want renaming upfront.
    # size_names = [ "10K", "20K", "50K", "100K", "200K", "500K", "1M", "2M", "5M", "10M" ]
    size_names = [ "2", "3", "4", "5" ]
    size_names = size_names[min_x:max_x]

    # Make the plot. Our data set sizes are roughly exponential,
    # so the x-axis already is kind of log scaled. Do the same for the y-axis.
    plt.figure( plotnum, figsize=(8,6) )
    ax = sns.lineplot( data=sub_data, markers=markers, dashes=line_styles, palette=line_colors )
    #dashes=False
    if scale == "log":
        ax.set_yscale('log')
    elif scale != "lin":
        raise Exception( "Invalid scale" )
    ax.yaxis.grid(True, which='major')
    # plt.tight_layout()
    plt.legend(loc='upper left')

    # # Why is it so damn complicated to just set an offset to the dashes?!
    # Screw it, using Inkscape for that!
    # for l in ax.lines:
    #     l.set_dashes(line_styles)
        # l.set_linestyle("--")

    # Nameing the plot and the axis.
    ax.set_title( title )
    #ax.set_xlabel('Dataset Size  [bytes]')
    ax.set_xlabel('Dataset Size  [number of samples]')
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
    plt.savefig(
        "figures_png/" + measure + "_" + testname + "_" + scale + ".png",
        format='png', bbox_inches="tight"
    )
    plt.savefig(
        "figures_svg/" + measure + "_" + testname + "_" + scale + ".svg",
        format='svg', bbox_inches="tight"
    )
    plt.close( plotnum )
    plotnum += 1

for testname in testcases:
    print( "Running", testname )

    plot_test(testname, tmr_data, "tmr", "lin")
    plot_test(testname, mem_data, "mem", "lin")
    plot_test(testname, tmr_data, "tmr", "log")
    plot_test(testname, mem_data, "mem", "log")
