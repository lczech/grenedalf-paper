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

# Yikes... https://stackoverflow.com/a/66683635
def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

# ------------------------------------------------------------
#     Settings
# ------------------------------------------------------------

# global names for our ins and outs
out_dir_png = "figures_png"
out_dir_pdf = "figures_pdf"
out_dir_svg = "figures_svg"

# ------------------------------------------------------------
#     Parsing
# ------------------------------------------------------------

def parse_grenedalf(infile):
    return pd.read_csv(infile, sep=',')

def parse_npstat(infile):
    return pd.read_csv(infile, sep='\t')

def parse_poolfstat(infile):
    return pd.read_csv(infile, sep=',')

def parse_popoolation_diversity(infile):
    return pd.read_csv(infile, sep='\t', header=None)

def parse_popoolation_fst(infile):
    df = pd.read_csv(infile, sep='\t', header=None)
    # df[5] = df[5].map(lambda x: remove_suffix(x, "1:2=")).astype({5: float})
    # df[5] = df[5].map(lambda x: remove_suffix(x, "1:2="))
    df[5] = df[5].str.replace("1:2=", "").replace("na", "nan").astype({5: float})
    return df

# ------------------------------------------------------------
#     Plotting
# ------------------------------------------------------------

plotnum = 1
def plot_corr(
    title, xlabel, ylabel, x, y
    # markers='o', dashes=(0, ""), palette='k', **kwargs
):
    global plotnum
    global out_dir_png
    global out_dir_pdf
    global out_dir_svg

    # print(x)
    # print(y)

    # Create dirs for results
    if not os.path.exists(out_dir_png):
        os.makedirs(out_dir_png)
    if not os.path.exists(out_dir_pdf):
        os.makedirs(out_dir_pdf)
    if not os.path.exists(out_dir_svg):
        os.makedirs(out_dir_svg)

    # Make the plot.
    plt.figure( plotnum, figsize=(8,8) )
    ax = sns.scatterplot(
        x=x, y=y #, markers=list_markers, dashes=list_dashes, palette=list_palette, **kwargs
    )
    ax.set_box_aspect(1)
    ax.set_aspect('equal')

    # Draw a line of x=y
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    lims = [max(x0, y0), min(x1, y1)]
    ax.plot(lims, lims, 'darkorange')
    # plt.plot([0, 1], [0, 1])

    # Nameing the plot and the axis.
    ax.set_title( title )
    ax.set_xlabel( xlabel )
    ax.set_ylabel( ylabel )

    # Save to files
    testcase = title.lower().replace( " ", "-" ) + '-' + xlabel + '-' + ylabel
    testcase = ''.join(c for c in testcase if c.isalnum() or c == '-')
    testcase = testcase.replace("--", "-")
    plt.savefig( out_dir_png + "/" + testcase + ".png", format='png', bbox_inches="tight" )
    plt.savefig( out_dir_pdf + "/" + testcase + ".pdf", format='pdf', bbox_inches="tight" )
    plt.savefig( out_dir_svg + "/" + testcase + ".svg", format='svg', bbox_inches="tight" )
    plt.close( plotnum )
    plotnum += 1

# ------------------------------------------------------------
#     Processing Diversity
# ------------------------------------------------------------

# Prepare grenedalf data, with the tajima d bug and without
# with the bug replication
grenedalf_popool_div_file = "grenedalf/diversity/diversity-S1-20000000-popoolation.csv"
grenedalf_popool_div = parse_grenedalf( grenedalf_popool_div_file )
grenedalf_popool_p = grenedalf_popool_div["1.theta_pi_rel"]
grenedalf_popool_w = grenedalf_popool_div["1.theta_watterson_rel"]
grenedalf_popool_d = grenedalf_popool_div["1.tajimas_d"]

# without
grenedalf_nobugs_div_file = "grenedalf/diversity/diversity-S1-20000000-nobugs.csv"
grenedalf_nobugs_div = parse_grenedalf( grenedalf_nobugs_div_file )
grenedalf_nobugs_p = grenedalf_nobugs_div["1.theta_pi_rel"]
grenedalf_nobugs_w = grenedalf_nobugs_div["1.theta_watterson_rel"]
grenedalf_nobugs_d = grenedalf_nobugs_div["1.tajimas_d"]

# Prepare popoolation data
popoolation_p_file = "popoolation/diversity/S1-20000000.pi"
popoolation_w_file = "popoolation/diversity/S1-20000000.theta"
popoolation_d_file = "popoolation/diversity/S1-20000000.d"
popoolation_p = parse_popoolation_diversity( popoolation_p_file )[4]
popoolation_w = parse_popoolation_diversity( popoolation_w_file )[4]
popoolation_d = parse_popoolation_diversity( popoolation_d_file )[4]

