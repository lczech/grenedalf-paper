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

infile = "full_check.tsv"
df = pd.read_csv(infile, sep='\t')

# ------------------------------------------------------------
#     grenedalf vs independent
# ------------------------------------------------------------

# Theta Pi
plot_corr( "theta_pi_1", "grenedalf", "independent", df["grenedalf.theta_pi_1"], df["indep.theta_pi_1"], with_kernel = False )
plot_corr( "theta_pi_2", "grenedalf", "independent", df["grenedalf.theta_pi_2"], df["indep.theta_pi_2"], with_kernel = False )

# Theta W
plot_corr( "theta_w_1", "grenedalf", "independent", df["grenedalf.theta_w_1"], df["indep.theta_w_1"], with_kernel = False )
plot_corr( "theta_w_2", "grenedalf", "independent", df["grenedalf.theta_w_2"], df["indep.theta_w_2"], with_kernel = False )

# Tajima's D
plot_corr( "tajimas_d_1", "grenedalf", "independent", df["grenedalf.tajimas_d_1"], df["indep.tajimas_d_1"], with_kernel = False )
plot_corr( "tajimas_d_2", "grenedalf", "independent", df["grenedalf.tajimas_d_2"], df["indep.tajimas_d_2"], with_kernel = False )

# Fst
plot_corr( "fst_nei", "grenedalf", "independent", df["grenedalf.fst_nei"], df["indep.fst_nei"], with_kernel = False )
plot_corr( "fst_hudson", "grenedalf", "independent", df["grenedalf.fst_hudson"], df["indep.fst_hudson"], with_kernel = False )
plot_corr( "fst_karlsson", "grenedalf", "independent", df["grenedalf.fst_karlsson"], df["indep.fst_karlsson"], with_kernel = False )
plot_corr( "fst_kofler", "grenedalf", "independent", df["grenedalf.fst_kofler"], df["indep.fst_kofler"], with_kernel = False )

# ------------------------------------------------------------
#     grenedalf vs PoPoolation
# ------------------------------------------------------------

# Theta Pi
plot_corr( "theta_pi_1", "grenedalf", "popoolation", df["grenedalf.theta_pi_1"], df["popoolation.theta_pi_1"], with_kernel = False )
plot_corr( "theta_pi_2", "grenedalf", "popoolation", df["grenedalf.theta_pi_2"], df["popoolation.theta_pi_2"], with_kernel = False )

# Theta W
plot_corr( "theta_w_1", "grenedalf", "popoolation", df["grenedalf.theta_w_1"], df["popoolation.theta_w_1"], with_kernel = False )
plot_corr( "theta_w_2", "grenedalf", "popoolation", df["grenedalf.theta_w_2"], df["popoolation.theta_w_2"], with_kernel = False )

# Tajima's D
plot_corr( "tajimas_d_1", "grenedalf", "popoolation", df["grenedalf.tajimas_d_1"], df["popoolation.tajimas_d_1"], with_kernel = False )
plot_corr( "tajimas_d_2", "grenedalf", "popoolation", df["grenedalf.tajimas_d_2"], df["popoolation.tajimas_d_2"], with_kernel = False )

# Fst
plot_corr( "fst_karlsson", "grenedalf", "popoolation", df["grenedalf.fst_karlsson"], df["popoolation.fst_karlsson"], with_kernel = False )
plot_corr( "fst_kofler", "grenedalf", "popoolation", df["grenedalf.fst_kofler"], df["popoolation.fst_kofler"], with_kernel = False )

# ------------------------------------------------------------
#     independent vs PoPoolation
# ------------------------------------------------------------

# Theta Pi
plot_corr( "theta_pi_1", "independent", "popoolation", df["indep.theta_pi_1"], df["popoolation.theta_pi_1"], with_kernel = False )
plot_corr( "theta_pi_2", "independent", "popoolation", df["indep.theta_pi_2"], df["popoolation.theta_pi_2"], with_kernel = False )

# Theta W
plot_corr( "theta_w_1", "independent", "popoolation", df["indep.theta_w_1"], df["popoolation.theta_w_1"], with_kernel = False )
plot_corr( "theta_w_2", "independent", "popoolation", df["indep.theta_w_2"], df["popoolation.theta_w_2"], with_kernel = False )

# Tajima's D
plot_corr( "tajimas_d_1", "independent", "popoolation", df["indep.tajimas_d_1"], df["popoolation.tajimas_d_1"], with_kernel = False )
plot_corr( "tajimas_d_2", "independent", "popoolation", df["indep.tajimas_d_2"], df["popoolation.tajimas_d_2"], with_kernel = False )

# Fst
plot_corr( "fst_karlsson", "independent", "popoolation", df["indep.fst_karlsson"], df["popoolation.fst_karlsson"], with_kernel = False )
plot_corr( "fst_kofler", "independent", "popoolation", df["indep.fst_kofler"], df["popoolation.fst_kofler"], with_kernel = False )
