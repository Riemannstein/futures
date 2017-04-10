import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

ticker = "al1705" # contract symbol
minPriceChange = 5.0 # minimum price change for the contract

# debug mode: 1
debug = 1

k = int(1) # times of minimum price change

# Read the data
df = pd.read_csv(ticker+".csv", encoding = "GBK")

# Delete the first two rows
df = df.iloc[2:]

spread = 

# Setting data length according to debugging mode
if debug == 1:
	data_len = 100
else:
	data_len = len(df)
