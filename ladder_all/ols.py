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

# Read the stv_to_disp array
stv_to_disp = np.loadtxt("stv_to_disp_array_"+data_date_before+".txt")

# Compute the normalized profit array
profit_normalized = np.divide(profit_array, open_price_array)

# Plot normalized profit and stv_to_disp

# Plot the buy, sell information
for i in range(len(profit_array)):
	plt.scatter(stv_to_disp[i], profit_normalized[i], color="r")
	plt.xlabel("Total variation")
	plt.ylabel("Profit / openPrice")
plt.savefig("profit_normalized_to_indicator_"+data_date+".eps", format="eps")
plt.close()

# Plot the buy, sell information
for i in range(len(profit_array)):
	plt.scatter(stv_to_disp[i], profit_array[i], color="r")
	plt.xlabel("Total variation")
	plt.ylabel("Profit")
plt.savefig("profit_to_indicator_"+data_date+".eps", format="eps")
plt.close()
