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

# Conversion
run_suite( sizes, "samtools/mpileup.sh" )
run_suite( sizes, "grenedalf/sync-bam.sh" )
run_suite( sizes, "grenedalf/sync-mpileup.sh" )
run_suite( sizes, "popoolation/sync-perl.sh" )
run_suite( sizes, "popoolation/sync-java.sh" )

# Diversity
run_suite( sizes, "grenedalf/diversity-bam.sh" )
run_suite( sizes, "grenedalf/diversity-mpileup.sh" )
run_suite( sizes, "grenedalf/diversity-sync.sh" )
run_suite( sizes, "popoolation/d.sh" )
# run_suite( sizes, "popoolation/pi.sh" )
# run_suite( sizes, "popoolation/theta.sh" )
run_suite( sizes, "npstat/diversity.sh" )

# FST
run_suite( sizes, "grenedalf/fst-bam.sh" )
run_suite( sizes, "grenedalf/fst-mpileup.sh" )
run_suite( sizes, "grenedalf/fst-sync.sh" )
run_suite( sizes, "grenedalf/fst-sync.sh" )
run_suite( sizes, "grenedalf/fst-sync-gz.sh" )
run_suite( sizes, "poolfstat/fst.sh" )
run_suite( sizes, "popoolation/fst.sh" )
