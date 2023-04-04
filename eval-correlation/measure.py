#!/usr/bin/python3

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

run_suite( sizes, "grenedalf/diversity.sh" )
run_suite( sizes, "grenedalf/diversity.sh", { "bugs": "1" })
run_suite( sizes, "npstat/diversity.sh" )
run_suite( sizes, "popoolation/diversity.sh", { "measure": "d" })
run_suite( sizes, "popoolation/diversity.sh", { "measure": "pi" })
run_suite( sizes, "popoolation/diversity.sh", { "measure": "theta" })

# FST

for method in ["unbiased-nei","unbiased-hudson","kofler","karlsson"]:
    run_suite( sizes, "grenedalf/fst.sh", { "window":    1, "method": method })
    run_suite( sizes, "grenedalf/fst.sh", { "window":  100, "method": method })
    run_suite( sizes, "grenedalf/fst.sh", { "window": 1000, "method": method })

for method in ["Anova","Identity"]:
    run_suite( sizes, "poolfstat/fst.sh", { "window":   1, "method": method })
    run_suite( sizes, "poolfstat/fst.sh", { "window": 100, "method": method })

for method in ["kofler","karlsson"]:
    run_suite( sizes, "popoolation/fst.sh", { "window":    1, "method": method })
    run_suite( sizes, "popoolation/fst.sh", { "window": 1000, "method": method })