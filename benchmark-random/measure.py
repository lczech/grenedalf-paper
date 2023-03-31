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
# If changed, the function below needs to take this as an arg.
sizes=[
    1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000,
    1000000, 2000000, 5000000, 10000000, 20000000, 50000000, 100000000
]

# For testing
sizes=[ 1000, 2000, 5000 ]

def run_file_tests( type, script, window=0, name=None, iterations=1 ):
    data_dir="../data/" + type
    if not name:
        name = script

    # Run tests for all file sizes
    for size in sizes:
        # Get the file, and run the test
        args = "{}/random-{}.{}".format( data_dir, size, type )
        args += " {}".format( window )
        ( time, memory ) = run_tests( script, args, iterations )

        # Immediately write the result.
        # This writes to our predefine table names automatically,
        # because we are lazy and use global names today...
        append_to_tables(
            "{}\t{}\t{}\t{}\n".format( name, window, size, time ),
            "{}\t{}\t{}\t{}\n".format( name, window, size, memory )
        )


# Run all tests

# grenedalf
run_file_tests( "pileup", "grenedalf/diversity.sh", window=1000, name="grenedalf/diversity" )
run_file_tests( "sync",   "grenedalf/fst.sh",       window=0,    name="grenedalf/fst" )
run_file_tests( "sync",   "grenedalf/fst.sh",       window=1,    name="grenedalf/fst" )
run_file_tests( "sync",   "grenedalf/fst.sh",       window=1000, name="grenedalf/fst" )

# PoPoolation
run_file_tests( "pileup", "popoolation/d.sh",   window=1000, name="popoolation/diversity" )
run_file_tests( "sync",   "popoolation/fst.sh", window=1,    name="popoolation/fst" )
run_file_tests( "sync",   "popoolation/fst.sh", window=1000, name="popoolation/fst" )

# poolfstat
# the "sliding" window in poolfstat is over number of SNPs instead of along the genome,
# and we hence use roughly the number of SNPs that we expect in a 1000bp window,
# so that we match the above tools. we used mutation rate of 1/10 for simulation, hence the number.
run_file_tests( "sync",   "poolfstat/fst.sh", window=0,    name="poolfstat/fst" )
run_file_tests( "sync",   "poolfstat/fst.sh", window=100, name="poolfstat/fst" )
