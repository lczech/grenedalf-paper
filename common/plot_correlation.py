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
import scipy as sp
from matplotlib.ticker import FuncFormatter

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
def plot_corr(
    title, xlabel, ylabel, x, y, with_kernel = True
    # markers='o', dashes=(0, ""), palette='k', **kwargs
):
    global plotnum
    global out_dir_png
    global out_dir_pdf
    global out_dir_svg

    # Get proper name and print it
    testcase = title + '-' + xlabel + '-' + ylabel
    testcase = testcase.lower().replace( " ", "-" )
    testcase = ''.join(c for c in testcase if c.isalnum() or c == '-')
    testcase = testcase.replace("--", "-")
    print("Plot: " + testcase)

    # print(x)
    # print(y)
    if len(x) != len(y):
        print("Warning: x has " + str(len(x)) + " rows, y has " + str(len(y)) + " rows")

    # Remake data as one frame, because of reasons
    # (being: we need to drop na, but in both at the same time)
    df = pd.DataFrame(data={'x': x, 'y': y})
    df = df[df['x'].notna()]
    df = df[df['y'].notna()]
    # print (df)

    # Create dirs for results
    if not os.path.exists(out_dir_png):
        os.makedirs(out_dir_png)
    if not os.path.exists(out_dir_pdf):
        os.makedirs(out_dir_pdf)
    if not os.path.exists(out_dir_svg):
        os.makedirs(out_dir_svg)

    # Compute the pearson correlation between both, and the mean squared error
    pearson_r, pearson_p = sp.stats.pearsonr(x=df['x'], y=df['y'])
    # mse = ((df['x'] - df['y'])**2).mean()
    mae = (np.absolute(df['x'] - df['y'])).mean()

    # Let's make a fancy density plot to be able to better see the dot density
    # Also, we subset for the kernel computation, as it takes waaaay to long otherwise...
    if with_kernel:
        max_df_size = 25000
        if len(df.index) > max_df_size:
            print("  subsetting")
            df = df.sample(n=max_df_size)
        values = np.vstack([df['x'], df['y']])
        colormap = plt.cm.viridis_r
        print("  kernel")
        kernel = sp.stats.gaussian_kde(values)(values)

        # Make the plot
        print("  plot", len(values[0]))
        plt.figure( plotnum, figsize=(8,8) )
        ax = sns.scatterplot(
            x=df["x"], y=df["y"],
            c=kernel,
            cmap=colormap,
            linewidth=0
        )
        # sns.kdeplot(
        #      x=df["x"], y=df["y"], fill=True, cmap=colormap
        # )
    else:
        # Make the plot
        plt.figure( plotnum, figsize=(8,8) )
        ax = sns.scatterplot(
            x=df["x"], y=df["y"],
            linewidth=0
        )

    # Make proper
    ax.set_box_aspect(1)
    ax.set_aspect('equal')

    # Draw a line of x=y
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    lims = [max(x0, y0), min(x1, y1)]
    ax.plot( lims, lims, 'lightgray', zorder=-1)
    # ax.plot( lims, lims, 'k', alpha=0.2 )
    # plt.plot([0, 1], [0, 1])

    # annotate the pearson correlation coefficient text to 2 decimal places
    plt.text(.05, .95, 'r={:.2f}'.format(pearson_r), transform=ax.transAxes)
    # plt.text(.05, .92, 's={:.6f}'.format(mse), transform=ax.transAxes)
    plt.text(.05, .92, 'MAE={:.4f}'.format(mae), transform=ax.transAxes)

    # Nameing the plot and the axis.
    ax.set_title( title )
    ax.set_xlabel( xlabel )
    ax.set_ylabel( ylabel )

    # Save to files
    plt.savefig( out_dir_png + "/" + testcase + ".png", format='png', bbox_inches="tight" )
    plt.savefig( out_dir_pdf + "/" + testcase + ".pdf", format='pdf', bbox_inches="tight" )
    plt.savefig( out_dir_svg + "/" + testcase + ".svg", format='svg', bbox_inches="tight" )
    plt.close( plotnum )
    plotnum += 1
