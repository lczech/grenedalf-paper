#!/bin/bash

# Some setup. Need this for accuracy calculations using `bc`,
# which otherwise might not work on eg German computers with "," being the decimal separator...
LC_NUMERIC=C
LC_COLLATE=C

# Default number of speed runs:
ITERATIONS=3

# This script needs some programs.
if [ -z "`which bc`" ] ; then
    echo "Program 'bc' not found. Cannot run this script."
    exit
fi
if [ -z "`which /usr/bin/time`" ] ; then
    # We cannot use normal `time` on Ubuntu, as it is a wrapper that does not have the -v option.
    # Need to run the underlying program instead.
    echo "Program '/usr/bin/time' not found. Cannot run this script."
    exit
fi

rm -f measure_time.csv
rm -f measure_memory.csv

# Run the test `ITERATIONS` times and show execution times.
# Takes the test case as input, returns 0 if successfull.
function run_tests() {
    local min=0 max=0 sum=0 avg mem
    # local s_time e_time

    # Get script to run, ch to its dir
    SCRIPT=${1}
    cd $(dirname "${1}")
    SCRIPT_NAME=./$(basename "${1}")

    # Get the data set to run
    DATA_NAME="${2}"
    DATA="${3}"

    # Get file size
    if [ -f "${DATA}" ]; then
        # FILESIZE=`stat --printf="%s" ${DATA}`
        FILESIZE=`ls -lah ${DATA} | awk -F " " {'print $5'}`b
    elif [ -d "${DATA}" ]; then
        FILESIZE=`du -hsL ${DATA} | sed "s/\t.*//g"`b
    else
        echo "${DATA} does not exist"
    fi

    # Print the line
    printf "%-40s%-40s%15s" ${SCRIPT} ${DATA_NAME} ${FILESIZE}
    # printf ' %.0s' {1..48}

    for i in $(seq 1 ${ITERATIONS}); do
        printf "%3u/%-3u" ${i} ${ITERATIONS}

        # Run test and measure time and memory.
        # This is where the actual script is being run.
        # Its output is immediately captured for processing.
        # s_time=`date +%s%N`
        script_out=`/usr/bin/time -v ${SCRIPT_NAME} ${DATA} 2>&1`
        success=$?
        # e_time=`date +%s%N`

        # Break if the test failed. We do not need to repeat it then.
        if [[ ${success} != 0 ]]; then
            break
        fi

        # Set timing counters.
        # duration=`echo "scale=3;(${e_time} - ${s_time})/(10^06)" | bc`
        # duration=`echo ${script_out} | grep "User time (seconds):" | sed "s/.* \([0-9]*\)\$/\1/g"`
        # duration=`echo ${script_out} | sed "s/.*User time .seconds.: \([0-9.]*\).*/\1/g"`
        duration=`echo ${script_out} | sed "s/.*Internal time: \([0-9.]*\).*/\1/g"`
        if [[ ${max} == 0 ]]; then
            min=${duration}
            max=${duration}
        else
            if [[ `echo "${duration} > ${max}" | bc` == 1 ]]; then
                max=${duration}
            fi
            if [[ `echo "${duration} < ${min}" | bc` == 1 ]]; then
                min=${duration}
            fi
        fi
        sum=`echo "${sum} + ${duration}" | bc`
        printf "\b\b\b\b\b\b\b"
    done
    printf ' %.0s'  {1..7}
    printf '\b%.0s' {1..7}
    # printf '\b%.0s' {1..48}

    # Print execution time summaries.
    if [[ ${success} == 0 ]]; then
        avg=`echo "scale=3;${sum}/${ITERATIONS}" | bc`

        printf "% 10.3fs " ${min}
        printf "% 10.3fs " ${max}
        printf "% 10.3fs " ${avg}

        # Format memory needs for nice output.
        mem=`echo ${script_out} | sed "s/.*Maximum resident set size .kbytes.: \([0-9]*\).*/\1/g"`
        mem=`echo "scale=3;${mem}/1024" | bc`
        printf "% 10.3fMb" ${mem}
        # echo "Mem: $(( ${mem_out} / 1024 )) Mb"

        # Use `time` to get alternative measurements of exec time for consistency checks.
        usrt=`echo ${script_out} | sed "s/.*User time .seconds.: \([0-9.]*\).*/\1/g"`
        # syst=`echo ${script_out} | sed "s/.*System time .seconds.: \([0-9.]*\).*/\1/g"`
        wallt=`echo ${script_out} | sed "s/.*Elapsed .wall clock. time .h.mm.ss or m.ss.: \([0-9.:]*\).*/\1/g"`
        printf "% 10.3fs " ${usrt}
        # printf "% 10.3fs " ${syst}
        printf "% 10s \n" ${wallt}

        # Print to tab files for easier post-processing
        echo -en "\t${min}" >> "../measure_time.csv"
        echo -en "\t${mem}" >> "../measure_memory.csv"
    else
        echo "Fail!"
    fi

    # Change back to prev dir.
    cd - > /dev/null

    return ${success}
}

