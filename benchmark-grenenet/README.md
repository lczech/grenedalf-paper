# Benchmark on real-world data with increasing number of positions in the files

Here, we benchmark the tools using subsets of two of our GrENE-net samples,
so that we can assess the scaling of grenedalf and other tools
using real-world data.

In particular, we want to benchmark the conversion from bam to pileup to sync,
using an increasing number of positions of the original bam files.

Use the `generate-data/create-subsets.sh` script to generate the data,
and see the script itself for further details.

