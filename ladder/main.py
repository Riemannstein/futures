import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *



	
# Initialize bid and ask state
my_bid = 0.0
my_ask = 0.0
short_position = np.zeros(data_len, dtype="int")
long_position = np.zeros(data_len, dtype="int")
short_price = np.zeros(data_len, dtype="int")
long_price = np.zeros(data_len, dtype="int")
position_stack = np.array([])
book = np.zeros(len(df))
cum_profit = int(0) # cumulative profit
profit_tick = np.zeros(len(df)) # profit series for trading in certain ticks 
commission = np.zeros(len(df)) # commission for each trade
unit = int(5)  # ton/contract
profit = int(0) # Record single trade profit
book_stack = int(0) # Record the book value on the positions held
position_stack_len = np.zeros(len(df), dtype="int") # Signed length of position_stack


# Get the spread series
spread1 = df.iloc[0:]["askPrice1"].as_matrix() - df.iloc[0:]["bidPrice1"].as_matrix()
print("My spread is ", my_spread)


for i in range(data_len):
	# For the first period, just set my bid and ask
	print("\nTick number ",i)
	print("Data time is ", df.iloc[i]["dataTime"])
	
	if i == 0:
		# Initialize the book value of the first tick
		book[i] = 0 
 		
		# Place limited orders
		my_bid = df.iloc[i]["bidPrice1"] 
		my_ask = df.iloc[i]["askPrice1"] 
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
		
		if df.iloc[i]["askPrice1"]  > my_ask or \
		 ( df.iloc[i]["lastPrice"] > my_ask and df.iloc[i]["volume"] != df.iloc[i-1]["volume"]):
			
			# Record short position
			short_position[i] = 1
			
			# Record the price of the position
			short_price[i] = my_ask
			print("Position short at", my_ask)

			# Update the position_stack
			if len(position_stack) == 0:
				position_stack = np.hstack((position_stack, -my_ask))
				
				## Reset Limited order (a)
				#my_bid = df.iloc[i]["bidPrice1"] 
				#my_ask = df.iloc[i]["askPrice1"] 				
				
			# If previously long
			elif position_stack[-1] > 0:
				# Calculate the profit
				profit_tick[i] = my_ask - position_stack[-1]
				profit = my_ask - position_stack[-1]
				cum_profit += profit
				print("Single profit is ", profit)
				
				## Reset limited order (a)
				#my_bid = df.iloc[i]["bidPrice1"]
				#my_ask = my_bid + my_spread
				
				# Pop back
				position_stack = np.delete(position_stack,-1)
				
			# If previously short
			elif position_stack[-1] < 0:
				# Append 
				position_stack = np.hstack((position_stack, -my_ask))
				print("Append short position: ", -my_ask)
				
				## Reset limited order (a)
				#my_ask = df.iloc[i]["askPrice1"]
				#my_bid = my_ask - my_spread			

						
		elif df.iloc[i]["bidPrice1"] < my_bid or \
		 (df.iloc[i]["lastPrice"] < my_bid and df.iloc[i]["volume"] != df.iloc[i-1]["volume"]):
			
			# Record long position
			long_position[i] = 1
			
			# Record the price of the position
			long_price[i] = my_bid
			print("Long position at ", my_bid)

			# Update the position_stack
			if len(position_stack) == 0:
				position_stack = np.hstack((position_stack, my_bid))
				
				## Reset limited order (a)
				#my_bid = df.iloc[i]["bidPrice1"] 
				#my_ask = df.iloc[i]["askPrice1"] 
				
			# If previously short
			elif position_stack[-1] < 0:
				# Calculate the profit
				profit_tick[i] = -my_bid - position_stack[-1]
				profit = -my_bid - position_stack[-1]
				print("Single profit is ", profit)
				cum_profit += profit
				
				## Reset limited order (a)
				#my_bid = df.iloc[i]["bidPrice1"]
				#my_ask = my_bid + my_spread
				
				# Pop back
				position_stack = np.delete(position_stack,-1)
				
			# If previously long
			elif position_stack[-1] > 0:
				# Append 
				position_stack = np.hstack((position_stack, my_bid))
				print("Append long position: ", my_bid)
				
				## Reset limited order (a)
				#my_ask = df.iloc[i]["askPrice1"]
				#my_bid = my_ask - my_spread	
				
		## Place limited orders (b)
		#if len(position_stack) == 0: 
			#my_bid = df.iloc[i]["bidPrice1"] 
			#my_ask = df.iloc[i]["askPrice1"] 
		#elif position_stack[-1] > 0:
			#my_bid = df.iloc[i]["bidPrice1"]
			#my_ask = my_bid + my_spread
		#elif position_stack[-1] < 0:
			#my_ask = df.iloc[i]["askPrice1"]
			#my_bid = my_ask - my_spread
		
		## Place limited orders (c)
		#if spread1[i] <= 5:		
			#my_bid = df.iloc[i]["bidPrice1"] - k*minPriceChange
			#my_ask = df.iloc[i]["askPrice1"] + k*minPriceChange
		#else:
			#my_bid = df.iloc[i]["bidPrice1"]
			#my_ask = df.iloc[i]["askPrice1"] 
			
		# Place limited orders (c)
		my_bid = df.iloc[i]["bidPrice1"]
		my_ask = df.iloc[i]["askPrice1"] 		
		


				
		# Update the book series
		# If not holding any position
		if len(position_stack) == 0:
			book[i] = cum_profit
		# If the position has changed
		else:
			if position_stack[-1] > 0:
				book_stack = sum(df.iloc[i]["lastPrice"] - position_stack)
				book[i] = book_stack + cum_profit
			elif position_stack[-1] < 0:
				book_stack = sum( - df.iloc[i]["lastPrice"] - position_stack)
				book[i] = book_stack + cum_profit			
		
		
		if len(position_stack) == 0:
			print("Not holding any position at the end of tick ", i)
		else:
			print("Position(s) held at the end of tick ", i, "is ", position_stack)
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
			

if debug == 1:		
	print("Short position list: ", short_position)
	print("Short price list: ", short_price)
	print("Long position list: ", long_position)
	print("Long price list: ", long_price)
	for e in position_stack:
		print(e)

# Save data for analysis
np.savetxt("./data/position_stack.txt", position_stack)
np.savetxt("./data/profit_tick.txt", profit_tick)
np.savetxt("./data/book.txt", book)
np.savetxt("./data/short_position.txt", short_position)
np.savetxt("./data/long_position.txt", long_position)
np.savetxt("./data/position_stack_len.txt", position_stack_len)

	
print("The cumulative tick profit is ", cum_profit)
print("Position stack is ", position_stack)
if debug == 1:			
	print(df.tail(5)["dataTime"])

