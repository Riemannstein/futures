import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *


# Iterate over all the contracts
for j in range(len(ticker_list)):
	
	# Read the data
	df = pd.read_csv("../data/tick_"+data_date+"/"+ticker_list[j]+"_"+data_date+".csv", encoding = "GBK")
	contract = pd.read_csv("../data/contract_20170413/"+ticker_list[j]+".csv", encoding = "GBK")
	start_index = 0 # get the start index of the dataframe

	# Get the index of the first tick
	for i in range(len(df)):
		if df.iloc[i]["lowPrice"] != 0:
			start_index = i
			break
	print("The starting tick has index ", start_index)
	
	# Delete the first two rows
	df = df.iloc[start_index:]
	
	# Setting data length according to debugging mode
	if debug == 1:
		data_len = 20
	else:
		data_len = len(df)
		
	# Initialize bid and ask state
	my_bid = 0.0
	my_ask = 0.0
	position_stack = np.array([])
	book = np.zeros(len(df))
	cum_profit = int(0) # cumulative profit
	profit_tick = np.zeros(len(df)) # profit series for trading in certain ticks 
	profit_tick_ba = np.zeros(len(df)) # profit series for bid ask trade
	commission = np.zeros(len(df)) # commission for each trade
	unit = int(5)  # ton/contract
	profit = int(0) # Record single trade profit
	book_stack = int(0) # Record the book value on the positions held
	position_stack_len = np.zeros(len(df), dtype="int") # Signed length of position_stack

	# Get the minimum price change
	minPriceChange = contract.iloc[0]["minChgPriceNum"]
	
	# Set my_spread (a crucial parameter)
	my_spread =  float(k*minPriceChange)
	
	for i in range(data_len):
		
		# For the first period, just set my bid and ask
		print("\nTick number ",i)
		print("Data time is ", df.iloc[i]["dataTime"])
		
		if i == 0:
			# Initialize the book value of the first tick
			book[i] = 0 
			
			# Place limited orders
			my_bid = df.iloc[i]["bidPrice1"] 
			my_ask = my_bid + my_spread
			print("My bid price at time", df.iloc[i]["dataTime"], " is ", my_bid)
			print("My ask price at time", df.iloc[i]["dataTime"], " is ", my_ask)
			print("Market bid price 1 at the current tick is ", df.iloc[i]["bidPrice1"])
			print("Market ask price 1 at the current tick is ", df.iloc[i]["askPrice1"])	
			
		else:	
											
			print("My bid price at previous tick is ", my_bid)
			print("My ask price at previous tick is ", my_ask)
			print("Market bid price 1 at the current tick is ", df.iloc[i]["bidPrice1"])
			print("Market ask price 1 at the current tick is ", df.iloc[i]["askPrice1"])	
			print("Last price of the current tick is", df.iloc[i]["lastPrice"])	
			
			# Trade conditions
			if df.iloc[i]["lastPrice"] >= my_ask:
				
				print("lastPrice >=  my_ask")
				print("Short at ", my_ask)

				# Update the position_stack
				if len(position_stack) == 0:
					print("Not holding any position previously, append ", -my_ask)
					position_stack = np.hstack((position_stack, -my_ask))
							
					# Place limited order
					my_ask = df.iloc[i]["lastPrice"] + my_spread/2
					my_bid = df.iloc[i]["lastPrice"] + my_spread/2
					
				# If previously long
				elif position_stack[-1] > 0:
					print("Most recent trade is ", position_stack[-1])
					# Calculate the profit
					profit_tick[i] = my_ask - position_stack[-1]
					profit = my_ask - position_stack[-1]
					cum_profit += profit
					print("Single profit is ", profit)
					
					# Pop back
					position_stack = np.delete(position_stack,-1)
					
				# If previously short
				elif position_stack[-1] < 0:
					print("Most recent trade is ", position_stack[-1])
					# Append 
					position_stack = np.hstack((position_stack, -my_ask))
					print("Append short position: ", -my_ask)	
					
				# Place limited order	
				if len(position_stack) == 0:
					my_ask = df.iloc[i]["lastPrice"] + my_spread/2
					my_bid = df.iloc[i]["lastPrice"] - my_spread/2
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)
					
				# If previously long
				elif position_stack[-1] > 0:
					my_ask = position_stack[-1] + my_spread/2
					my_bid = position_stack[-1] - my_spread/2
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)				
					
					
				# If previously short
				elif position_stack[-1] < 0:
					my_bid = -position_stack[-1] - my_spread/2
					my_ask = -position_stack[-1] + my_spread/2
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)	
			
			# Trade condition 
			elif df.iloc[i]["lastPrice"] <= my_bid:
				
				print("lastPrice <=  my_ask")
				print("Long at ", my_bid)
				
				# Update the position_stack
				if len(position_stack) == 0:
					print("Not holding any position previously, append", my_bid)
					position_stack = np.hstack((position_stack, my_bid))
					
					# Place limited order
					
					
				# If previously short
				elif position_stack[-1] < 0:
					print("Most recent trade is ", position_stack[-1])
					# Calculate the profit
					profit_tick[i] = -my_bid - position_stack[-1]
					profit = -my_bid - position_stack[-1]
					print("Single profit is ", profit)
					cum_profit += profit
					
					# Pop back
					position_stack = np.delete(position_stack,-1)
					
				# If previously long
				elif position_stack[-1] > 0:
					print("Most recent trade is ", position_stack[-1])
					# Append 
					position_stack = np.hstack((position_stack, my_bid))
					print("Append long position: ", my_bid)
					
				# Place limited order	
				if len(position_stack) == 0:
					my_ask = df.iloc[i]["lastPrice"] + my_spread/2
					my_bid = df.iloc[i]["lastPrice"] - my_spread/2
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)
					
				# If previously long
				elif position_stack[-1] > 0:
					my_ask = position_stack[-1] + my_spread/2
					my_bid = position_stack[-1] - my_spread/2
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)				
					
					
				# If previously short
				elif position_stack[-1] < 0:
					my_bid = -position_stack[-1] - my_spread/2
					my_ask = -position_stack[-1] + my_spread/2 
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)

					
			if df.iloc[i]["askPrice1"]  > my_ask:
				
				print("\naskPrice1 > my_ask")
				print("Short at, ", my_ask)
				# Update the position_stack
				if len(position_stack) == 0:
					print("Not holding any position previously, append ", -my_ask)
					position_stack = np.hstack((position_stack, -my_ask))		

				# If previously short
				elif position_stack[-1] < 0:
					print("Most recent trade is ", position_stack[-1])
					# Append 
					position_stack = np.hstack((position_stack, -my_ask))
					print("Append short position: ", -my_ask)
					
				# If previously long
				elif position_stack[-1] > 0:
					print("Most recent trade is ", position_stack[-1])
					
					# Calculate the profit
					profit_tick_ba[i] = my_ask - position_stack[-1]
					profit = my_ask - position_stack[-1]
					cum_profit += profit
					print("Single profit is ", profit)
					
					# Pop back
					position_stack = np.delete(position_stack,-1)

				# Place limited order	
				if len(position_stack) == 0:
					my_ask = df.iloc[i]["lastPrice"] + my_spread/2
					my_bid = df.iloc[i]["lastPrice"] - my_spread/2
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)
					
				# If previously long
				elif position_stack[-1] > 0:
					my_ask = position_stack[-1] + my_spread/2
					my_bid = position_stack[-1] - my_spread/2
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)				
					
					
				# If previously short
				elif position_stack[-1] < 0:
					my_bid = -position_stack[-1] - my_spread/2
					my_ask = -position_stack[-1] + my_spread/2 
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)
			
			elif df.iloc[i]["bidPrice1"] < my_bid:
				print("\nbidPrice1 < my_bid")			
				print("Long at ", my_bid)

				# Update the position_stack
				if len(position_stack) == 0:
					print("Not holding any position previously, append ", my_bid)
					position_stack = np.hstack((position_stack, my_bid))
					
				# If previously short
				elif position_stack[-1] < 0:
					print("Most recent trade is ", position_stack[-1])
					# Calculate the profit
					profit_tick_ba[i] = -my_bid - position_stack[-1]
					profit = -my_bid - position_stack[-1]
					print("Single profit is ", profit)
					cum_profit += profit
					
					# Pop back
					position_stack = np.delete(position_stack,-1)
					
				# If previously long
				elif position_stack[-1] > 0:
					print("Most recent trade is ", position_stack[-1])
					# Append 
					position_stack = np.hstack((position_stack, my_bid))
					print("Append long position: ", my_bid)
						
				# Place limited order	
				if len(position_stack) == 0:
					my_ask = df.iloc[i]["lastPrice"] + my_spread/2
					my_bid = df.iloc[i]["lastPrice"] - my_spread/2
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)
					
				# If previously long
				elif position_stack[-1] > 0:
					my_ask = position_stack[-1] + my_spread
					my_bid = position_stack[-1] - my_spread/2 
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)				
					
					
				# If previously short
				elif position_stack[-1] < 0:
					my_bid = -position_stack[-1] - my_spread/2
					my_ask = -position_stack[-1] + my_spread/2
					print("My updated ask price is ", my_ask)
					print("My updated bid price is ", my_bid)
							
			# Update the book series
			# If not holding any position
			if len(position_stack) == 0:
				book[i] = cum_profit
			# If holding position(s)
			else:
				if position_stack[-1] > 0:
					book_stack = sum(df.iloc[i]["lastPrice"] - position_stack)
					book[i] = book_stack + cum_profit
				elif position_stack[-1] < 0:
					book_stack = sum( - df.iloc[i]["lastPrice"] - position_stack)
					book[i] = book_stack + cum_profit			
			
			
			if len(position_stack) == 0:
				print("\nNot holding any position at the end of tick ", i)
			else:
				print("\nPosition(s) held at the end of tick ", i, "is ", position_stack)
			print("Book value at the end of tick ", i, "is", book[i])
			
			# Print the cumulative tick profit
			print("Cumulative tick profit is ", cum_profit)
			
			# Compute the signed length of the position_stack
			if len(position_stack) == 0:
				position_stack_len[i] = 0
			elif position_stack[-1] > 0:
				position_stack_len[i] = len(position_stack)
			elif position_stack[-1] < 0:
				position_stack_len[i] = -len(position_stack)
				
		if debug == 1:
			print("Position stack is ", position_stack)
			
	# Save data for analysis
	np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_position_stack.txt", position_stack)
	np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_profit_tick.txt", profit_tick)
	np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_book.txt", book)
	np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_profit_tick_ba.txt", profit_tick_ba)
	np.savetxt("./data_"+data_date+"/"+ticker_list[j]+"_position_stack_len.txt", position_stack_len)

		
	print("The cumulative tick profit is ", cum_profit)
	print("Position stack is ", position_stack)
	if debug == 1:			
		print(df.tail(5)["dataTime"])