# Prepare npstat data
npstat_file = "npstat/diversity/diversity-S1-20000000.stats"
npstat_div = parse_npstat( npstat_file )
npstat_p = npstat_div["Pi"]
npstat_w = npstat_div["Watterson"]
npstat_d = npstat_div["Tajima_D"]

# npstat gives Tajima'S D valus in the range +/- 10^13, which seems _slighly_ wrong.
# Replaceing the large ones here so that we can actually plot something useful to show this.
npstat_d = npstat_d.apply( lambda x: x if x > -10.0 and x < 10.0 else np.nan )

# Plot grenedalf with bugs vs popoolation
plot_corr( "Theta Pi (bugs)",        "grenedalf", "PoPoolation", grenedalf_popool_p, popoolation_p )
plot_corr( "Theta Watterson (bugs)", "grenedalf", "PoPoolation", grenedalf_popool_w, popoolation_w )
plot_corr( "Tajima's D (bugs)",      "grenedalf", "PoPoolation", grenedalf_popool_d, popoolation_d )

# Plot grenedalf without bugs vs popoolation
plot_corr( "Theta Pi",        "grenedalf", "PoPoolation", grenedalf_nobugs_p, popoolation_p )
plot_corr( "Theta Watterson", "grenedalf", "PoPoolation", grenedalf_nobugs_w, popoolation_w )
plot_corr( "Tajima's D",      "grenedalf", "PoPoolation", grenedalf_nobugs_d, popoolation_d )

# Plot grenedalf with bugs vs without
plot_corr( "Theta Pi",        "grenedalf", "grenedalf (bugs)", grenedalf_nobugs_p, grenedalf_popool_p )
plot_corr( "Theta Watterson", "grenedalf", "grenedalf (bugs)", grenedalf_nobugs_w, grenedalf_popool_w )
plot_corr( "Tajima's D",      "grenedalf", "grenedalf (bugs)", grenedalf_nobugs_d, grenedalf_popool_d )

# Plot grenedalf vs npstat
plot_corr( "Theta Pi",        "grenedalf", "npstat", grenedalf_nobugs_p, npstat_p )
plot_corr( "Theta Watterson", "grenedalf", "npstat", grenedalf_nobugs_w, npstat_w )
plot_corr( "Tajima's D",      "grenedalf", "npstat", grenedalf_nobugs_d, npstat_d )

# ------------------------------------------------------------
#     Processing FST
# ------------------------------------------------------------

# Prepare grenedalf data
grenedalf_fst = {}
grenedalf_fst_file_base = "grenedalf/fst/fst-S1S2-20000000-{}-{}.csv"
for method in ["unbiased-nei","unbiased-hudson","kofler","karlsson"]:
    for window in ["1", "100", "1000"]:
        grenedalf_fst[window + "-" + method] = parse_grenedalf(
            grenedalf_fst_file_base.format(window, method )
        )#["1.2"]

# Prepare poolfstat data
poolfstat_fst = {}
poolfstat_file_base = "poolfstat/fst/fst-S1S2-20000000-{}-{}.txt-sliding.csv"
for method in ["Anova","Identity"]:
    for window in ["1", "100"]:
        poolfstat_fst[window + "-" + method] = parse_poolfstat(
            poolfstat_file_base.format( window method )
        )#["MultiLocusFst"]

# Prepare PoPoolation2 data
popoolation_fst = {}
popoolation_file_base = "popoolation/fst/S1S2-20000000-{}-{}.fst"
for method in ["kofler","karlsson"]:
    for window in ["1", "1000"]:
        popoolation_fst[window + "-" + method] = parse_popoolation_fst(
            popoolation_file_base.format( window, method )
        )#[5]

# Plot grenedalf fsts against each other
for method in ["kofler", "karlsson"]:
    window="1000"
    plot_corr(
        "FST (" + method + ", " + window + ")", "grenedalf", "PoPoolation",
        grenedalf_fst[window + "-" + method]["1.2"],
        popoolation_fst[window + "-" + method][5]
    )

    window="1"
    merged_df = grenedalf_fst[window + "-" + method].merge(
        popoolation_fst[window + "-" + method], how = 'inner',
        left_on='START', right_on=1
    )
    plot_corr(
        "FST (" + method + ", " + window + ")", "grenedalf", "PoPoolation",
        merged_df["1.2"], merged_df[5]
    )
