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

# Such a cheat to import stuff in python...
# See https://stackoverflow.com/a/22956038
sys.path.insert(0, '../common')
from plot_correlation import *

# ------------------------------------------------------------
#     Settings
# ------------------------------------------------------------

# quick switches for development
plot_diversity = True
plot_fst       = True

# ==================================================================================================
#     Functions
# ==================================================================================================

# ------------------------------------------------------------
#     Parsing
# ------------------------------------------------------------

def parse_grenedalf(infile):
    df = pd.read_csv(infile, sep=',')
    # Different early versions of grenedalf changed the naming of columns.
    # We here just add both then, to make the downstream stuff easier.
    if "S1S2-20000000.1:S1S2-20000000.2" in df:
        df["1.2"] = df["S1S2-20000000.1:S1S2-20000000.2"]
    for col in df.columns.tolist():
        if col.startswith("S1-20000000."):
            df[col[len("S1-20000000."):]] = df[col]
    if "start" in df:
        df["START"] = df["start"]
    return df

def parse_npstat(infile):
    return pd.read_csv(infile, sep='\t')

def parse_poolfstat(infile):
    return pd.read_csv(infile, sep=',')

def parse_popoolation_diversity(infile):
    return pd.read_csv(infile, sep='\t', header=None)

def parse_popoolation_fst(infile):
    df = pd.read_csv(infile, sep='\t', header=None)
    df[5] = df[5].str.replace("1:2=", "").replace("na", "nan").astype({5: float})
    return df

# ==================================================================================================
#     Diversity
# ==================================================================================================

if plot_diversity:
    # for window in [1000, 20000]:
    for window in [100000]:

        # ------------------------------------------------------------
        #     Reading
        # ------------------------------------------------------------

        # Prepare grenedalf data, with the tajima d bug and without
        # with the bug replication
        grenedalf_popool_div_file = "grenedalf/diversity/diversity-S1-20000000-popoolation-{}.csv".format(window)
        grenedalf_popool_div = parse_grenedalf( grenedalf_popool_div_file )
        grenedalf_popool_p = grenedalf_popool_div["1.theta_pi_rel"]
        grenedalf_popool_w = grenedalf_popool_div["1.theta_watterson_rel"]
        grenedalf_popool_d = grenedalf_popool_div["1.tajimas_d"]

        # without
        grenedalf_nobugs_div_file = "grenedalf/diversity/diversity-S1-20000000-nobugs-{}.csv".format(window)
        grenedalf_nobugs_div = parse_grenedalf( grenedalf_nobugs_div_file )
        grenedalf_nobugs_p = grenedalf_nobugs_div["1.theta_pi_rel"]
        grenedalf_nobugs_w = grenedalf_nobugs_div["1.theta_watterson_rel"]
        grenedalf_nobugs_d = grenedalf_nobugs_div["1.tajimas_d"]

        # Prepare popoolation data
        # popoolation_p_file = "popoolation/diversity/S1-20000000-{}.pi".format(window)
        # popoolation_w_file = "popoolation/diversity/S1-20000000-{}.theta".format(window)
        # popoolation_d_file = "popoolation/diversity/S1-20000000-{}.d".format(window)
        # popoolation_p = parse_popoolation_diversity( popoolation_p_file )[4]
        # popoolation_w = parse_popoolation_diversity( popoolation_w_file )[4]
        # popoolation_d = parse_popoolation_diversity( popoolation_d_file )[4]

        # Prepare npstat data
        npstat_file = "npstat/diversity/diversity-S1-20000000-{}.stats".format(window)
        npstat_div = parse_npstat( npstat_file )
        npstat_p = npstat_div["Pi"]
        npstat_w = npstat_div["Watterson"]
        npstat_d = npstat_div["Tajima_D"]

        # npstat gives Tajima'S D valus in the range +/- 10^13, which seems _slighly_ wrong.
        # Replaceing the large ones here so that we can actually plot something useful to show this.
        npstat_d = npstat_d.apply( lambda x: x if x > -10.0 and x < 10.0 else np.nan )

        # ------------------------------------------------------------
        #     grenedalf vs PoPoolation
        # ------------------------------------------------------------

        # Plot grenedalf with bugs vs popoolation
        plot_corr( "Theta Pi (bugs) ({})".format(window),        "grenedalf", "PoPoolation", grenedalf_popool_p, popoolation_p )
        plot_corr( "Theta Watterson (bugs) ({})".format(window), "grenedalf", "PoPoolation", grenedalf_popool_w, popoolation_w )
        plot_corr( "Tajima's D (bugs) ({})".format(window),      "grenedalf", "PoPoolation", grenedalf_popool_d, popoolation_d )

        # Plot grenedalf without bugs vs popoolation
        plot_corr( "Theta Pi ({})".format(window),        "grenedalf", "PoPoolation", grenedalf_nobugs_p, popoolation_p )
        plot_corr( "Theta Watterson ({})".format(window), "grenedalf", "PoPoolation", grenedalf_nobugs_w, popoolation_w )
        plot_corr( "Tajima's D ({})".format(window),      "grenedalf", "PoPoolation", grenedalf_nobugs_d, popoolation_d )

        # ------------------------------------------------------------
        #     grenedalf vs npstat
        # ------------------------------------------------------------

        # Plot grenedalf vs npstat
        plot_corr( "Theta Pi ({})".format(window),        "grenedalf", "npstat", grenedalf_nobugs_p, npstat_p )
        plot_corr( "Theta Watterson ({})".format(window), "grenedalf", "npstat", grenedalf_nobugs_w, npstat_w )
        plot_corr( "Tajima's D ({})".format(window),      "grenedalf", "npstat", grenedalf_nobugs_d, npstat_d )

        # ------------------------------------------------------------
        #     stats vs stats
        # ------------------------------------------------------------

        # Plot grenedalf with bugs vs without
        # plot_corr(
        #     "Theta Pi",        "grenedalf", "grenedalf (bugs)",
        #     grenedalf_nobugs_p, grenedalf_popool_p
        # )
        # plot_corr(
        #     "Theta Watterson", "grenedalf", "grenedalf (bugs)",
        #     grenedalf_nobugs_w, grenedalf_popool_w
        # )
        plot_corr(
            "Tajima's D ({})".format(window),      "grenedalf", "grenedalf (bugs)",
            grenedalf_nobugs_d, grenedalf_popool_d
        )

