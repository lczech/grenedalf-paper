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
out_dir_pdf = "figures_pdf"
out_dir_svg = "figures_svg"
in_file_tmr = "measure_time.csv"
in_file_mem = "measure_memory.csv"

# Prepare nice plotting aestatics for each benchmark
# Colors: https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html
all_markers = {
    "grenedalf/diversity": '^',
    "grenedalf/diversity-bam": '>',
    "grenedalf/diversity-mpileup": '^',
    "grenedalf/diversity-sync": 's',
    "grenedalf/fst": 's',
    "grenedalf/fst-SNP": 's',
    "grenedalf/fst-WG": 's',
    "grenedalf/fst-bam": '>',
    "grenedalf/fst-mpileup": '^',
    "grenedalf/fst-sync": 's',
    "grenedalf/sync-bam": '>',
    "grenedalf/sync-mpileup": '^',
    "npstat/diversity": '^',
    "poolfstat/fst": 's',
    "poolfstat/fst-SNP": 's',
    "poolfstat/fst-WG": 's',
    "popoolation/diversity": '^',
    "popoolation/fst": 's',
    "popoolation/fst-SNP": 's',
    "popoolation/fst-WG": 's',
    "popoolation/sync-java": 'D',
    "popoolation/sync-perl": 'o',
    "samtools/mpileup": 'o',
}
all_dashes = {
    "grenedalf/diversity": (1,0),
    "grenedalf/diversity-bam": (1,0),
    "grenedalf/diversity-mpileup": (1,0),
    "grenedalf/diversity-sync": (1,0),
    "grenedalf/fst": (1,0),
    "grenedalf/fst-SNP": (1,1),
    "grenedalf/fst-WG": (1,0),
    "grenedalf/fst-bam": (1,0),
    "grenedalf/fst-mpileup": (1,0),
    "grenedalf/fst-sync": (1,0),
    "grenedalf/sync-bam": (1,0),
    "grenedalf/sync-mpileup": (1,0),
    "npstat/diversity": (5,2),
    "poolfstat/fst": (5,2),
    "poolfstat/fst-SNP": (1,1),
    "poolfstat/fst-WG": (1,0),
    "popoolation/diversity": (5,2),
    "popoolation/fst": (5,2),
    "popoolation/fst-SNP": (1,1),
    "popoolation/fst-WG": (1,0),
    "popoolation/sync-java": (5,2),
    "popoolation/sync-perl": (5,2),
    "samtools/mpileup": (5,2),
}
all_palette = {
    "grenedalf/diversity": "k",
    "grenedalf/diversity-bam": "k",
    "grenedalf/diversity-mpileup": "k",
    "grenedalf/diversity-sync": "k",
    "grenedalf/fst": "k",
    "grenedalf/fst-SNP": "k",
    "grenedalf/fst-WG": "k",
    "grenedalf/fst-bam": "k",
    "grenedalf/fst-mpileup": "k",
    "grenedalf/fst-sync": "k",
    "grenedalf/sync-bam": "k",
    "grenedalf/sync-mpileup": "k",
    "npstat/diversity": "C7",
    "poolfstat/fst": "C3",
    "poolfstat/fst-SNP": "C3",
    "poolfstat/fst-WG": "C3",
    "popoolation/diversity": "C9",
    "popoolation/fst": "C9",
    "popoolation/fst-SNP": "C9",
    "popoolation/fst-WG": "C9",
    "popoolation/sync-java": "C9",
    "popoolation/sync-perl": "C9",
    "samtools/mpileup": "C5",
}
size_xticklabels = [
    "10K", "20K", "50K", "100K", "200K", "500K", "1M", "2M", "5M", "10M", "20M", "50M", "100M"
]

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
                raise Exception( "Not right line len: " + line )
            entries = {
                "tool": elems[1],
                data_col_name: float(elems[len(params)*2 + 2])
            }
            for i in range(len(params)):
                if elems[2+2*i] != params[i]:
                    raise Exception("Invalid params")
                try:
                    entries[params[i]] = int(elems[3+2*i])
                except Exception as e:
                    entries[params[i]] = elems[3+2*i]
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
    # tmr_data["time"] = tmr_data["time"] / 60.0

    if len(tmr_data) != len(mem_data):
        raise Exception("Tables not matching")
    return ( tmr_data, mem_data )

# ------------------------------------------------------------
#     select_column_data
# ------------------------------------------------------------

def select_column_data_table( df, value_col, filter_cols_and_values, rename=None ):
    df = df.copy()

    # Subset the table to where all criteria match
    for col, val in filter_cols_and_values.items():
        df = df.loc[df[col].isin(val)]

    # If we need to rename columns (in order to avoid clashes, such as when plotting
    # multiple window sizes in one plot), we apply that here, using the given column to rename.
    if rename:
        df["tool"] = df["tool"] + '-' + df[rename].astype(str)
        df = df.drop(columns=rename)

    # Turn to wide format
    df = df.pivot(index='size', columns='tool', values=value_col)

    # The wide format uses our "size" col as index, which screws up
    # the plotting, as it's not a linear scale. Reindex, and remove the size.
    df = df.reset_index().drop(columns="size")
    # print(df)
    return df

