"""
Created on 201702

@author: Klaus G. Paul

licence: This package is released under https://www.gnu.org/licenses/gpl GNU General Public License 3, and is provided as is without any warranty.

"""

import numpy as np
import matplotlib.cm as cm
from matplotlib.pyplot import figure, show, rc, NullFormatter
from matplotlib.lines import Line2D
import pandas as pd
import random

df =pd.read_excel("data.xlsx")
df["complete"] = df.Finished/df.Total
df = df.replace(np.inf,0.0)
df = df.sort_values("complete",ascending=False).reset_index()
df["width"] = df.Total/df.Total.sum()*2*np.pi

fig = figure(figsize=(8,8))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)

for item in [fig, ax]:
    item.patch.set_visible(False)
    
ax.spines["polar"].set_visible(False)

N = len(df)
theta = np.arange(0.0, 2*np.pi, 2*np.pi/N)

df["theta"] = 0.
df.set_value(0,"theta",0.)
for i in range(1,N):
    theta = 0.
    for j in range(0,i):
        theta += df.width[j]
    df.set_value(i,"theta",theta)
bars = ax.bar(df.theta, df.complete, width=df.width, bottom=0.0)

for r,bar in zip(df.complete, bars):
    bar.set_facecolor( cm.viridis(r))
    print r,
    bar.set_alpha(0.5)
ax.get_xaxis().set_visible(False)
ax.set_ylim([0.0,2.])

labels = ["" for i in range(N)]
for i in range(N):
    labels[i] = "%.1f%% %s"%(df.complete[i]*100,df.Module[i])

pos = np.arange(0.,N)
pos[0] = df.width[0]/2.
for i in range(1,N):
    pos[i] = 0
    for j in range(0,i):
        pos[i] += df.width[j]
    pos[i] += df.width[i]/2

for i in range(N):
    ax.annotate(xy=(pos[i],df.complete[i]),xytext=(pos[i],1.6+random.random()*0.5),s=labels[i],horizontalalignment='center',
                arrowprops=dict(facecolor='black', width=1,headwidth=1.0),)

ax.set_yticks([1./3.,2./3.,1.0])
ax.yaxis.grid(True,which='major')
ax.yaxis.set_major_formatter(NullFormatter())
                
show()