# ==================================================================================================
#     FST
# ==================================================================================================

if plot_fst:
    # ------------------------------------------------------------
    #     Reading
    # ------------------------------------------------------------

    # Prepare grenedalf data
    grenedalf_fst = {}
    grenedalf_fst_file_base = "grenedalf/fst/fst-S1S2-20000000-{}-{}.csv"
    for method in ["unbiased-nei","unbiased-hudson","kofler","karlsson"]:
        for window in ["1", "100", "1000"]:
            grenedalf_fst[window + "-" + method] = parse_grenedalf(
                grenedalf_fst_file_base.format(window, method )
            )#["1.2"]

    # # Prepare poolfstat data
    # poolfstat_fst = {}
    # poolfstat_file_base = "poolfstat/fst/fst-S1S2-20000000-{}-{}.txt-sliding.csv"
    # for method in ["Anova","Identity"]:
    #     for window in ["1", "100"]:
    #         poolfstat_fst[window + "-" + method] = parse_poolfstat(
    #             poolfstat_file_base.format( window, method )
    #         )#["MultiLocusFst"]

    # Prepare PoPoolation2 data
    popoolation_fst = {}
    popoolation_file_base = "popoolation/fst/S1S2-20000000-{}-{}.fst"
    for method in ["kofler","karlsson"]:
        for window in ["1", "1000"]:
            popoolation_fst[window + "-" + method] = parse_popoolation_fst(
                popoolation_file_base.format( window, method )
            )#[5]

            # PoPoolation somehow prints one out last row that we don't want for this
            if window == "1000":
                popoolation_fst[window + "-" + method].drop(
                    popoolation_fst[window + "-" + method].tail(1).index,inplace=True
                )

    # ------------------------------------------------------------
    #     grenedalf vs PoPoolation
    # ------------------------------------------------------------

    # Plot grenedalf vs PoPoolation
    for method in ["kofler", "karlsson"]:
        # We set up the tools so that they produce the same number of windows already,
        # so we can immediately match here.
        window="1000"
        plot_corr(
            "FST (" + method + ", " + window + ")", "grenedalf", "PoPoolation",
            grenedalf_fst[window + "-" + method]["1.2"],
            popoolation_fst[window + "-" + method][5]
        )

        # Here, the exact filtering seems to not quite match for some reason.
        # Hence, we join to only get the matching positions.
        window="1"
        merged_df = grenedalf_fst[window + "-" + method].merge(
            popoolation_fst[window + "-" + method], how = 'inner',
            left_on='START', right_on=1
        )
        plot_corr(
            "FST (" + method + ", " + window + ")", "grenedalf", "PoPoolation",
            merged_df["1.2"], merged_df[5]
        )

    # ------------------------------------------------------------
    #     stats vs stats
    # ------------------------------------------------------------

    # Plot grenedalf statistics against each other
    for window in ["1000", "100", "1"]:
        # Kofler matches with the lines, so we can plot directly
        plot_corr(
            "FST (Kofler vs Nei, " + window + ")", "Nei", "Kofler",
            grenedalf_fst[window + "-unbiased-nei"]["1.2"],
            grenedalf_fst[window + "-kofler"]["1.2"],
        )

        # For hudson, we compute with all SNPs, but karlsson is only biallelic, so we subset
        merged_df = grenedalf_fst[window + "-unbiased-hudson"].merge(
            grenedalf_fst[window + "-karlsson"], how='inner', on="START"
        )
        plot_corr(
            "FST (Karlsson vs Hudson, " + window + ")", "Hudson", "Karlsson",
            merged_df["1.2_x"], merged_df["1.2_y"],
        )
