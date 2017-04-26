import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# debug mode for data length for each contract: 1
debug = 0

# debug mode for contract number
debug_contract = 1

# data length for debug mode
data_len_debug = 10

# Threshold for pvalue of adf test
p_threshold = 0.05

# ticker lists
ticker_list_shfe = ["ag1706", "al1706", "au1706", "bu1706", "cu1706",  "hc1710", "ni1709", "pb1705", "rb1710", "ru1709", "sn1705", "zn1706"]
ticker_list_xdce = ["a1709", "c1709", "cs1709", "i1709", "j1709", "jd1709", "jm1709", "l1709", "m1709", "p1709", "pp1709", "v1709", "y1709"]
ticker_list_xzce = ["CF709", "FG709", "MA709","OI709", "RM709", "SF705", "SM705", "SR709", "TA709", "WH705", "ZC705"]
ticker_list_ccfx = ["IF1705", "IC1705", "IH1705", "TF1706", "T1706"]

# data date and previous date and previous date
data_date = "20170419"
data_date_before = "20170418"

# Number of ticks used for ADF test
num_adf = int(20)

if debug_contract == 1:
	ticker_list = ["ag1706"]
else:
	ticker_list = ticker_list_shfe + ticker_list_xdce + ticker_list_xzce + ticker_list_ccfx


plot_start =0
plot_end = 500

divisor = 4 # Use the divisor to filter the contract

k = int(2) # times of minimum price change

## Get the spread series
#spread1 = df.iloc[0:]["askPrice1"].as_matrix() - df.iloc[0:]["bidPrice1"].as_matrix()
#print("My spread is ", my_spread)
