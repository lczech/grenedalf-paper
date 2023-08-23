#!/usr/bin/env python3

# Import packages
import sys, os
import glob
import pandas as pd
import numpy as np

# Import from the independent_check
from typing import List
import tqdm
from pandas import DataFrame
from numpy import sqrt
from scipy.stats import binom

# Speed up the repetitive part
from functools import lru_cache

# ------------------------------------------------------------
#     README
# ------------------------------------------------------------

# On 2023-08-18, we noticed a difference in our equations doc and
# our implementation that was weird, and made us double check.
# This is a small simulation test to verify whether the harmonic
# a_1 needs to be part of the theta watterson computation.
#
# We have two files, simulated as follows: There are 1M sites,
# and every site has coverage 100. The files simply contain the
# number of derived allele reads at positions where that is
# not zero (i.e., a text file with a bunch of rows, and each row
# is just the number of reads with the derived allele).
# One simulation has n=10, one has n=1000, should be clear from
# the file names.
# The theta that we're hoping to estimate is 0.001
#
# Result: Our implementation was correct, and we just had an
# algebraic mistake in our equations document.
# Good that we checked :-D

# ------------------------------------------------------------
#     Functions
# ------------------------------------------------------------

@lru_cache(maxsize=None)
def harmonic(n: float, power: float) -> float:
    """Returns the nth harmonic number of type power"""
    int_n = round(n)
    return sum([1/x**power for x in range(1, int_n+1)])

@lru_cache(maxsize=None)
def binom_pmf(r, n, p):
    return binom.pmf(r, n, p)

@lru_cache(maxsize=None)
def theta_w_denom( n, c_ell, b ):
    den = 0.
    for m in range(b, c_ell - b + 1):
        for k_val in range(1, n):
            den += binom_pmf(m, c_ell, k_val/n) / k_val
    return den

def theta_w_no_harmonic(
    n: int,
    c: List[int],
    k: List[int],
    b: int
) -> float:
    """
    Equation (16)

    n: number of individuals in the pool
    c: list of coverages at each position
    k: number of derived alleles at each position
    b: minimum number of minor alleles to consider
    """
    assert len(c) == len(k)
    to_return = 0.
    for c_ell, k_ell in zip(c, k):
        if k_ell < b or (c_ell - k_ell) < b:
            continue
        to_return += 1.0 / theta_w_denom( n, c_ell, b )

    return to_return / len(c)

# ------------------------------------------------------------
#     Main
# ------------------------------------------------------------

# test files, mapping to their pool size
testfiles = {
    "coverage_100_theta_0.001_n_10.txt": 10,
    "coverage_100_theta_0.001_n_1000.txt": 1000
}

def read_derived_counts_file(infile, w):
    with open(infile) as f:
        derived_counts = [int(x) for x in f.read().split()]
    assert len(derived_counts) < w
    return derived_counts + [0] * (w - len(derived_counts))

# Run everything but the bagel
def main():
    w = 1000000
    c = [100] * w
    b = 2

    for testfile, n in testfiles.items():
        k = read_derived_counts_file(testfile, w)
        assert len(k) == w
        assert len(c) == len(k)

        # Compute both values, according to the equations doc,
        # and according to our implementation, and compare.
        print(testfile)
        tw1 = theta_w_no_harmonic( n, c, k, b )
        a1 = harmonic(n-1, 1)
        tw2 = tw1 / a1

        print("w/o harmonic", tw1)
        print("w/  harmonic", tw2)

if __name__ == '__main__':
    main()
