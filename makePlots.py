import os
import pandas as pd

import matplotlib.pyplot as plt

# python interface for creating stylized plots
from TikzPlotsFromPython.GenerateTikz import GenerateTikz

BASE_FP = os.getcwd() + "\\plots\\"

df = pd.read_csv("dataset.csv")
print(df.shape)
print(df["Diameter"].describe())

df = df[df["Category"] != "Infrastructure network" ]


df_dict = df.set_index("Size")["Maximum degree"].to_dict()
plot = GenerateTikz(BASE_FP + "set.tikz", documentation="Log-log of size-maximum degree, on all networks ~Infrastructure network")
plot.setConfiguration(0, max(df_dict.keys()), 0, max(df_dict.values()), xlog=True, ylog=True)
plot.addSeries(df_dict, "Maximum Degree")

df.plot.scatter(x="Size", y = "Maximum degree", logx=True, logy=True)
plt.show()