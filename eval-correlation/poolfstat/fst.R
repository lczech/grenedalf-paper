#!/usr/bin/env Rscript

# R.Version()
# library(poolfstat)

args <- commandArgs(trailingOnly = TRUE)
infile <- args[1]
window <- strtoi(args[2])
method <- args[3]
outfile <- args[4]

print(infile)
print(outfile)

library(poolfstat)

# pairwiseFST apparently needs at least three populations... no idea why...
# pooldata=popsync2pooldata(sync.file=infile,poolsizes=rep(100,2))
# resfst=compute.pairwiseFST(pooldata)

pooldata=popsync2pooldata(
    sync.file=infile, poolsizes=rep(100,2),
    min.rc=2, min.cov.per.pool = 4, max.cov.per.pool = 100, min.maf = 0.0
)

resfst=computeFST(pooldata,sliding.window.size=window,method=method)

sink(outfile)
resfst
sink()

write.table( resfst$snp.FST, file = paste0(outfile, "-snps.csv"), sep = ",")
write.table( resfst$sliding.windows.fst, file = paste0(outfile, "-sliding.csv"), sep = ",")
