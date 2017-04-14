import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *

# Data used for preprocessing, overide
data_date = "20170413"
print("Data date is ", data_date)

# Initialize tv_to_disp_array
tv_to_disp_array = np.zeros(len(ticker_list))

for i in range(len(ticker_list)):
	# Read the data
	df = pd.read_csv("../data/tick_"+data_date_before+"/"+ticker_list[i]+"_"+data_date_before+".csv", encoding = "GBK")
	
	start_index = 0 # get the start index of the dataframe
	
	# Get the index of the first tick
	for k in range(len(df)):
		if df.iloc[k]["lowPrice"] != 0:
			start_index = k
			break

	# Delete the first two rows
	df = df.iloc[start_index:]
	
	# Sum of the absolute value of the change in price
	tv = 0.0

	# Absolute value of the difference between close and open price 
	displacement = abs( df.iloc[-1]["closePrice"] - df.iloc[-1]["openPrice"] )
	
	# Compute the total variation to displacement ratio
	tv_to_disp = 0.0

	for j in range(len(df)):
		if j == 0:
			tv = 0.0
		else:
			tv += abs( df.iloc[j]["lastPrice"] - df.iloc[j-1]["lastPrice"] )

	print("The total variation of the lastPrice series is ", tv)

	if displacement == 0:
		tv_to_disp = float("inf")
	else:
		tv_to_disp = tv/float(displacement)
	
	tv_to_disp_array[i] = tv_to_disp

np.savetxt("tv_to_disp_array_"+data_date+".txt", tv_to_disp_array)


