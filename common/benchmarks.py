#!/usr/bin/python3

import subprocess
import sys, os
import re
import time
from datetime import datetime

def data_size( path ):
    # Get the size of the file, or of the whole directory.

    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
    else:
        print("path does not exist: " + path)

def append_to_tables( time, memory,
    time_file="measure_time.csv", memory_file="measure_memory.csv",
    with_date_time=True
):
    # Helper to append results to our table files.
    # Files are immediately closed again, to make sure data is written, in case we crash
    # during over night long benchmarks runs...

    if with_date_time:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S\t")
        time   = now + str(time)
        memory = now + str(memory)
    with open(time_file, "a") as f:
        f.write(str(time))
    with open(memory_file, "a") as f:
        f.write(str(memory))

def run_benchmark( script, args, iterations=1, stdout=None ):
    # Run a test script.
    # The function expects the script to be run, and a dict with key value pairs for the args.
    # We run bash scripts containing the tests, and they parse these args again.
    # Our scripts are then expected to measure time internally, and report it via an echo
    # to stdout containing the string "Internal time: s" in seconds.

    print("=========================================\n")
    print("At " + datetime.now().strftime("%Y-%m-%d %H:%M:%S\t"))
    print(
        "Running " + script + "\n  - " +
        "\n  - ".join([ key + "=" + str(val) for key, val in args.items() ])
    )
    print()

    # Prepare the command to be run.
    # We cannot use normal `time` on Ubuntu, as it is a wrapper that does not have the -v option.
    # Need to run the underlying program instead.
    script=os.path.realpath(script)
    script_path = os.path.dirname(os.path.realpath(script))
    script_name = os.path.basename(os.path.realpath(script))
    script_args = " ".join([ key + "=" + str(val) for key, val in args.items() ])
    command = "/usr/bin/time -v " + script + " " + script_args + " 2>&1"

    # We want to measure all timings
    time_min=0
    time_max=0
    time_sum=0
    memory=0

    # Run as many iterations as needed
    for iteration in range(iterations):
        print("    Iteration " + str(iteration), flush=True)

        # Start the process, capturing everything, and terminating on failure
        time.sleep(1)
        try:
            result = subprocess.run(
                command, cwd=script_path,
                capture_output=True, shell=True, text=True
            )
        except Exception as e:
            print("FAILED")
            print(e)
            break
        if result.returncode != 0:
            print("FAILED")
            print(result.stdout)
            print(result.stderr)
            break

        # Get time (s) and mem (Mb) from script output.
        # We use a few differnt ways for the time, just to make sure.
        match = re.search(r'.*Internal time: ([0-9.]*).*', result.stdout)
        duration = float(match.group(1))
        match = re.search(r'.*Maximum resident set size .kbytes.: ([0-9]*).*', result.stdout)
        memory = float(match.group(1)) / 1024
        match = re.search(r'.*User time .seconds.: ([0-9.]*).*', result.stdout)
        user_time = match.group(1)
        match = re.search(r'.*Elapsed .wall clock. time .h.mm.ss or m.ss.: ([0-9.:]*).*', result.stdout)
        wall_time = match.group(1)
        print("    Time " + str(duration) + "s")
        print("    Mem  " + str(memory) + "Mb")
        print("    User " + str(user_time))
        print("    Wall " + str(wall_time))
        print(flush=True)

        # Set the measurements
        if time_max == 0:
            time_min = duration
            time_max = duration
        else:
            time_min = min(duration, time_min)
            time_max = max(duration, time_max)
        time_sum += duration

        # Just in case, we allow to write the captured timing data.
        # The program being run is usually captured within the script,
        # so we do not see much here...
        if stdout:
            if os.path.dirname(stdout):
                os.makedirs(os.path.dirname(stdout), exist_ok=True)
            with open(stdout, "a") as stdoutfile:
                stdoutfile.write(result.stdout)
                stdoutfile.write(result.stderr)

    # Final output for this test
    time_avg = time_sum / float(iterations)
    print("min " + str(time_min))
    print("max " + str(time_max))
    print("avg " + str(time_avg))
    print("mem " + str(memory))
    print(flush=True)

    # Return the best time, and the memory
    return ( time_min, memory )

def run_suite( sizes, script, args, name=None, iterations=1 ):
    # Run a benchmark using one tool, for different input `sizes`.
    # Takes the list of sizes, the script, and a dict of the script args.

    if not name:
        name = os.path.splitext(script)[0]

    # Run tests for all file sizes
    for size in sizes:
        # Get the file, and run the test
        args["size"] = str(size)
        ( time, memory ) = run_benchmark( script, args, iterations )

        # Get a tab-separated key-value pairs for the results table
        tab_args = "\t".join([ key + "\t" + str(val) for key, val in args.items() ])

        # Immediately write the result.
        # This writes to our predefine table names automatically,
        # because we are lazy and use global names today...
        append_to_tables(
            "{}\t{}\t{}\n".format( name, tab_args, time ),
            "{}\t{}\t{}\n".format( name, tab_args, memory )
        )
