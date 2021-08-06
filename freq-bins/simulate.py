#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

samples_per_bin = 1000
sigma = 6

values = []
for mu in [ 0, 20, 40, 60, 80, 100 ]:
    v = []
    while len(v) < samples_per_bin:
        s = np.random.normal(mu, sigma)
        if s > 0 and s < 100:
            v.append(s)
    # values.append(v)
    values += v

# print(values)

count, bins, ignored = plt.hist(values, 100, histtype="barstacked")

# plt.show()
plt.savefig("hist_" + str(sigma) + ".pdf", format='pdf')
