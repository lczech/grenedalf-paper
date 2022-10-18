#!/usr/bin/env Rscript

# R.Version()
# library(poolfstat)

args <- commandArgs(trailingOnly = TRUE)
infile <- args[1]
outfile <- args[2]

print(infile)
print(outfile)

library(poolfstat)

# pairwiseFST apparently needs at least three populations... no idea why...
# pooldata=popsync2pooldata(sync.file=infile,poolsizes=rep(100,2))
# resfst=compute.pairwiseFST(pooldata)

pooldata=popsync2pooldata(sync.file=infile,poolsizes=rep(100,2))
resfst=computeFST(pooldata,sliding.window.size=1000)

sink(outfile)
resfst
sink()
