#!/usr/bin/env python3

import sys, os

# Make sure we are in the script dir
os.chdir(os.path.dirname(sys.argv[0]))

# Such a cheat to import stuff in python...
# See https://stackoverflow.com/a/22956038
sys.path.insert(0, '../common')
from benchmarks import *

sizes=[ 1 ]

# Run all tests

# Diversity

# for window in [100000]:
for window in [1000, 20000, 100000]:
    run_suite( sizes, "grenedalf/diversity.sh", {   "window": window })
    run_suite( sizes, "grenedalf/diversity.sh", {   "window": window, "bugs": "1" })
    run_suite( sizes, "npstat/diversity.sh", {      "window": window } )
    run_suite( sizes, "popoolation/diversity.sh", { "window": window, "measure": "d" })
    run_suite( sizes, "popoolation/diversity.sh", { "window": window, "measure": "pi" })
    run_suite( sizes, "popoolation/diversity.sh", { "window": window, "measure": "theta" })

# FST

# grenedalf
for method in ["unbiased-nei","unbiased-hudson","kofler","karlsson"]:
    run_suite( sizes, "grenedalf/fst.sh", { "window":    1, "method": method })
    run_suite( sizes, "grenedalf/fst.sh", { "window":  100, "method": method })
    run_suite( sizes, "grenedalf/fst.sh", { "window": 1000, "method": method })

# # poolfstat
for method in ["Anova","Identity"]:
    run_suite( sizes, "poolfstat/fst.sh", { "window":   1, "method": method })
    run_suite( sizes, "poolfstat/fst.sh", { "window": 100, "method": method })

# popoolation
for method in ["kofler","karlsson"]:
    run_suite( sizes, "popoolation/fst.sh", { "window":    1, "method": method })
    run_suite( sizes, "popoolation/fst.sh", { "window": 1000, "method": method })
