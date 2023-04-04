#!/usr/bin/python3

# libraries
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import seaborn as sns
import os, sys
from matplotlib.ticker import FuncFormatter

# ------------------------------------------------------------
#     Settings
# ------------------------------------------------------------

# global names for our ins and outs
out_dir_png = "figures_png"
out_dir_svg = "figures_svg"
in_file_tmr = "measure_time.csv"
in_file_mem = "measure_memory.csv"

# ------------------------------------------------------------
#     read_benchmark_csv
# ------------------------------------------------------------

# Custom reading for our table format.
def read_benchmark_csv( infile, params, data_col_name ):
    # This is a bit weird, but based on the simple tab separated output of our benchmarks.
    # We wanted the benchmarks to report their params in every row, so that it's easy to
    # change and concat tables without losing header information.
    # So now, we have to clean up the mess here, and select only the columns that contain data...
    row_list=[]
    with open(infile, 'r') as f:
        for line in f:
            elems = line.strip().split('\t')
            if len(elems) != 3 + len(params) * 2:
                raise Exception( "Not right line len " + str(len(elems)) )
            entries = {
                "tool": elems[1],
                data_col_name: float(elems[len(params)*2 + 2])
            }
            for i in range(len(params)):
                if elems[2+2*i] != params[i]:
                    raise Exception("Invalid params")
                entries[params[i]] = int(elems[3+2*i])
            row_list.append(entries)
    columns = ["tool"] + params + [data_col_name]
    return pd.DataFrame(row_list, columns=columns)

# ------------------------------------------------------------
#     prepare_tables
# ------------------------------------------------------------

def prepare_tables(param_cols):
    # Read data
    tmr_file = in_file_tmr
    mem_file = in_file_mem
    tmr_data = read_benchmark_csv( tmr_file, param_cols, "time" )
    mem_data = read_benchmark_csv( mem_file, param_cols, "memory" )
    # tmr_data = pd.read_csv( tmr_file, sep="\t", header=None ) #, index_col=0 )
    # mem_data = pd.read_csv( mem_file, sep="\t", header=None ) #, index_col=0 )
    # print(tmr_data)
    # print(mem_data)

    # Convert time to minutes instead of seconds
    tmr_data["time"] = tmr_data["time"] / 60.0

    if len(tmr_data) != len(mem_data):
        raise Exception("Tables not matching")
    return ( tmr_data, mem_data )

# ------------------------------------------------------------
#     select_column_data
# ------------------------------------------------------------

def select_column_data_table( df, value_col, filter_cols_and_values ):
    df = df.copy()

    # Subset the table to where all criteria match
    for col, val in filter_cols_and_values.items():
        df = df.loc[df[col].isin(val)]

    # Turn to wide format
    df = df.pivot(index='size', columns='tool', values=value_col)

    # The wide format uses our "size" col as index, which screws up
    # the plotting, as it's not a linear scale. Reindex, and remove the size.
    df = df.reset_index().drop(columns="size")
    # print(df)
    return df

def select_column_data( time_data, memory_data, filter_cols_and_values ):
    return (
        select_column_data_table( time_data,   "time",   filter_cols_and_values ),
        select_column_data_table( memory_data, "memory", filter_cols_and_values )
    )

# ------------------------------------------------------------
#     plot_table
# ------------------------------------------------------------

plotnum = 1
def plot_table(
    title, data, measure, scale="lin",
    markers='o', dashes=(0, ""), palette='k', xticklabels=None, **kwargs
):
    global plotnum
    global out_dir_png
    global out_dir_svg

    # Create dirs for results
    if not os.path.exists(out_dir_png):
        os.makedirs(out_dir_png)
    if not os.path.exists(out_dir_svg):
        os.makedirs(out_dir_svg)

    # Make the tile
    if measure == "tmr":
        title += "  " + "(Runtime)"
    else:
        title += "  " + "(Memory)"

    # Scale to minutes or hours in linear case
    if measure == "tmr" and scale == "lin":
        data = data / 60.0

    # Seaborn can't deal with dicts properly, we need to translate to a list
    # of the values that are actually used, in the correct order...
    list_markers=[]
    list_dashes=[]
    list_palette=[]
    for col in data.columns.values:
        if type(markers) is dict:
            list_markers.append( markers[col] )
        else:
            list_markers.append( markers )
        if type(dashes) is dict:
            list_dashes.append( dashes[col] )
        else:
            list_dashes.append( dashes )
        if type(palette) is dict:
            list_palette.append( palette[col] )
        else:
            list_palette.append( palette )

    # Make the plot. Our data set sizes are roughly exponential,
    # so the x-axis already is kind of log scaled. Do the same for the y-axis.
    plt.figure( plotnum )
    ax = sns.lineplot(
        data=data, markers=list_markers, dashes=list_dashes, palette=list_palette, **kwargs
    )
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
            ax.set_ylabel('Runtime  [min]')
    elif measure == "mem":
    	ax.set_ylabel('Memory  [MB]')
    else:
        raise Exception( "Invalid measure" )

    # Set correct x axis labels. Nightmare.
    ax.set_xticks(list(), minor=False)
    ax.set_xticklabels('', minor=False)
    ax.set_xticks(list(range(len(xticklabels))), minor=True)
    if xticklabels:
        ax.set_xticklabels(xticklabels, minor=True)
    #ax.xaxis.grid(False, which='minor')
    plt.legend(title='')

    # Save to files
    testcase = title.lower().replace( " ", "-" )
    testcase = ''.join(c for c in testcase if c.isalnum() or c == '-')
    plt.savefig(out_dir_png + "/" + measure + "_" + testcase + "_" + scale + ".png", format='png')
    plt.savefig(out_dir_svg + "/" + measure + "_" + testcase + "_" + scale + ".svg", format='svg')
    plt.close( plotnum )
    plotnum += 1

# ------------------------------------------------------------
#     plot_all_tables
# ------------------------------------------------------------

def plot_all_tables(
    testcase, time_data, memory_data,
    markers='o', dashes=(0, ""), palette='k', xticklabels=None, **kwargs
):
    plot_table( testcase, time_data,   "tmr", "lin", markers, dashes, palette, xticklabels, **kwargs )
    plot_table( testcase, memory_data, "mem", "lin", markers, dashes, palette, xticklabels, **kwargs )
    plot_table( testcase, time_data,   "tmr", "log", markers, dashes, palette, xticklabels, **kwargs )
    plot_table( testcase, memory_data, "mem", "log", markers, dashes, palette, xticklabels, **kwargs )
