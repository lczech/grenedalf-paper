#!/usr/bin/env Rscript

# R.Version()
# library(poolfstat)

args <- commandArgs(trailingOnly = TRUE)
infile <- args[1]
window <- strtoi(args[2])
outfile <- args[3]

print(infile)
print(window)
print(outfile)

library(poolfstat)

# pairwiseFST apparently needs at least three populations... no idea why...
# pooldata=popsync2pooldata(sync.file=infile,poolsizes=rep(100,2))
# resfst=compute.pairwiseFST(pooldata)

pooldata=popsync2pooldata(sync.file=infile,poolsizes=rep(100,2))

if (window > 0) {
    resfst=computeFST(pooldata,sliding.window.size=window)
} else {
    resfst=computeFST(pooldata)
}

sink(outfile)
resfst
sink()

print("done")
