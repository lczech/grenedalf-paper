#!/usr/bin/env Rscript

# R.Version()
library(poolfstat)
library(stringr)

args <- commandArgs(trailingOnly = TRUE)
infile <- args[1]
outfile <- args[2]


print(infile)
print(outfile)

# pairwiseFST apparently needs at least three populations... no idea why...
# pooldata=popsync2pooldata(sync.file=infile,poolsizes=rep(100,2))
# resfst=compute.pairwiseFST(pooldata)

# we get the number of samples form the file name.
# easier than rewriting our test script to forward that number...
samples <- strtoi(str_extract(infile, "[0-9]+"))
pooldata=popsync2pooldata(sync.file=infile,poolsizes=rep(100,samples))
resfst=compute.pairwiseFST(pooldata)

sink(outfile)
slot(resfst,"values")
sink()

