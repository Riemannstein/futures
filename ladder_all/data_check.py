import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *

df = pd.read_csv("../data/tick_"+data_date+"/"+"al1706"+"_"+data_date+".csv", encoding = "GBK")

print(df.iloc[-1]["closePrice"])
print(df.iloc[-1]["openPrice"])
print(df.iloc[-1]["lastPrice"])

