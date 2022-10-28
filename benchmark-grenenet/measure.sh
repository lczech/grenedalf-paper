#!/bin/bash

####################################################################################################
#     Setup
####################################################################################################

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

####################################################################################################
#     Single Test Run
####################################################################################################

# Run the test `ITERATIONS` times and show execution times.
# Takes the test case as input, returns 0 if successfull.
function run_test() {
    local min=0 max=0 sum=0 avg mem
    # local s_time e_time

    # Get script to run, ch to its dir
    SCRIPT=${1}
    cd $(dirname "${1}")
    EXEC=./$(basename "${1}")

    # Get the data set to run
    NAME="${2}"
    SIZE="${3}"
    DATA="${@:4}"

    # Get file size
    # if [ -f "${DATA}" ]; then
    #     # FILESIZE=`stat --printf="%s" ${DATA}`
    #     FILESIZE=`ls -lah ${DATA} | awk -F " " {'print $5'}`b
    # elif [ -d "${DATA}" ]; then
    #     FILESIZE=`du -hsL ${DATA} | sed "s/\t.*//g"`b
    # else
    #     echo "${DATA} does not exist"
    # fi

    # Print the line
    printf "%-30s%-30s%15s" ${SCRIPT} ${NAME} ${SIZE}
    # printf ' %.0s' {1..48}

    for i in $(seq 1 ${ITERATIONS}); do
        printf "%3u/%-3u" ${i} ${ITERATIONS}

        # Run test and measure time and memory.
        # This is where the actual script is being run.
        # Its output is immediately captured for processing.
        # s_time=`date +%s%N`
        script_out=`/usr/bin/time -v ${EXEC} ${NAME} ${DATA} 2>&1`
        success=$?
        # e_time=`date +%s%N`
        # echo $script_out

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

####################################################################################################
#     All Sizes Tests
####################################################################################################

# Ascending order of file sizes (in number of positions along the genome)
# CHUNKS="1000 2000 5000 10000"
# CHUNKS="1000 2000 5000 10000 20000 50000 100000"
CHUNKS="1000 2000 5000 10000 20000 50000 100000 200000 500000 1000000 2000000 5000000 10000000 20000000 50000000 100000000"

# We use the following function to loop over all input file sizes for the tests.
# The function is called for each file type or set of files that we want to run,
# using the below run...() functions. They are only convenience so that the main
# test run calls at the end of this script can remain simple.

# We use different inputs, depending on what the respective tests need:
#  - Only one input file with one sample (S1)
#  - One input file with two samples (S1S2)
#  - Separate input files with two samples (S1_S2)

function run_chunk_tests() {
    # ARGS as expected by the run_test() function:
    #     (1)   script to run
    #     (2)   name of the run
    #     (3)   size of the run
    #     (4..) data files (remainder of args)
    # We here take all of this and run it through eval.
    # We also extract the script name, for reporting in the result tables.

    SCRIPT="${1}"
    echo -n "${SCRIPT}" >> "measure_time.csv"
    echo -n "${SCRIPT}" >> "measure_memory.csv"

    for CHUNK in ${CHUNKS} ; do
        # At some point, run times are long enough so that the repetition does not matter much.
        if [ "$CHUNK" -gt 1000000 ]; then
            ITERATIONS=1
        else
            ITERATIONS=3
        fi

        eval run_test ${@}
    done

    echo >> "measure_time.csv"
    echo >> "measure_memory.csv"
}

# --------------------------------------------------------------------------
#     bam
# --------------------------------------------------------------------------

function run_bam_S1() {
    run_chunk_tests \
        "${1}" "S1-\${CHUNK}" "\${CHUNK}" \
        "../subsets-bam/S1-\${CHUNK}.bam"
}

function run_bam_S1_S2() {
    run_chunk_tests \
        "${1}" "S1-S2-\${CHUNK}" "\${CHUNK}" \
        "../subsets-bam/S1-\${CHUNK}.bam" "../subsets-bam/S2-\${CHUNK}.bam"
}

# --------------------------------------------------------------------------
#     mpileup
# --------------------------------------------------------------------------

function run_mpileup_S1() {
    run_chunk_tests \
        "${1}" "S1-\${CHUNK}" "\${CHUNK}" \
        "../subsets-mpileup/S1-\${CHUNK}.mpileup"
}

function run_mpileup_S1S2() {
    run_chunk_tests \
        "${1}" "S1S2-\${CHUNK}" "\${CHUNK}" \
        "../subsets-mpileup/S1S2-\${CHUNK}.mpileup"
}

function run_mpileup_S1_S2() {
    run_chunk_tests \
        "${1}" "S1_S2-\${CHUNK}" "\${CHUNK}" \
        "../subsets-mpileup/S1-\${CHUNK}.mpileup" "../subsets-mpileup/S2-\${CHUNK}.mpileup"
}

# --------------------------------------------------------------------------
#     sync
# --------------------------------------------------------------------------

function run_sync_S1() {
    run_chunk_tests \
        "${1}" "S1-\${CHUNK}" "\${CHUNK}" \
        "../subsets-sync/S1-\${CHUNK}.sync"
}

function run_sync_S1S2() {
    run_chunk_tests \
        "${1}" "S1S2-\${CHUNK}" "\${CHUNK}" \
        "../subsets-sync/S1S2-\${CHUNK}.sync"
}

function run_sync_S1S2gz() {
    run_chunk_tests \
        "${1}" "S1S2-\${CHUNK}-gz" "\${CHUNK}" \
        "../subsets-sync-gz/S1S2-\${CHUNK}.sync.gz"
}

function run_sync_S1_S2() {
    run_chunk_tests \
        "${1}" "S1_S2-\${CHUNK}" "\${CHUNK}" \
        "../subsets-sync/S1-\${CHUNK}.sync" "../subsets-sync/S2-\${CHUNK}.sync"
}

# --------------------------------------------------------------------------
#     table
# --------------------------------------------------------------------------

function run_table_S1() {
    run_chunk_tests \
        "${1}" "S1-\${CHUNK}" "\${CHUNK}" \
        "../subsets-table/S1-\${CHUNK}.csv"
}

function run_table_S1S2() {
    run_chunk_tests \
        "${1}" "S1S2-\${CHUNK}" "\${CHUNK}" \
        "../subsets-table/S1S2-\${CHUNK}.csv"
}

function run_table_S1_S2() {
    run_chunk_tests \
        "${1}" "S1_S2-\${CHUNK}" "\${CHUNK}" \
        "../subsets-table/S1-\${CHUNK}.csv" "../subsets-table/S2-\${CHUNK}.csv"
}

####################################################################################################
#     Benchmark Tests
####################################################################################################

# On screen output
echo "Start: `date`"
echo
echo "Command                       Data                                   Size         Min         Max         Avg         Mem        User          Wall "

# Init result files
echo -n "Tool" > measure_time.csv
echo -n "Tool" > measure_memory.csv
for c in $CHUNKS ; do
    echo -ne "\t${c}" >> measure_time.csv
    echo -ne "\t${c}" >> measure_memory.csv
done
echo >> "measure_time.csv"
echo >> "measure_memory.csv"

# Run either all known scripts, or the one provided.
if [ $# -eq 0 ] ; then

    # # Conversion
    # run_bam_S1_S2 samtools/mpileup.sh
    # run_bam_S1_S2 grenedalf/sync-bam.sh
    # run_mpileup_S1S2 grenedalf/sync-mpileup.sh
    # run_mpileup_S1S2 popoolation/sync-perl.sh
    # run_mpileup_S1S2 popoolation/sync-java.sh
    #
    # # Diversity
    # run_bam_S1 grenedalf/diversity-bam.sh
    # run_mpileup_S1 grenedalf/diversity-mpileup.sh
    # run_sync_S1 grenedalf/diversity-sync.sh
    # run_mpileup_S1 popoolation/pi.sh
    # run_mpileup_S1 popoolation/theta.sh
    # run_mpileup_S1 popoolation/d.sh

    # F_ST
    run_bam_S1_S2 grenedalf/fst-bam.sh
    run_mpileup_S1S2 grenedalf/fst-mpileup.sh
    # run_mpileup_S1_S2 grenedalf/fst-mpileup.sh
    run_sync_S1S2 grenedalf/fst-sync.sh
    run_sync_S1S2gz grenedalf/fst-sync.sh
    # run_sync_S1_S2 grenedalf/fst-sync.sh
    # run_sync_S1S2 poolfstat/fst.sh
    # run_sync_S1S2 popoolation/fst.sh

else
    #run_test ${1} ${2}
    echo "Nothing to do"
fi

echo
echo "End: `date`"
