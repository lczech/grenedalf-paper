#!/usr/bin/python3

import sys, os

# Make sure we are in the script dir
os.chdir(os.path.dirname(sys.argv[0]))

# Such a cheat to import stuff in python...
# See https://stackoverflow.com/a/22956038
sys.path.insert(0, '../common')
from benchmarks import *

# Sizes of the datasets for which we want to run the tests.
# We currently use the same for sync and pileup, for convenience.
sizes=[
    1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000,
    1000000, 2000000, 5000000, 10000000, 20000000, 50000000, 100000000
]

# For testing
# sizes=[ 1000, 2000, 5000 ]

# Run all tests

# grenedalf
run_suite( sizes, "grenedalf/diversity.sh", { "window": 1000 },  iterations=3 )
run_suite( sizes, "grenedalf/fst.sh",       { "window": 0 },     iterations=3 )
run_suite( sizes, "grenedalf/fst.sh",       { "window": 1 },     iterations=3 )
run_suite( sizes, "grenedalf/fst.sh",       { "window": 1000 },  iterations=3 )

# PoPoolation
# run_suite( sizes, "popoolation/d.sh",   { "window": 1000 })
run_suite( sizes, "popoolation/fst.sh", { "window": 1 })
run_suite( sizes, "popoolation/fst.sh", { "window": 1000 })
run_suite( sizes, "popoolation/fst.sh", { "window": 100000000 })

# poolfstat
# the "sliding" window in poolfstat is over number of SNPs instead of along the genome,
# and we hence use roughly the number of SNPs that we expect in a 1000bp window,
# so that we match the above tools. we used mutation rate of 1/10 for simulation, hence the number.
run_suite( sizes, "poolfstat/fst.sh", { "window": 0 })
run_suite( sizes, "poolfstat/fst.sh", { "window": 1 })
run_suite( sizes, "poolfstat/fst.sh", { "window": 100 })
