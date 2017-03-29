from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant
from statsmodels.tsa.stattools import coint
#from matplotlib.pyplot import plot, show, savefig, close
import matplotlib.pyplot as plt
import os
import threading
import pandas as pd
import numpy as np
import seaborn as sns
import itertools


# 期货交易所,如:XZCE 郑州商品交易所, CCFX 中国金融期货交易所, XSGE 上海期货交易所, XDCE 大连期货交易所
exchangeCD = "XSGE"

# 各个交易所交易品种列表
XSGE_sec = ["cu","al","zn","pb","ni","sn","au","ag","rb","wr","hc","fu","bu","ru"]

# delivery date of the contracts we want to focus
ticker_date = "1704"

# Test plotting the cointegration series
first = pd.read_csv("cu"+ticker_date+".csv",encoding="GBK")
second = pd.read_csv("al"+ticker_date+".csv",encoding="GBK")
print(first.settlePrice)
print(len(first.index))
plt.xlabel("Period")
plt.ylabel("Settle Price")
plt.plot(second.index, first.settlePrice, label="cu")
plt.plot(second.index, second.settlePrice, label="al")
plt.legend(loc="upper left")
plt.savefig("./cual")
print(coint(first.settlePrice, second.settlePrice, regression="c"))
print(OLS(second.settlePrice, add_constant(first.settlePrice)).fit().params)


# Iterate over all possible combination of sector
for subset in itertools.combinations(XSGE_sec, 2):
	
  # Store the two series
  first = pd.read_csv(subset[0]+ticker_date+".csv",encoding="GBK")
  second = pd.read_csv(subset[1]+ticker_date+".csv",encoding="GBK")
  
  # If the length of two series are the same, we make the plot
  if len(first.index) == len(second.index):
	  plt.xlabel("Period (Day)")
	  plt.ylabel("Settle Price")
	  plt.plot(second.index, first.settlePrice, label=subset[0]+ticker_date)
	  plt.plot(second.index, second.settlePrice, label=subset[1]+ticker_date)
	  plt.legend(loc="upper left")
	  plt.savefig("./"+subset[0]+subset[1])
	  plt.close()
	  print(subset[0],subset[1])
	  print(coint(first.settlePrice,second.settlePrice, regression="c"))
	  print(OLS(first.settlePrice, add_constant(second.settlePrice)).fit().params, "\n")
	  
	  
	  

