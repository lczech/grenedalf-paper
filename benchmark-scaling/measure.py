#!/usr/bin/python3

import sys, os

# Make sure we are in the script dir
os.chdir(os.path.dirname(sys.argv[0]))

# Such a cheat to import stuff in python...
# See https://stackoverflow.com/a/22956038
sys.path.insert(0, '../common')
from benchmarks import *

# Number of samples for the scaling tests.
# We are on an 8-core system, so that's how far we go.
samples=[ 1, 2, 3, 4, 5, 6, 7, 8 ]

# For testing
# samples=[ 1, 2 ]

# Run all tests

# bam
run_suite( samples, "grenedalf/diversity-strong.sh", { "type": "bam" })
run_suite( samples, "grenedalf/diversity-weak.sh", { "type": "bam" })
run_suite( samples, "grenedalf/fst-strong.sh", { "type": "bam" })
run_suite( samples, "grenedalf/fst-weak.sh", { "type": "bam" })

# sync
run_suite( samples, "grenedalf/diversity-strong.sh", { "type": "sync" })
run_suite( samples, "grenedalf/diversity-weak.sh", { "type": "sync" })
run_suite( samples, "grenedalf/fst-strong.sh", { "type": "sync" })
run_suite( samples, "grenedalf/fst-weak.sh", { "type": "sync" })
