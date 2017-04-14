import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant
from statsmodels.tsa.stattools import coint

# Read profit array
profit_array = np.loadtxt("profit_array_"+data_date+".txt")

# Read the open price array
open_price_array = np.loadtxt("open_price_array_"+data_date+".txt")

# Read the tv_to_disp array
tv_to_disp_array = np.loadtxt("tv_to_disp_array_"+data_date_before+".txt")

# Compute the normalized profit array
profit_normalized = np.divide(profit_array, open_price_array)

# Compute the log of total variation
log_tv_to_disp_array = np.log(tv_to_disp_array)

# Compute the log of profit
log_profit_array = np.log(profit_array)


# Plot normalized profit and stv_to_disp

# Plot
for i in range(len(profit_array)):
	plt.scatter(tv_to_disp_array[i], profit_normalized[i], color="r")
	plt.xlabel("Total variation (20170413)")
	plt.ylabel("Profit / openPrice (20170414)")
plt.savefig("profit_normalized_to_indicator_"+data_date+".eps", format="eps")
plt.close()

# Plot
for i in range(len(profit_array)):
	plt.scatter(tv_to_disp_array[i], profit_array[i], color="r")
	plt.xlabel("Total variation (20170413)")
	plt.ylabel("Profit (20170414)")
plt.savefig("profit_to_indicator_"+data_date+".eps", format="eps")
plt.close()

# Plot
for i in range(len(profit_array)):
	plt.scatter(log_tv_to_disp_array[i], profit_normalized[i], color="r")
	plt.xlabel("log Total variation (20170413)")
	plt.ylabel("Profit / openPrice (20170414)")
plt.savefig("profit_normalized_to_log_indicator_"+data_date+".eps", format="eps")
plt.close()

# Plot
for i in range(len(profit_array)):
	plt.scatter(log_tv_to_disp_array[i], log_profit_array[i], color="r")
	plt.xlabel("log Total variation (20170413)")
	plt.ylabel("log Profit (20170414)")
plt.savefig("log_profit_to_log_indicator_"+data_date+".eps", format="eps")
plt.close()
