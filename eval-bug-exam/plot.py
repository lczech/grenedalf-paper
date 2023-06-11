#!/usr/bin/env python3

# libraries
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import seaborn as sns
import os, sys

# ------------------------------------------------------------
#     Settings
# ------------------------------------------------------------

# global names for our ins and outs
out_dir_png = "figures_png"
out_dir_pdf = "figures_pdf"
out_dir_svg = "figures_svg"

# ------------------------------------------------------------
#     Plotting
# ------------------------------------------------------------

plotnum = 1
def plot_window(window):
    global plotnum
    table="windows/window-{}.csv".format( window )

    # Data axis names
    x_name = "Min Coverage"
    y_name = "Tajima's D, ratio bug / fix"
    h_name = "Poolsize"

    # Read the data and transform as needed into long format
    data = pd.read_csv(table, sep='\t')
    data = data.melt(var_name="id", value_name="val")
    df = data["id"].str.split( ";", expand=True )
    df = df.rename(columns={0: x_name, 1: h_name})
    df[y_name] = data["val"]
    # print(df)

    # Subset to only larger pool sizes, to keep plot consistent
    df = df[df["Poolsize"].astype(int) >= 100]
    n_colors=4 #7 with all

    # Plot the thing. Obviously, because catplot, we cannot just set the figure size
    # beforehand as with other plot types in seaborn... have to do it in the function... WTF
    # aaaand it has to be specified with height and aspcet, instead of width....
    # plt.figure( plotnum, figsize=(40,15) )
    g = sns.catplot(
        data=df, x=x_name, y=y_name, hue=h_name,
        kind="violin", scale="width", palette=sns.color_palette("flare", n_colors=n_colors),
        linewidth=0.5, height=6, aspect=1.8, legend_out=False,
        facet_kws={"gridspec_kws": {"wspace":0.0}, "margin_titles": True, "ylim": (0, 8.5) }
    )
    # margin_titles=False, xlim=None, ylim=None, subplot_kws=None, gridspec_kws=None

    # plt.ylim(0, 11)
    g.fig.tight_layout()
    plt.tight_layout()
    plt.subplots_adjust( wspace=0.0 )
    g.wspace=0.0
    plt.legend(loc='upper right')
    sns.move_legend(g, "upper right", bbox_to_anchor=(.97, .95))

    # Draw reference line
    g.map(plt.axhline, y=1.0, linestyle="--", color='lightgray', clip_on=False)

    # set the axis labels
    # plt.xlabel(x_name)
    # plt.ylabel(y_name)

    # plt.ylim(0, 11)
    # # plt.yticks([range(0, 11)])
    # # sns.set_style("ticks", {"ytick.major.size":1})
    # plt.yticks(np.arange(0, 10))
    # ax = sns.violinplot(x=xname, y=yname, data=df, scale="width").set_title(os.path.splitext(table)[0])

    # Save to files
    plt.savefig( out_dir_png + "/window-" + window + ".png", format='png', bbox_inches="tight" )
    plt.savefig( out_dir_pdf + "/window-" + window + ".pdf", format='pdf', bbox_inches="tight" )
    plt.savefig( out_dir_svg + "/window-" + window + ".svg", format='svg', bbox_inches="tight" )
    plt.close( plotnum )
    plotnum += 1

# ------------------------------------------------------------
#     Call
# ------------------------------------------------------------

# Create dirs for results
if not os.path.exists(out_dir_png):
    os.makedirs(out_dir_png)
if not os.path.exists(out_dir_pdf):
    os.makedirs(out_dir_pdf)
if not os.path.exists(out_dir_svg):
    os.makedirs(out_dir_svg)

# for window in [ "100", "1000" ]:
for window in [ "5", "10", "20", "50", "100", "200", "500", "1000" ]:
    print("Window", window)
    plot_window( window )
