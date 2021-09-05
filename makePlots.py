import os
import pandas as pd

import matplotlib.pyplot as plt

# python interface for creating stylized plots
from TikzPlotsFromPython.GenerateTikz import GenerateTikz

BASE_FP = os.getcwd() + "\\plots\\"
size_min = 0
df = pd.read_csv("dataset.csv")

def make_plot(df, index, metric, xlog, ylog):
    global size_min

    if xlog:
        if ylog:
            fp = ("log_" + index + "-log_" + metric + ".tikz").replace(" ", "_")
        else:
            fp = ("log_" + index + "-" + metric + ".tikz").replace(" ", "_")
    else:
        if ylog:
            fp = (index + "-log_" + metric + ".tikz").replace(" ", "_")
        else:
            fp = (index + "-" + metric + ".tikz").replace(" ", "_")

    print("++ " + fp)

    # filter the dataframe on
    # - minimum size
    # - not a Infrastructure network
    # - TODO inspect to also filter http://konect.cc/networks/dbpedia-location/
    print("dataframe shape before filter", df.shape)
    df = df[(df["Category"] != "Infrastructure network") & (df["Size"] >= size_min)]
    print("dataframe shape after filter", df.shape)

    df_dict = df.set_index(index)[metric].dropna().to_dict()
    plot = GenerateTikz(BASE_FP + fp, documentation="Plot of Konect networks without Infrastructure networks and with size > {}, total number of networks {}".format(size_min, df.shape[0]))
    plot.setConfiguration(min(df_dict.keys()), max(df_dict.keys()), min(df_dict.values()), max(df_dict.values()), xlog=xlog, ylog=ylog, xlabel=index, ylabel=metric)
    plot.addSeries(df_dict, metric)



N = 10000

# N>1000(?)
size_min = N
# log netwerk size - log maximum degree
make_plot(df, "Size", "Maximum degree", True, True)
# log netwerk size - log maximum indegree
make_plot(df, "Size", "Maximum indegree", True, True)


size_min = 0
# log netwerk size - log average degree
make_plot(df, "Size", "Average degree", True, True)
# log netwerk size - log average indegree (0.5*average degree)
# TODO decide to split up undirected vs directed logs

# size N>1000(?)
size_min = N
# 	(ook zonder log proberen)
# log(size)	- 50-Percentile effective diameter
df = pd.read_csv("dataset.csv")
make_plot(df, "Size", "50-Percentile effective diameter", True, False)
# log(size)	- 90-Percentile effective diameter
make_plot(df, "Size", "90-Percentile effective diameter", True, False)


size_min = 0
# unipartite undirected
# size - proportion van largest component (Relative size of LCC)
df["Relative size of LCC"] = df["Size of LCC"] / df["Size"]
make_plot(df[df['Attributes'].apply(lambda x : ("Unipartite" in eval(x)) and ("undirected" in eval(x)))], "Size", "Relative size of LCC", False, False)
make_plot(df[df['Attributes'].apply(lambda x : ("Unipartite" in eval(x)) and ("undirected" in eval(x)))], "Size", "Relative size of LCC", True, False)

# directed
# size - proportion van giant  component (Relative size of LSCC)
make_plot(df[df['Attributes'].apply(lambda x : ("directed" in eval(x)))], "Size", "Relative size of LSCC", False, False)
make_plot(df[df['Attributes'].apply(lambda x : ("directed" in eval(x)))], "Size", "Relative size of LSCC", True, False)

# size N>1000(?)
size_min = N
# size 		- diameter	
make_plot(df, "Size", "Diameter", False, False)
# log(size)	- diameter 	(verwacht lineare trend in wolk omhoog)
make_plot(df, "Size", "Diameter", True, False)

# size N>1000(?)
size_min = N
# size 		- clustering coefficient	(real world meer clustering dan random graphs)
make_plot(df, "Size", "Clustering coefficient", False, False)