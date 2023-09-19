#!/usr/bin/env python3

import sys, os

from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
import seaborn as sns

# Standard embeddings
# https://stackabuse.com/guide-to-multidimensional-scaling-in-python-with-scikit-learn/
from sklearn.manifold import MDS, TSNE
from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances
import sklearn.datasets as dt

# Also trying UMAP
# https://umap-learn.readthedocs.io/en/latest/
# https://plotly.com/python/t-sne-and-umap-projections/
from umap import UMAP

# Extra for mantel test
# import skbio
import mantel
from geopy import distance

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

# MDS
# mds = MDS( metric=True, dissimilarity='precomputed', random_state=0 )
# transformed = mds.fit_transform(matrix)

# t-SNE
tsne = TSNE(metric="precomputed", init="random")
transformed = tsne.fit_transform(matrix)

# UMAP
# umap_2d = UMAP(n_components=2, metric="precomputed", init='random', random_state=0)
# transformed = umap_2d.fit_transform(matrix)

# print(transformed)
# print("transformed values",len(transformed))

# make a DataFrame again... ah python...
# df = pd.DataFrame(index=data.index)
# df = pd.DataFrame({ "sample": list(data.index) })
# df = df.join(pd.DataFrame(transformed, columns = ['x','y']))
df = pd.DataFrame(transformed, columns = ['x','y'], index=data.index)
print(df)

# ------------------------------------------------------------
#     meta-data
# ------------------------------------------------------------

samples = pd.read_csv( "grene-master/data/samples_data.csv", header=0, index_col=0 )
locations = pd.read_csv( "grene-master/data/locations_data.csv", header=0, index_col=0 )
# print(samples)
# print(locations)

# For each sample name, look up its site, and from there, its location metadata.
# We here rely on the arrays being in the correct order, as we were working on numpy,
# so there we lost the association with names for a moment...
meta = pd.DataFrame(columns=["site","year","latitude","longitude","altitude"], index=data.index)
for sample in data.index:
    site = samples.loc[sample, "site"]
    meta.loc[sample] = pd.Series({
        "site": samples.loc[sample, "site"],
        "year": samples.loc[sample, "year"],
        "latitude":  locations.loc[site, "latitude"],
        "longitude": locations.loc[site, "longitude"],
        "altitude":  locations.loc[site, "altitude"]
    })
# print(meta)

# Now put that in the same df that we have for the embedding
df = pd.concat([df, meta], axis=1)
# print(df)

# Also we need to convert sites to string, so that seaborn recognizes it as a categorical value...
# and because it's so much fun, we go through int first, to not end up with `.0` in each item...
df['site'] = df['site'].astype(int).astype(str)
print(df)

# ------------------------------------------------------------
#     Mantel
# ------------------------------------------------------------

# This is a simple test for the fst and geo distance correlation.
# Not much, correlation 0.0714, indicating that the first two years have patterns that
# are not just dominated by geo location
if False:
    # Make a distance matrix between all locations in the df
    geo = np.zeros(shape=(len(data.index), len(data.index)))
    for i in range(len(data.index)):
        for j in range(i+1, len(data.index)):
            loc_i = ( df.iloc[i]["latitude"], df.iloc[i]["longitude"] )
            loc_j = ( df.iloc[j]["latitude"], df.iloc[j]["longitude"] )
            dist = distance.distance(loc_i, loc_j).km
            geo[i][j] = dist
            geo[j][i] = dist

    # print(geo)
    np.savetxt(outdir + "/distances.csv", geo, delimiter=",")

    # Fucking skbio does not work, lack of funding or whatever...
    # coeff, p_value = skbio.math.stats.distance.mantel(x=matrix, y=geo, method="pearson")
    correlation, p_value, z_score = mantel.test(matrix, geo, method="pearson")
    print("mantel:", correlation, p_value, z_score)

# ------------------------------------------------------------
#     plotting tests
# ------------------------------------------------------------

plotnum = 1
def plot( value, palette ):
    global plotnum
    print(value)

    # prep and make the plot
    fig = plt.figure(plotnum, figsize=(12, 10))
    ax = fig.add_subplot()
    ax = sns.scatterplot(
        data=df,
        x="x", y="y",
        hue=value,
        palette=palette,
        # palette = cm.viridis_r,
        linewidth=0,
        legend='auto'
    )

    # legend settings do not work like that, we have to _move_ them, duh...
    # https://stackoverflow.com/questions/75526957/seaborn-boxplot-legend-ignoring-colors
    plt.legend(bbox_to_anchor=(1.1, 1), loc='upper right', borderaxespad=0)
    # sns.move_legend(ax, bbox_to_anchor=(1.1, 1), loc='upper right', borderaxespad=0)
    # sns.move_legend(ax, "center right")
    plt.title("t-SNE on FST, " + value)
    ax.set_xlabel( "t-SNE[0]" )
    ax.set_ylabel( "t-SNE[1]" )

    # Safe without dot annotations
    plt.savefig( outdir + "/plot_" + value + ".png", format='png', bbox_inches="tight" )
    plt.savefig( outdir + "/plot_" + value + ".pdf", format='pdf', bbox_inches="tight" )
    plt.savefig( outdir + "/plot_" + value + ".svg", format='svg', bbox_inches="tight" )

    # Add annotations to each dot, to see which sample it is
    # (meant for close inspection, not meant for nice figures)
    def label_point(x, y, val, ax):
        a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
        for i, point in a.iterrows():
            ax.text(point['x']+.02, point['y'], str(point['val']))

    label_point(df["x"], df["y"], df[value], plt.gca())

    # Save again, with dot annotations
    # plt.show()
    plt.savefig( outdir +"/plot_" + value + "_annotated.png", format='png', bbox_inches="tight" )
    plt.savefig( outdir +"/plot_" + value + "_annotated.pdf", format='pdf', bbox_inches="tight" )
    plt.savefig( outdir +"/plot_" + value + "_annotated.svg", format='svg', bbox_inches="tight" )
    plt.close( plotnum )
    plotnum += 1

# call the plotting function with different meta-data and colorizations
print("plotting")
plot("site", "husl")
plot("latitude", cm.viridis_r)
plot("year", cm.viridis_r)
