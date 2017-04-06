import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *

# Load the data
df = pd.read_csv(ticker+".csv", encoding = "GBK")
# Delete the first two rows
df = df.iloc[2:]

position_stack = np.loadtxt("./data/position_stack.txt")
profit_tick = np.loadtxt("./data/profit_tick.txt")
cum_profit = sum(profit_tick) # cumulative profit from ticks
profit_before = np.zeros(len(df))

for i in range(len(profit_tick)):
	if i == 0:
		profit_before[i] = profit_tick[i]
	else:
		profit_before[i] = profit_before[i-1] + profit_tick[i]



if debug == 1:
	data_len = 5
else:
	data_len = len(df)
	
close_profit = np.zeros(data_len)

# Calculate the profit for closing positions at the end of the day
for i in range(len(position_stack)):
	if position_stack[i] > 0:
		cum_profit += df.iloc[-1]["lastPrice"] - position_stack[i]
		close_profit[i] = df.iloc[-1]["lastPrice"] - position_stack[i]
	elif position_stack[i] < 0:
		cum_profit += -position_stack[i] - df.iloc[-1]["lastPrice"]	
		close_profit[i] = -position_stack[i] - df.iloc[-1]["lastPrice"]

# Compute the net profit series after closing all positions
profit_after = np.zeros(len(profit_before))
profit_after[0:] = profit_before[0:]
profit_after[-1] = cum_profit 

print("The profit from closing positions is ", sum(close_profit))
print("The profit from ticks is ", sum(profit_tick))
print("The cumulative profit is ", sum(profit_tick) + sum(close_profit))
print("Number of naked positions is ", len(position_stack))

# Plot the price series
plt.xlabel("Tick")
plt.ylabel("Lase price")
plt.plot(df.lastPrice)
plt.savefig("./plot/lastPrice.eps", format="eps")
plt.close()

# Plot the net profit series before closing positions
plt.xlabel("Tick")
plt.ylabel("Net proftit before closing positions")
plt.plot(profit_before)
plt.savefig("./plot/profit_before.eps", format="eps")
plt.close()

# Plot the net profit series after closing positions
plt.xlabel("Tick")
plt.ylabel("Net profit after closing positions")
plt.plot(profit_after)
plt.savefig("./plot/profit_after.eps", format="eps")
plt.close()

print(position_stack)

