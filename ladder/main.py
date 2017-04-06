import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *


# Read the data
df = pd.read_csv(ticker+".csv", encoding = "GBK")
#print(df.head(3))
#print(len(df))

# Delete the first two rows
df = df.iloc[2:]
#print(df.head(1))
#print(len(df))


if debug == 1:
	data_len = 5
else:
	data_len = len(df)
	
# Initialize bid and ask state
my_bid = 0.0
my_ask = 0.0
short_position = np.zeros(data_len, dtype="int")	
long_position = np.zeros(data_len, dtype="int")
short_price = np.zeros(data_len, dtype="int")
long_price = np.zeros(data_len, dtype="int")
position_stack = np.array([])
cum_profit = int(0) # cumulative profit
profit_tick = np.zeros(len(df)) # profit series for trading in certain ticks 
commission = np.zeros(len(df)) # commission for each trade
unit = int(5)  # ton/contract


for i in range(data_len):
	# For the first period, just set my bid and ask
	print("\nData time is ", df.iloc[i]["dataTime"])
	if i == 0:
		my_bid = df.iloc[i]["bidPrice1"] 
		my_ask = df.iloc[i]["askPrice1"] 
		print("My bid price at time", df.iloc[i]["dataTime"], " is ", my_bid)
		print("My ask price at time", df.iloc[i]["dataTime"], " is ", my_ask)
	else:
		my_bid = df.iloc[i-1]["bidPrice1"] 
		my_ask = df.iloc[i-1]["askPrice1"] 		
		print("My bid price at previous tick is ", my_bid)
		print("My ask price at previous tick is ", my_ask)
		print("Last price of the current tick is", df.iloc[i]["lastPrice"])
		print("Market bid price 1 at the current tick is ", df.iloc[i]["bidPrice1"])
		print("Market ask price 1 at the current tick is ", df.iloc[i]["askPrice1"])		
		
		if df.iloc[i]["bidPrice1"]  > my_ask or \
		 ( df.iloc[i]["lastPrice"] > my_ask and df.iloc[i]["volume"] != df.iloc[i-1]["volume"]):
			
			# Record short position
			short_position[i] = 1
			
			# Record the price of the position
			short_price[i] = my_ask
			print("Position short at", my_ask)

			# Update the position_stack
			if len(position_stack) == 0:
				position_stack = np.hstack((position_stack, -my_ask))
				
				
			# If previously long
			elif position_stack[-1] > 0:
				# Calculate the profit
				profit_tick[i] = my_ask - position_stack[-1]
				cum_profit += ( my_ask - position_stack[-1] )
				# Pop back
				position_stack = np.delete(position_stack,-1)
				
			# If previously short
			elif position_stack[-1] < 0:
				# Append 
				position_stack = np.hstack((position_stack, -my_ask))
				print("Append short position: ", -my_ask)
						
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
				
			# If previously short
			elif position_stack[-1] < 0:
				# Calculate the profit
				profit_tick[i] = -my_bid - position_stack[-1]
				cum_profit += ( -my_bid - position_stack[-1] )
				# Pop back
				position_stack = np.delete(position_stack,-1)
				
			# If previously long
			elif position_stack[-1] > 0:
				# Append 
				position_stack = np.hstack((position_stack, my_bid))
				print("Append long position: ", my_bid)
			
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


	
print("The cumulative profit is ", cum_profit)
print("Position stack is ", position_stack)
if debug == 1:			
	print(df.tail(5)["dataTime"])

