#!/usr/bin/env python3

import sys, os

from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
import seaborn as sns

from scipy.spatial.distance import pdist, squareform
from sklearn import datasets
from fastcluster import linkage

# https://gmarti.gitlab.io/ml/2017/09/07/how-to-sort-distance-matrix.html

def seriation(Z,N,cur_index):
    '''
        input:
            - Z is a hierarchical tree (dendrogram)
            - N is the number of points given to the clustering process
            - cur_index is the position in the tree for the recursive traversal
        output:
            - order implied by the hierarchical tree Z

        seriation computes the order implied by a hierarchical tree (dendrogram)
    '''
    if cur_index < N:
        return [cur_index]
    else:
        left = int(Z[cur_index-N,0])
        right = int(Z[cur_index-N,1])
        return (seriation(Z,N,left) + seriation(Z,N,right))

def compute_serial_matrix(dist_mat,method="ward"):
    '''
        input:
            - dist_mat is a distance matrix
            - method = ["ward","single","average","complete"]
        output:
            - seriated_dist is the input dist_mat,
              but with re-ordered rows and columns
              according to the seriation, i.e. the
              order implied by the hierarchical tree
            - res_order is the order implied by
              the hierarhical tree
            - res_linkage is the hierarhical tree (dendrogram)

        compute_serial_matrix transforms a distance matrix into
        a sorted distance matrix according to the order implied
        by the hierarchical tree (dendrogram)
    '''
    N = len(dist_mat)
    flat_dist_mat = squareform(dist_mat)
    res_linkage = linkage(flat_dist_mat, method=method,preserve_input=True)
    res_order = seriation(res_linkage, N, N + N-2)
    seriated_dist = np.zeros((N,N))
    a,b = np.triu_indices(N,k=1)
    seriated_dist[a,b] = dist_mat[ [res_order[i] for i in a], [res_order[j] for j in b]]
    seriated_dist[b,a] = seriated_dist[a,b]

    return seriated_dist, res_order, res_linkage

# ------------------------------------------------------------
#     embedding
# ------------------------------------------------------------

# infile = "hafpipe-231-fst-subset/fst-matrix-concise.csv"
# outdir = "plots-subset"
infile = "hafpipe-231-fst-all/fst-matrix-concise.csv"
outdir = "plots-all"

data = pd.read_csv( infile, header=0, index_col=0 )
matrix = data.to_numpy( copy=True )
matrix = matrix.clip(min=0)
print(data)


# methods = ["ward","single","average","complete"]
# methods = ["ward","average","complete"]
methods = ["average"]
plotnum = 1
for method in methods:
    print("Method:\t",method)
    ordered_dist_mat, res_order, res_linkage = compute_serial_matrix(data.to_numpy(),method)

    plotnum = 1
    fig = plt.figure(plotnum, figsize=(14, 12))
    # ax = fig.add_subplot()
    sns.heatmap(ordered_dist_mat, cmap="inferno_r")
    # plt.show()
    plt.savefig( "plot_heatmap_" + method + ".png", format='png', bbox_inches="tight" )
    plotnum += 1