def select_column_data( time_data, memory_data, filter_cols_and_values, rename=None ):
    return (
        select_column_data_table( time_data,   "time",   filter_cols_and_values, rename ),
        select_column_data_table( memory_data, "memory", filter_cols_and_values, rename )
    )

# ------------------------------------------------------------
#     plot_table
# ------------------------------------------------------------

plotnum = 1
def plot_table(
    title, data, measure, xlabel_scale, yscale="lin", xticklabels=None,
    markers='o', dashes=(0, ""), palette='k', **kwargs
):
    global plotnum
    global out_dir_png
    global out_dir_pdf
    global out_dir_svg

    # Create dirs for results
    if not os.path.exists(out_dir_png):
        os.makedirs(out_dir_png)
    if not os.path.exists(out_dir_pdf):
        os.makedirs(out_dir_pdf)
    if not os.path.exists(out_dir_svg):
        os.makedirs(out_dir_svg)

    # Make the tile
    if measure == "tmr":
        fulltitle = "Runtime:  " + title
    elif measure == "mem":
        fulltitle = "Memory:  " + title
    else:
        fulltitle = title

    # Scale to minutes or hours in linear case
    if measure == "tmr" and yscale == "lin":
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
    # plt.figure( plotnum )
    plt.figure( plotnum, figsize=(8,6) )
    ax = sns.lineplot(
        data=data, markers=list_markers, dashes=list_dashes, palette=list_palette, **kwargs
    )
    if yscale == "log":
        ax.set_yscale('log')
    elif yscale != "lin":
        raise Exception( "Invalid scale" )
    ax.yaxis.grid(True, which='major')
    # plt.tight_layout()

    # # Why is it so damn complicated to just set an offset to the dashes?!
    # Screw it, using Inkscape for that!
    # for l in ax.lines:
    #     l.set_dashes(line_styles)
        # l.set_linestyle("--")

    # Nameing the plot and the axis.
    ax.set_title( fulltitle )
    #ax.set_xlabel('Dataset Size  [bytes]')
    ax.set_xlabel('Dataset Size  [' + xlabel_scale + ']')
    if measure == "tmr":
        ax.set_ylabel('Runtime  [s]')

        # Scale to minutes in linear case
        if yscale == "lin":
            ax.set_ylabel('Runtime  [min]')
    elif measure == "mem":
    	ax.set_ylabel('Memory  [MB]')
    elif measure == "strong":
        ax.set_ylabel('Speedup')
    elif measure == "weak":
        ax.set_ylabel('Efficieny')
    else:
        raise Exception( "Invalid measure" )

    # Set correct x axis labels. Nightmare.
    ax.set_xticks(list(), minor=False)
    ax.set_xticklabels('', minor=False)
    if xticklabels:
        ax.set_xticks(list(range(len(xticklabels))), minor=True)
        ax.set_xticklabels(xticklabels, minor=True)
    #ax.xaxis.grid(False, which='minor')
    plt.legend(title='')
    plt.legend(loc='upper left')
    if "Strong" in title and measure == "tmr":
        plt.legend(loc='center left')

    # For mem plots, we need to legend, as it's already in the time plot
    if measure == "mem" or measure == "strong" or measure == "weak":
        ax.get_legend().remove()

    # Save to files
    testcase = title.lower().replace( " ", "-" )
    testcase = ''.join(c for c in testcase if c.isalnum() or c == '-')
    testcase = testcase.replace("--", "-")
    plt.savefig(
        out_dir_png + "/" + testcase + '-' + measure + "-" + yscale + ".png",
        format='png', bbox_inches="tight"
    )
    plt.savefig(
        out_dir_pdf + "/" + testcase + '-' + measure + "-" + yscale + ".pdf",
        format='pdf', bbox_inches="tight"
    )
    plt.savefig(
        out_dir_svg + "/" + testcase + '-' + measure + "-" + yscale + ".svg",
        format='svg', bbox_inches="tight"
    )
    plt.close( plotnum )
    plotnum += 1

# ------------------------------------------------------------
#     plot_all_tables
# ------------------------------------------------------------

def plot_all_tables(
    testcase, time_data, memory_data, xlabel_scale, xticklabels=size_xticklabels,
    markers=all_markers, dashes=all_dashes, palette=all_palette, measure_1="tmr", **kwargs
):
    plot_table(
        testcase, time_data, measure_1, xlabel_scale, "lin", xticklabels,
        markers, dashes, palette, **kwargs
    )
    plot_table(
        testcase, memory_data, "mem", xlabel_scale, "lin", xticklabels,
        markers, dashes, palette, **kwargs
    )
    plot_table(
        testcase, time_data, measure_1, xlabel_scale, "log", xticklabels,
        markers, dashes, palette, **kwargs
    )
    plot_table(
        testcase, memory_data, "mem", xlabel_scale, "log", xticklabels,
        markers, dashes, palette, **kwargs
    )
