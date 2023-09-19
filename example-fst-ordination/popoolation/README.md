# Speed test

Quick test to see how slow popoolation is on the data.
these are the first 1k lines from

    lczech@login.hpc.caltech.edu:~/central/grenephase1/hafpipe-231-fst-all
    
and then turned into a single sync file (s that popoolation can read it).


# Result with grenedalf

    Started 2023-05-02 20:34:26

    Processing 2415 samples

    Computing FST between 2914905 pairs of samples.
    At chromosome 1
    At chromosome 2
    At chromosome 3
    At chromosome 4
    At chromosome 5

    Processed 5 chromosomes with 2946222 (non-filtered) positions in 1 window.
    Total filter summary (after applying all sample filters):
    Passed:               2946222
    Not SNP:              2253

    Finished 2023-05-03 12:56:48


for 

    cat counts-xaa.sync.gz | wc -l 
    15982348

positions


# Result with PoPoolation

On the 1000 subpositions... okay doesn't work at all. giving up on this test...
trying with a single line instead. does not work if the line is position "1", so we use "2" instead.
probably due to their off by one error in the position...

head -n 1 counts.sync | sed "s/\t524\t/\t1\t/g" > line1.txt

./fst.sh

    Start Thu 04 May 2023 10:55:34 PM PDT
    End Thu 04 May 2023 10:55:53 PM PDT
    Internal time: 19.329639013

this produces a table with 2914910 columns, 5 fixed columns, and the 2914905 pairs of samples.
all of them "na", not sure what's going on there, but popoolation just does not seem to be able to handle it...

the time above is for a single line, so times 15982348 SNP lines in the the data: 

15982348 SNPs * 19.33s = 9.78 years

that's a lot
