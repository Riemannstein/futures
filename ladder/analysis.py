import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *


# Load additional data
position_stack = np.loadtxt("./data/position_stack.txt", ndmin = 1)
profit_tick = np.loadtxt("./data/profit_tick.txt")
book = np.loadtxt("./data/book.txt")
long_position = np.loadtxt("./data/long_position.txt")
short_position = np.loadtxt("./data/short_position.txt")
position_stack_len = np.loadtxt("./data/position_stack_len.txt")
cum_profit = sum(profit_tick) # cumulative profit from ticks
profit_before = np.zeros(len(df))

# Add columns to dataframe
df["book"] = pd.Series(book, index=df.index)
df["position_stack_len"] = pd.Series(position_stack_len, index=df.index)

# Compute the cumulative profit series for each tick
for i in range(len(profit_tick)):
	if i == 0:
		profit_before[i] = profit_tick[i]
	else:
		profit_before[i] = profit_before[i-1] + profit_tick[i]
		
# Get the spread series
spread1 = df.askPrice1 - df.bidPrice1

for e in spread1:
	if e == 15:
		print(e)
print(type(position_stack))
print(position_stack)
print(len(np.array([1,2,3])))
print(type(np.array([1,2,3])))
print(len(position_stack))
close_profit = np.zeros(position_stack.size)

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
print("The end book series is ", book[-1])
print("Number of naked positions is ", len(position_stack))

# Plot the price series
plt.xlabel("Tick")
plt.ylabel("Lase price")
plt.plot(df.lastPrice[0:data_len])
plt.plot(df.askPrice1[0:data_len])
plt.plot(df.bidPrice1[0:data_len])
plt.savefig("./plot/lastPrice.eps", format="eps")
plt.close()

# Plot the net profit series before closing positions
plt.xlabel("Tick")
plt.ylabel("Net proftit before closing positions")
plt.plot(profit_before[0:data_len], linewidth = 0.3)
plt.savefig("./plot/profit_before.eps", format="eps")
plt.close()

# Plot the net profit series after closing positions
plt.xlabel("Tick")
plt.ylabel("Net profit after closing positions")
plt.plot(profit_after[0:data_len], linewidth = 0.3)
plt.savefig("./plot/profit_after.eps", format="eps")
plt.close()

# Plot the net profit series before closing positions
plt.xlabel("Tick")
plt.ylabel("Book series")
plt.plot(book[0:data_len], linewidth = 0.3)
plt.savefig("./plot/book.eps", format="eps")
plt.close()

# Plot the net profit series after closing positions
plt.xlabel("Tick")
plt.ylabel("Bid ask spread")
plt.plot(spread1[0:data_len], linewidth = 0.3)
plt.savefig("./plot/spread1.eps", format="eps")
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
plt.savefig("./plot/price_book.eps", format="eps")
plt.close()


# Plot book and last price for a certain priod
plt.subplot(2,1,1)
df.lastPrice[plot_start:plot_end].plot(secondary_y=True, legend=True, label = "Last price")
df.book[plot_start:plot_end].plot(legend=True, label = "Book value")

plt.subplot(2,1,2)
plt.plot(position_stack_len[plot_start:plot_end])
plt.xlim(0,plot_end-plot_start)
plt.savefig("./plot/price_book_local.eps", format="eps")
plt.close()

#lastPrice = df.lastPrice.as_matrix()
#print(lastPrice[0:10])
#print(type(df.lastPrice.as_matrix()))
#print(type(df.iloc[:]["lastPrice"]))
#print(type(df.iloc[:].lastPrice))
