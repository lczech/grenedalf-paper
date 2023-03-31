#!/bin/bash

####################################################################################################
#     Setup
####################################################################################################

# Some setup. Need this for accuracy calculations using `bc`,
# which otherwise might not work on eg German computers with "," being the decimal separator...
LC_NUMERIC=C
LC_COLLATE=C

# Default number of speed runs:
ITERATIONS=1

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
        sleep 1

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
#     Main Loop
####################################################################################################

# Change to test dir. This ensures that the script can be called from any directory.
cd "$(dirname "$0")"

GRENEDALF="/home/lucas/Dropbox/GitHub/grenedalf/bin/grenedalf"
mkdir -p "grenedalf-logs"

# directory with the samples we are using
MAPPED="/home/lucas/Projects/grenephase1/mapped"

mkdir -p "sample-sync"

# On screen output
echo "Start: `date`"
echo
echo "Command                       Data                                   Size         Min         Max         Avg         Mem        User          Wall "

# Init result files.
# Here, we write the files with one measurement per line, for all tools,
# instead of one tool per line for all measurements.
# This is easier to set up, given the way that we process the samples here.
# To still be able to use our plot script easily later, we simply transpose afterwards.
echo -e "Samples\tgrenedalf\tpoolfstat\tpopoolation2" > measure_time.csv
echo -e "Samples\tgrenedalf\tpoolfstat\tpopoolation2" > measure_memory.csv

# we create the sync files on the fly, and might delete them afterwards,
# as they otherwise take up too much disk space for my poor little laptop ;-)
# that is a bit wasteful when repeating the measurement, but we can live with it.
for NUMSAM in `seq 7 10` ; do
    #echo `date`

    # select the first n samples, and create a sync file from them
    DATA=`ls ${MAPPED}/*.bam | sort | head -n ${NUMSAM}`
    
    # build command line for grenedalf
    INPATHS=""
    for D in ${DATA} ; do
        INPATHS="${INPATHS} --sam-path ${D}"
    done

    # run grenedalf to get a sync file
    #echo "creating sync for ${NUMSAM} samples"
    if [ ! -f "sample-sync/counts-${NUMSAM}.sync" ] ; then
        ${GRENEDALF} sync-file ${INPATHS} --allow-file-overwriting --out-dir "sample-sync" --file-suffix "-${NUMSAM}" \
            > "grenedalf-logs/sync-samples-${NUMSAM}.log" 2>&1
    fi

    echo -n "${NUMSAM}" >> "measure_time.csv"
    echo -n "${NUMSAM}" >> "measure_memory.csv"

    run_test "grenedalf/fst-sync.sh"   "Samples-${NUMSAM}" "${NUMSAM}" "../sample-sync/counts-${NUMSAM}.sync"
    run_test "poolfstat/fst.sh"        "Samples-${NUMSAM}" "${NUMSAM}" "../sample-sync/counts-${NUMSAM}.sync"
    run_test "popoolation/fst.sh"      "Samples-${NUMSAM}" "${NUMSAM}" "../sample-sync/counts-${NUMSAM}.sync"
    
    # remove file again to save disk space
    #rm "sample-sync/counts-${NUMSAM}.sync"

    echo >> "measure_time.csv"
    echo >> "measure_memory.csv"   
done

echo
echo "End: `date`"

####################################################################################################
#     Finalize Output
####################################################################################################

function transpose() {
    awk '
    { 
        for (i=1; i<=NF; i++)  {
            a[NR,i] = $i
        }
    }
    NF>p { p = NF }
    END {    
        for(j=1; j<=p; j++) {
            str=a[1,j]
            for(i=2; i<=NR; i++){
                str=str"\t"a[i,j];
            }
            print str
        }
    }' $1 > $1.tmp
    rm $1
    mv $1.tmp $1
}

transpose "measure_time.csv"
transpose "measure_memory.csv"  

