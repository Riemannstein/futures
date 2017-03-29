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



n = 60 # number of periods for regression

# delivery date of the contracts we want to focus
ticker_date = "1704"

# Pick rb and hc contracts 
rb = pd.read_csv("rb1704.csv", encoding='GBK')
hc = pd.read_csv("hc1704.csv", encoding='GBK')
print(rb.columns)

start = rb.iloc[0]['tradeDate'] # Start date
end = rb.iloc[-1]['tradeDate'] # end date
tt = rb.iloc[n]['tradeDate'] # Begin date of trade
sigma = 1e-2             # Threshold level
print(start, end, (end > tt) & (tt > start))

# Store the position of the two contracts
rb_position = int(0) # number of contract for rb, positive for long and negative for short
hc_position = int(0) # number of contract for hc, positive for long and negative for short
state = int(0) # Current state of position
profit = int(0) # accumulated profit

# Get ols estimate for analysis period
ols = OLS(rb.settlePrice, add_constant(hc.settlePrice)).fit().params
mean  = ols[0]
slope = ols[1]
print(ols)
print(mean, slope)

# Subset the data used for trading
rb_t = rb.iloc[n:-1,]
hc_t = hc.iloc[n:-1,]

# Test rounding function
#print(round(0.4582,2))
#print(rb_t.tradeDate)

rbhc_t = pd.merge(rb_t,hc_t,on='tradeDate')
print(rbhc_t.head(3))

# Define the threshold 
def upper(m):
	return m+1

def lower(m):
	return m-1
	

# Buy low, sell high
for index, row in rbhc_t.iterrows():
	print(row["tradeDate"], )
	if row["openPrice_x"] -slope*row["openPrice_y"] <= lower(mean) and \
	 rb_position == 0 and hc_position == 0:
		rb_position = 1000 
		hc_position = -int(slope*1000)
		state = rb_position*row["openPrice_x"] + hc_position*row["openPrice_y"]
		print(hc_position)
	if rb_position != 0 or hc_position != 0:
		if row["openPrice_x"] -slope*row["openPrice_y"] >= upper(mean):
			rb_position = 0
			hc_position = 0
			profit = profit + \
			 rb_position*row["openPrice_x"] + hc_position*row["openPrice_y"] - \
			 state
			state = 0
			print(profit)
print("Final profit is ", profit)
			
			 
		
		  
		