function run_pileup() {
    DATA_DIR="../data/pileup"

    echo -n "$1" >> "measure_time.csv"
    echo -n "$1" >> "measure_memory.csv"

    # # ITERATIONS=1
    run_tests $1 random-pileup-1000      "${DATA_DIR}/random-1000.pileup"
    run_tests $1 random-pileup-2000      "${DATA_DIR}/random-2000.pileup"
    run_tests $1 random-pileup-5000      "${DATA_DIR}/random-5000.pileup"
    run_tests $1 random-pileup-10000     "${DATA_DIR}/random-10000.pileup"
    run_tests $1 random-pileup-20000     "${DATA_DIR}/random-20000.pileup"
    run_tests $1 random-pileup-50000     "${DATA_DIR}/random-50000.pileup"
    run_tests $1 random-pileup-100000    "${DATA_DIR}/random-100000.pileup"
    run_tests $1 random-pileup-200000    "${DATA_DIR}/random-200000.pileup"
    run_tests $1 random-pileup-500000    "${DATA_DIR}/random-500000.pileup"
    # ITERATIONS=3
    run_tests $1 random-pileup-1000000   "${DATA_DIR}/random-1000000.pileup"
    run_tests $1 random-pileup-2000000   "${DATA_DIR}/random-2000000.pileup"
    # ITERATIONS=1
    run_tests $1 random-pileup-5000000   "${DATA_DIR}/random-5000000.pileup"
    run_tests $1 random-pileup-10000000  "${DATA_DIR}/random-10000000.pileup"
    run_tests $1 random-pileup-20000000  "${DATA_DIR}/random-20000000.pileup"
    run_tests $1 random-pileup-50000000  "${DATA_DIR}/random-50000000.pileup"
    run_tests $1 random-pileup-100000000  "${DATA_DIR}/random-100000000.pileup"

    echo >> "measure_time.csv"
    echo >> "measure_memory.csv"
}

function run_sync() {
    DATA_DIR="../data/sync"

    echo -n "$1" >> "measure_time.csv"
    echo -n "$1" >> "measure_memory.csv"

    # ITERATIONS=1
    run_tests $1 random-sync-1000      "${DATA_DIR}/random-1000.sync"
    run_tests $1 random-sync-2000      "${DATA_DIR}/random-2000.sync"
    run_tests $1 random-sync-5000      "${DATA_DIR}/random-5000.sync"
    run_tests $1 random-sync-10000     "${DATA_DIR}/random-10000.sync"
    run_tests $1 random-sync-20000     "${DATA_DIR}/random-20000.sync"
    run_tests $1 random-sync-50000     "${DATA_DIR}/random-50000.sync"
    run_tests $1 random-sync-100000    "${DATA_DIR}/random-100000.sync"
    run_tests $1 random-sync-200000    "${DATA_DIR}/random-200000.sync"
    run_tests $1 random-sync-500000    "${DATA_DIR}/random-500000.sync"
    # # ITERATIONS=3
    run_tests $1 random-sync-1000000   "${DATA_DIR}/random-1000000.sync"
    run_tests $1 random-sync-2000000   "${DATA_DIR}/random-2000000.sync"
    # ITERATIONS=1
    run_tests $1 random-sync-5000000   "${DATA_DIR}/random-5000000.sync"
    run_tests $1 random-sync-10000000  "${DATA_DIR}/random-10000000.sync"
    run_tests $1 random-sync-20000000  "${DATA_DIR}/random-20000000.sync"
    run_tests $1 random-sync-50000000  "${DATA_DIR}/random-50000000.sync"
    run_tests $1 random-sync-100000000  "${DATA_DIR}/random-100000000.sync"

    echo >> "measure_time.csv"
    echo >> "measure_memory.csv"
}

echo "Start: `date`"
echo
echo "Command                                 Data                                             Size         Min         Max         Avg         Mem        User          Wall "

# Run either all known scripts, or the one provided.
if [ $# -eq 0 ] ; then

    # Diversity
    ITERATIONS=5
    run_pileup grenedalf/diversity.sh
    ITERATIONS=1
    # run_pileup popoolation/pi.sh
    # run_pileup popoolation/theta.sh
    run_pileup popoolation/d.sh

    # # F_ST
    # ITERATIONS=5
    # run_sync grenedalf/fst.sh
    # ITERATIONS=1
    # run_sync popoolation/fst.sh

else
    #run_tests ${1} ${2}
    echo "Nothing to do"
fi

echo
echo "End: `date`"
