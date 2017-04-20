import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant
from statsmodels.tsa.stattools import coint

# Read profit array
profit_array = np.loadtxt("./data/profit_array_"+data_date+".txt")

# Read the open price array
open_price_array = np.loadtxt("./data/open_price_array_"+data_date+".txt")

# Read the tv_to_disp array
tv_to_disp_array = np.loadtxt("./data/tv_to_disp_array_"+data_date_before+".txt")

# Compute the normalized profit array
profit_normalized = np.divide(profit_array, open_price_array)

# Compute the log of total variation
log_tv_to_disp_array = np.log(tv_to_disp_array)


# Plot profit/openPrice against total variation
for i in range(len(profit_array)):
	plt.scatter(tv_to_disp_array[i], profit_normalized[i], color="r")
	plt.xlabel("Total variation " + data_date_before)
	plt.ylabel("Profit / openPrice " + data_date)
plt.savefig("./plot/profit_normalized_to_indicator_"+data_date+".eps", format="eps")
plt.close()

# Plot profit against total variation
for i in range(len(profit_array)):
	plt.scatter(tv_to_disp_array[i], profit_array[i], color="r")
	plt.xlabel("Total variation " + data_date_before)
	plt.ylabel("Profit " + data_date)
plt.savefig("./plot/profit_to_indicator_"+data_date+".eps", format="eps")
plt.close()

# Plot profit/openPrice against log total variation
for i in range(len(profit_array)):
	plt.scatter(log_tv_to_disp_array[i], profit_normalized[i], color="r")
	plt.xlabel("log Total variation " + data_date_before)
	plt.ylabel("Profit / openPrice " + data_date)
plt.savefig("./plot/profit_normalized_to_log_indicator_"+data_date+".eps", format="eps")
plt.close()

# Compute the average profit per contract
profit_avg = sum(profit_array)/len(profit_array)
print("Average profit for all the contract is ", profit_avg)

# Compute the average profit for selected contract

# Sort profit according to total variation
profit_array_sort = profit_array[tv_to_disp_array.argsort()]
num_filter = int(len(profit_array)/divisor)
profit_array_filter_avg = sum(profit_array_sort[-num_filter:])/num_filter
print("Average profit after picking ", num_filter, "contract is ", profit_array_filter_avg)

# Compute the win rate 
win_rate = 0.0
win_rate = (profit_array >= 0).sum()/len(profit_array)
print("Win rate for all the contracts is ", win_rate)

win_rate_filter = 0.0
win_rate_filter = (profit_array_sort[-num_filter:] >= 0).sum()/num_filter
print("Average profit after picking ", num_filter, "contract is ", win_rate_filter)
print(profit_array)
print(tv_to_disp_array)



