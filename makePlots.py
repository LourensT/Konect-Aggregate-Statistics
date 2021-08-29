import os
import pandas as pd

import matplotlib.pyplot as plt

# python interface for creating stylized plots
from TikzPlotsFromPython.GenerateTikz import GenerateTikz

BASE_FP = os.getcwd() + "\\plots\\"
size_min = 0

def make_plot(index, metric, xlog, ylog):
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

    # filter the dataframe
    df = pd.read_csv("dataset.csv")
    print("dataframe shape before filter", df.shape)
    df = df[(df["Category"] != "Infrastructure network") & (df["Size"] >= size_min)]
    print("dataframe shape after filter", df.shape)

    df_dict = df.set_index(index)[metric].to_dict()
    plot = GenerateTikz(BASE_FP + fp, documentation="Plot of Konect networks without Infrastructure networks and with size > {}, total number of networks {}".format(size_min, df.shape[0]))
    plot.setConfiguration(0, max(df_dict.keys()), 0, max(df_dict.values()), xlog=xlog, ylog=ylog, xlabel=index, ylabel=metric)
    plot.addSeries(df_dict, metric)




# N>1000(?)
size_min = 1000
# log netwerk size - log maximum degree
make_plot("Size", "Maximum degree", True, True)
# log netwerk size - log maximum indegree
make_plot("Size", "Maximum indegree", True, True)

size_min = 0
# log netwerk size - log average degree
make_plot("Size", "Average degree", True, True)
# log netwerk size - log average indegree (0.5*average degree)
# TODO decide to split up undirected vs directed logs

# size N>1000(?)
size_min = 1000
# 	(ook zonder log proberen)
# log(size)	- 50-Percentile effective diameter
make_plot("Size", "50-Percentile effective diameter", True, False)
# log(size)	- 90-Percentile effective diameter
make_plot("Size", "90-Percentile effective diameter", True, False)

# unipartite undirected
# size - proportion van largest component (Relative size of LC)
# TODO

# directed
# size - proportion van giant  component (Relative size of LSCC)
# TODO

# size N>1000(?)
size_min = 1000
# size 		- diameter	
make_plot("Size", "Diameter", False, False)
# log(size)	- diameter 	(verwacht lineare trend in wolk omhoog)
make_plot("Size", "Diameter", True, False)

# size N>1000(?)
size_min = 1000
# size 		- clustering coefficient	(real world meer clustering dan random graphs)
make_plot("Size", "Clustering coefficient", False, False)