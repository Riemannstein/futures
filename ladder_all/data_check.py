import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *

df = pd.read_csv("../data/tick_"+"20170413"+"/"+"IH1704"+"_"+"20170413"+".csv", encoding = "GBK")

print(df.iloc[-1]["closePrice"])
print(df.iloc[-1]["openPrice"])
print(df.iloc[-1]["lastPrice"])

