#!/usr/bin/env python3

import subprocess
import sys, os
import glob
from multiprocessing import Pool
from functools import partial
import datetime

# The data for this is simply the chunked data from eval-corr-grenenet,
# created by calling `make_data.sh` in this directory.

# We are testing on a 8-core hyperthreaded CPU.
# Using 12 threads seems like a good balance for independent runs without too much oversubscription.
# It does not have to be optimal, but this should give some speedup.
num_tasks = 12

# ------------------------------------------------------------
#     Run Functions
# ------------------------------------------------------------

# Run function, similar to the common/benchmarks.py function,
# but without all the printing and measuring, which we do not need here.
def run_script( script, args ):
    # Run a test script.
    # The function expects the script to be run, and a dict with key value pairs for the args.
    # We run bash scripts containing the tests, and they parse these args again.

    # Prepare the command to be run.
    # We cannot use normal `time` on Ubuntu, as it is a wrapper that does not have the -v option.
    # Need to run the underlying program instead.
    script=os.path.realpath(script)
    script_path = os.path.dirname(os.path.realpath(script))
    script_name = os.path.basename(os.path.realpath(script))
    script_args = " ".join([ key + "=" + str(val) for key, val in args.items() ])
    command = "/usr/bin/time -v " + script + " " + script_args + " 2>&1"

    # Start the process, capturing everything, and terminating on failure
    try:
        result = subprocess.run(
            command, cwd=script_path,
            capture_output=True, shell=True, text=True
        )
    except Exception as e:
        print("FAILED")
        print(e)
    if result.returncode != 0:
        print("FAILED")
        print(result.stdout)
        print(result.stderr)

def run_script_interal( script, args, chunk ):
    # print(f"Chunk {chunk}")
    args["chunk"] = chunk
    return run_script( script, args )

def run_chunk( script, args, chunk_prefix ):
    print(datetime.datetime.now(), "Run", script, str(args))

    # https://stackoverflow.com/a/25553970/4184258
    func = partial(run_script_interal, script, args)

    # Get the list of chunks, without the file names, so just `aaaa` etc.
    # Our file names do not have extensions, that makes it easy here to just `glob`.
    files = glob.glob( chunk_prefix + "*")
    chunks = [ fn[fn.startswith(chunk_prefix) and len(chunk_prefix):] for fn in files ]
    chunks.sort()

    # Run test cases in thread pool, for each chunk.
    with Pool(num_tasks) as pool:
        # pool.map(func, chunks[0:100])
        pool.map(func, chunks)

def run_diversity( script, args={} ):
    run_chunk( script, args, "chunks_mpileup/split_" )

def run_fst( script, args={} ):
    run_chunk( script, args, "chunks_sync/split_" )

def collect_results( expr, target ):
    files = glob.glob(expr)
    files.sort()
    out = open(target, "w")
    for file in files:
        with open(file) as f:
            lines = f.read().splitlines()
            if len(lines) not in [1, 2]:
                print("FILE WRONG", file)
            out.write(lines[-1] + "\n")
    out.close()

# ------------------------------------------------------------
#     Cases
# ------------------------------------------------------------

# Run all tests

# Diversity

run_diversity( "grenedalf/diversity.sh" )
collect_results(
    "grenedalf/diversity/diversity-split_*-nobugs.csv",
    "grenedalf/diversity-nobugs.csv"
)

run_diversity( "grenedalf/diversity.sh", { "bugs": "1" })
collect_results(
    "grenedalf/diversity/diversity-split_*-popoolation.csv",
    "grenedalf/diversity-popoolation.csv"
)

run_diversity( "popoolation/diversity.sh", { "measure": "d" })
collect_results(
    "popoolation/diversity/split_*.d",
    "popoolation/diversity-d.csv"
)

run_diversity( "popoolation/diversity.sh", { "measure": "pi" })
collect_results(
    "popoolation/diversity/split_*.pi",
    "popoolation/diversity-pi.csv"
)

run_diversity( "popoolation/diversity.sh", { "measure": "theta" })
collect_results(
    "popoolation/diversity/split_*.theta",
    "popoolation/diversity-theta.csv"
)

run_diversity( "npstat/diversity.sh" )
collect_results(
    "npstat/diversity/diversity-split_*.stats",
    "npstat/diversity.csv"
)

# FST

# grenedalf
for method in ["unbiased-nei","unbiased-hudson","kofler","karlsson"]:
    for window in [100, 1000]:
        run_fst( "grenedalf/fst.sh", { "window": window, "method": method })
        collect_results(
            f"grenedalf/fst/fst-split_*-{window}-{method}.csv",
            f"grenedalf/fst-{window}-{method}.csv"
        )

# popoolation
for method in ["kofler","karlsson"]:
    for window in [1000]:
        run_fst( "popoolation/fst.sh", { "window": window, "method": method })
        collect_results(
            f"popoolation/fst/split_*-{window}-{method}.fst",
            f"popoolation/fst-{window}-{method}.csv"
        )

# poolfstat
for method in ["Anova","Identity"]:
    for window in [1000, 100]:
        run_fst( "poolfstat/fst.sh", { "window": window, "method": method })
        collect_results(
            f"poolfstat/fst/fst-split_*-{window}-{method}.txt-fst.csv",
            f"poolfstat/fst-{window}-{method}.csv"
        )
