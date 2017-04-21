import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import os
from param import *

if debug == 1 or debug_contract == 1:
	plot_dir = "./plot_"+data_date+"_debug/"
	data_dir = "./data_debug"
	data_read_dir = "./data_"+data_date+"_debug/"
else:
	plot_dir = "./plot_"+data_date+"/"
	data_dir = "./data"
	data_read_dir = "./data_"+data_date+"/"


if not os.path.exists(plot_dir):
	os.makedirs(plot_dir)
	
if not os.path.exists(data_dir):
	os.makedirs(data_dir)
	

profit_array = np.zeros(len(ticker_list)) # profit array
open_price_array = np.zeros(len(ticker_list)) # open price array

# Iterate over all contracts
for j in range(len(ticker_list)):
	
	# Read the data
	df = pd.read_csv("../data/tick_"+data_date+"/"+ticker_list[j]+"_"+data_date+".csv", encoding = "GBK")
	contract = pd.read_csv("../data/contract_20170413/"+ticker_list[j]+".csv", encoding = "GBK")

	
	# Get the index of the first tick
	for i in range(len(df)):
		if df.iloc[i]["lowPrice"] != 0:
			start_index = i
			break
	print("The starting tick has index ", start_index)
	
	# Delete the useless two rows
	df = df.iloc[start_index:]

	# Setting data length according to debugging mode
	if debug == 1:
		data_len = 20
	else:
		data_len = len(df)
		
	# Load results data
	position_stack = np.loadtxt(data_read_dir+ticker_list[j]+"_position_stack.txt", ndmin = 1)
	profit_tick = np.loadtxt(data_read_dir+ticker_list[j]+"_profit_tick.txt")
	book = np.loadtxt(data_read_dir+ticker_list[j]+"_book.txt")
	position_stack_len = np.loadtxt(data_read_dir+ticker_list[j]+"_position_stack_len.txt")
	profit_tick_ba = np.loadtxt(data_read_dir+ticker_list[j]+"_profit_tick_ba.txt")
	profit_close = np.loadtxt(data_read_dir+ticker_list[j]+"_profit_close.txt", ndmin = 1)
	# cumulative profit from ticks(last price and bid/ask), and closing position 	
	cum_profit = sum(profit_tick) + sum(profit_tick_ba) + sum(profit_close)
	profit_before = np.zeros(len(df))
	print((profit_close > 0))
	# Add columns to dataframe
	df["book"] = pd.Series(book, index=df.index)
	df["position_stack_len"] = pd.Series(position_stack_len, index=df.index)

	# Compute the cumulative profit series for each tick
	for i in range(len(profit_tick)):
		if i == 0:
			profit_before[i] = profit_tick[i] + profit_tick_ba[i]
		else:
			profit_before[i] = profit_before[i-1] + profit_tick[i] + profit_tick_ba[i]
			
	# Get the spread series
	spread1 = df.askPrice1 - df.bidPrice1
	print(type(spread1))

	for e in spread1:
		if e == 15:
			print(e)
	print(type(position_stack))
	print(position_stack)
	print(len(np.array([1,2,3])))
	print(type(np.array([1,2,3])))
	print(len(position_stack))


	# Compute the net profit series after closing all positions
	profit_after = np.zeros(len(profit_before))
	profit_after[0:] = profit_before[0:]
	profit_after[-1] = cum_profit 
	
	# Save the cumulative profit for each contract
	profit_array[j] = cum_profit
	
	# Save the open price array for each contract
	open_price_array[j] = df.iloc[0]["openPrice"]

	print("The profit from closing positions is ", sum(profit_close))
	print("The profit from ticks is ", sum(profit_tick) + sum(profit_tick_ba))
	print("The total profit is ", sum(profit_tick) + sum(profit_tick_ba) + sum(profit_close))
	print("The cumulative profit is ", cum_profit)
	print("The end book series is ", book[-1])
	print("Number of naked positions is ", len(position_stack))
	print("Profit array of tick ", j, "is ", profit_array[j])
	
	
	
	# Plot the price series
	plt.xlabel("Tick")
	plt.ylabel("Lase price")
	plt.plot(df.lastPrice[0:data_len])
	plt.plot(df.askPrice1[0:data_len])
	plt.plot(df.bidPrice1[0:data_len])
	plt.savefig(plot_dir+ticker_list[j]+"_lastPrice.eps", format="eps")
	plt.close()

	# Plot the net profit series before closing positions
	plt.xlabel("Tick")
	plt.ylabel("Net proftit before closing positions")
	plt.plot(profit_before[0:data_len], linewidth = 0.3)
	plt.savefig(plot_dir+ticker_list[j]+"_profit_before.eps", format="eps")
	plt.close()

	# Plot the net profit series after closing positions
	plt.xlabel("Tick")
	plt.ylabel("Net profit after closing positions")
	plt.plot(profit_after[0:data_len], linewidth = 0.3)
	plt.savefig(plot_dir+ticker_list[j]+"_profit_after.eps", format="eps")
	plt.close()

	# Plot the net profit series before closing positions
	plt.xlabel("Tick")
	plt.ylabel("Book series")
	plt.plot(book[0:data_len], linewidth = 0.3)
	plt.savefig(plot_dir+ticker_list[j]+"_book.eps", format="eps")
	plt.close()

	# Plot the net profit series after closing positions
	plt.xlabel("Tick")
	plt.ylabel("Bid ask spread")
	plt.plot(spread1[0:data_len], linewidth = 0.3)
	plt.savefig(plot_dir+ticker_list[j]+"_spread1.eps", format="eps")
	plt.close()

	## Plot price and book series together
	#plt.subplot(2,1,1)
	#plt.plot(df.lastPrice,linewidth=0.1)
	#plt.ylabel("Last price")
	#plt.subplot(2,1,2)
	#plt.plot(book, linewidth=0.1)
	#plt.ylabel("Book value")
	#plt.savefig("./plot/price_book.eps", format="eps")
	#plt.close()

	# Plot book and last price
	plt.subplot(2,1,1)
	df.lastPrice[0:data_len].plot(secondary_y=True, legend=True, label = "Last price")
	df.book[0:data_len].plot(legend=True, label = "Book value")
	plt.subplot(2,1,2)
	plt.plot(position_stack_len)
	plt.savefig(plot_dir+ticker_list[j]+"_price_book.eps", format="eps")
	plt.close()


	# Plot book and last price for a certain priod
	plt.subplot(2,1,1)
	df.lastPrice[plot_start:plot_end].plot(secondary_y=True, legend=True, label = "Last price")
	df.book[plot_start:plot_end].plot(legend=True, label = "Book value")

	plt.subplot(2,1,2)
	plt.plot(position_stack_len[plot_start:plot_end])
	plt.xlim(0,plot_end-plot_start)
	plt.savefig(plot_dir+ticker_list[j]+"_price_book_local.eps", format="eps")
	plt.close()

	#lastPrice = df.lastPrice.as_matrix()
	#print(lastPrice[0:10])
	#print(type(df.lastPrice.as_matrix()))
	#print(type(df.iloc[:]["lastPrice"]))
	#print(type(df.iloc[:].lastPrice))

	#print(df.iloc[-1]["closePrice"])
	#print(df.iloc[-1]["openPrice"])
	
np.savetxt(data_dir+"/profit_array_"+data_date+".txt", profit_array)
np.savetxt(data_dir+"/open_price_array_"+data_date+".txt", open_price_array)
