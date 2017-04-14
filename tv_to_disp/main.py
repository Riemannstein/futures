import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools

debug = 0

# ticker lists
ticker_list_shfe = ["ag1706", "al1706", "au1706", "bu1706", "cu1706",  "hc1710", "ni1709", "pb1705", "rb1710", "ru1709", "sn1705", "zn1706"]
ticker_list_xdce = ["a1709", "c1709", "cs1709", "i1709", "j1709", "jd1709", "jm1709", "l1709", "m1709", "p1709", "pp1709", "v1709", "y1709"]
ticker_list_xzce = ["CF709", "FG709", "MA709","OI709", "RM709", "SF705", "SM705", "SR709", "TA709", "WH705", "ZC705"]
ticker_list_ccfx = ["IF1704", "IC1704", "IH1704", "TF1706", "T1706"]
data_date = "20170413"

# 

if debug == 1:
	ticker_list = ["ag1706", "a1709", "CF709", "IF1704"]
else:
	ticker_list = ticker_list_shfe + ticker_list_xdce + ticker_list_xzce + ticker_list_ccfx

# Initialize tv_to_disp_array
tv_to_disp_array = np.zeros(len(ticker_list))

for i in range(len(ticker_list)):
	# Read the data
	df = pd.read_csv("../data/tick_"+data_date+"/"+ticker_list[i]+"_"+data_date+".csv", encoding = "GBK")

	# Delete the first two rows
	df = df.iloc[2:]
	
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


