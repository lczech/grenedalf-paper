#!/usr/bin/python3

import sys, os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

if len(sys.argv) != 2:
    raise Exception("Need file")
table=sys.argv[1]
image=os.path.splitext(table)[0] + ".pdf"

xname = "Min Coverage ; Poolsize"
yname = "Tajima's D bug/fix"

data=pd.read_csv(table, sep='\t')
df = data.melt(var_name=xname, value_name=yname)

sns.set_theme(style="whitegrid")
plt.figure(figsize=(30, 20))
plt.ylim(0, 11)
# plt.yticks([range(0, 11)])
# sns.set_style("ticks", {"ytick.major.size":1})
plt.yticks(np.arange(0, 10))

ax = sns.violinplot(x=xname, y=yname, data=df, scale="width").set_title(os.path.splitext(table)[0])

# plt.show()
plt.savefig(image, bbox_inches='tight')
