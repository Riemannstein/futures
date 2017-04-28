import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import os
import time
from statsmodels.tsa.stattools import adfuller
from param import *
from function import *

# Create directory if not existed
if not os.path.exists("./data_"+data_date+"/"):
	os.makedirs("./data_"+data_date+"/")
	
if not os.path.exists("./data_"+data_date+"_debug/"):
	os.makedirs("./data_"+data_date+"_debug/")
	
# Iterate over all the contracts
for j in range(len(ticker_list)):
	
	# Read the data
	df = pd.read_csv("../data/tick_"+data_date+"/"+ticker_list[j]+"_"+data_date+".csv", encoding = "GBK")
	contract = pd.read_csv("../data/contract_20170413/"+ticker_list[j]+".csv", encoding = "GBK")
	start_index = 0 # get the start index of the dataframe

	# Get the index of the first tick
	for i in range(len(df)):
		print(type(df.iloc[i]["dataTime"]), df.iloc[i]["dataTime"])
		if df.iloc[i]["dataTime"] == "09:00:00" or df.iloc[i]["dataTime"] == "21:00:00":
			start_index = i
			break
	print("The starting tick has index ", start_index)
	
	# Delete the first two rows
	df = df.iloc[start_index:]
	
	# Dropna
	df = df.dropna(subset=["lastPrice","askPrice1","bidPrice1"])
	
	# Setting data length according to debugging mode
	if debug == 1:
		data_len = data_len_debug
	else:
		data_len = len(df)

	# Get the minimum price change
	minPriceChange = contract.iloc[0]["minChgPriceNum"]
	print("minPriceChange for contract", ticker_list[j], "is ", minPriceChange)



