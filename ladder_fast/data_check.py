import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *

df = pd.read_csv("../data/tick_"+data_date+"/"+"al1706"+"_"+data_date+".csv", encoding = "GBK")

start_index = 0 # get the start index of the dataframe

# Get the index of the first tick
for i in range(len(df)):
	if df.iloc[i]["lowPrice"] != 0:
		start_index = i
		break
print("The starting tick has index ", start_index)

# Delete the first two rows
df = df.iloc[start_index:]

for i in range(20):
	print("\n", i)
	print("Last price: ", df.iloc[i]["lastPrice"])
	print("Bid price 1: ", df.iloc[i]["bidPrice1"])
	print("askPrice 1: ", df.iloc[i]["askPrice1"])



