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

	book = np.zeros(data_len) # Book series
		
	# Initialize state variables
	current_book = 0.0 # current marked-to-book value
	net_profit_lastPrice = 0.0 # net profit
	
	price_lastPrice = df.lastPrice.as_matrix()
	cum_profit = 0.0
	profit = 0.0
	
	for i in range(1,data_len):
		displacement = abs(price_lastPrice[i] - df.iloc[0]["openPrice"])
		cum_profit += abs( price_lastPrice[i] - price_lastPrice[i-1] )/2
		
		book[i] = cum_profit + loss_disp(minPriceChange, displacement)
	
	## Intialize the price array
	#price = np.zeros(2*data_len)
	#price[0] = df.iloc[0]["openPrice"]
	#price[1] = df.iloc[0]["lastPrice"]
	#print(price[0], price[1])
	#if price[1] >= price[0]:
		## Sell
		#previous = -price[1]
	#else:
		## Buy
		#previous = price[1] 
	
	#for i in range(1, data_len):
		
		## Record price using lastPrice
		#price[2*i] = df.iloc[i]["lastPrice"]
		#if df.iloc[i]["lastPrice"] > previous:
			#previous = -df.iloc[i]["lastPrice"]
		#elif df.iloc[i]["lastPrice"] < previous:
			#previous = df.iloc[i]["lastPrice"]
			
		## Record price using bid ask
		#if previous > 0:
			#if df.iloc[i]["askPrice1"] > abs(previous):
				#price[2*i+1] = df.iloc[i]["askPrice1"]
				#previous = -df.iloc[i]["askPrice1"]
			#else:
				#price[2*i+1] = df.iloc[i]["bidPrice1"]
				#previous = df.iloc[i]["bidPrice1"]
		#elif previous < 0:
			#if df.iloc[i]["bidPrice1"] < abs(previous):
				#price[2*i+1] = df.iloc[i]["bidPrice1"]
				#previous = df.iloc[i]["bidPrice1"]
			#else:
				#price[2*i+1] = df.iloc[i]["askPrice1"]
				#previous = -df.iloc[i]["askPrice1"]
			
		##print(price[2*i],price[2*i+1])
	
	displacement = abs( df.iloc[-1]["closePrice"] - df.iloc[-1]["openPrice"] )
	gain_lastPrice = gain_osci(price_lastPrice)
	loss_lastPrice = loss_disp(minPriceChange, displacement)
	net_profit_lastPrice = gain_lastPrice + loss_lastPrice
	
	print("Displacement is ", displacement)
	print("Gain using last price is ", gain_lastPrice)
	print("Loss using last price is ", loss_lastPrice)
	print("Net profit is ", net_profit_lastPrice)
	print("Final book value is ", book[-1])
	
	# Save data for analysis
	if debug == 1 or debug_contract == 1:
		np.savetxt("./data_"+data_date+"_debug/"+ticker_list[j]+"_book.txt", book)
		#np.savetxt("./data_"+data_date+"_debug/"+ticker_list[j]+"_profit_tick.txt", profit_tick)
		#np.savetxt("./data_"+data_date+"_debug/"+ticker_list[j]+"_book.txt", book)
		#np.savetxt("./data_"+data_date+"_debug/"+ticker_list[j]+"_profit_tick_ba.txt", profit_tick_ba)
		#np.savetxt("./data_"+data_date+"_debug/"+ticker_list[j]+"_position_stack_len.txt", position_stack_len)
		#np.savetxt("./data_"+data_date+"_debug/"+ticker_list[j]+"_profit_close.txt", profit_close)

	else:	
		np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_book.txt", book) 
		#np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_position_stack.txt", position_stack)
		#np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_profit_tick.txt", profit_tick)
		#np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_profit_tick_ba.txt", profit_tick_ba)
		#np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_position_stack_len.txt", position_stack_len)
		#np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_profit_close.txt", profit_close)
	#print("The cumulative tick profit is ", cum_profit)
	#print("Position stack is ", position_stack)
	#if debug == 1:			
		#print(df.tail(5)["dataTime"])

