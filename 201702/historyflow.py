"""
Created on 201702

@author: Klaus G. Paul

licence: This package is released under https://www.gnu.org/licenses/gpl GNU General Public License 3, and is provided as is without any warranty.

This package is inspired by IBM Research History Flow https://www.research.ibm.com/visual/projects/history_flow/
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

folder = "examples/doors"

dfIndex = pd.read_table(folder+"/index",names=["file","baselineID","baselineComment","datetime"])
dfIndex.datetime = pd.to_datetime(dfIndex.datetime)

dfDocument = pd.DataFrame([])

for idx,entry in dfIndex.iterrows():
    with open(folder+"/"+entry["file"],"rt") as docfile:
        document = []
        docdata = docfile.readlines()
        for i in range(len(docdata)):
            line = docdata[i].strip().split(" ",1)         
            document.append({"ID":entry["baselineID"],"line":i,"reqID":line[0],"reqText":line[1],
                             "datetime":entry.datetime})
        dfDocument = dfDocument.append(document)
dfDocument = dfDocument.reset_index()
del dfDocument["index"]
dfDocument.datetime = pd.to_datetime(dfDocument.datetime)

reqIDs = dfDocument.reqID.unique()

dfDocument["version"] = 1
dfDocument["age"] = 0

for r in reqIDs:
    entries = dfDocument[dfDocument.reqID == r].index.tolist()
    for i in range(1,len(entries)):
        if dfDocument.loc[entries[i]].reqText != dfDocument.loc[entries[i-1]].reqText:
            dfDocument.set_value(entries[i],"version",dfDocument.loc[entries[i-1]].version + 1)
        else:
            dfDocument.set_value(entries[i],"age",dfDocument.loc[entries[i-1]].age + 1)

maxAge = float(dfDocument.age.max())
            
fig = plt.figure(figsize=(12,20))

baselines = dfIndex.baselineID.unique()

for i in range(1,len(baselines)):
    x1 = dfIndex.ix[i-1].datetime
    x2 = dfIndex.ix[i].datetime
    entriesFrom = dfDocument[dfDocument.ID == baselines[i-1]].index.tolist()
    for entryFrom in entriesFrom:
        colorIdx = dfDocument.ix[entryFrom].age
        y1 = dfDocument.ix[entryFrom].line
        ddf = dfDocument[dfDocument.ID == baselines[i]]
        ddf = ddf[ddf.reqID == dfDocument.ix[entryFrom].reqID]
        if len(ddf) > 0:
            y2 = ddf.line.values[0]
            alpha = 1.0
            plt.plot([x1,x2],[-y1,-y2],"k-",alpha=alpha,color=cm.Spectral(colorIdx/maxAge))
_ = plt.show() 

