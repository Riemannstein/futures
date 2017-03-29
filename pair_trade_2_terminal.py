# coding: utf-8

# In[ ]:

from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import seaborn as sns

# contract_ratio determines the ratio of the two contracts
# Parameter: floating number
# Return value: A list contains two non-zero integer
def contract_ratio(r):
    int_list = [x+1 for x in range(10)]
    my_matrix = np.zeros((10,10), dtype=float)
    for pair in itertools.product(int_list, int_list):
        my_matrix[pair[0]-1][pair[1]-1] = float(pair[1])/float(pair[0])
    my_matrix = abs(my_matrix - r)
    #print my_matrix
    int_1 = np.unravel_index(my_matrix.argmin(), my_matrix.shape)[0] + 1
    int_2 = np.unravel_index(my_matrix.argmin(), my_matrix.shape)[1] + 1
    return [int_1, int_2]

def ma(list):
    "Compute the moving average of a list of non-zero length by using      arithematic mean"
    if len(list) == 0:
        print("Empty list, moving average not defined")
    else:
        return float(sum(list))/float(len(list))
        
def std_dev(my_list, sample = True ):
    "Compute the standard deviation, sample (True) or population(False)"
    if len(my_list) == 0:
        print("Empty list, standard deviation not defined")
    else:
        mean = float(sum(my_list))/float(len(my_list))
        #print "mean of the series is", mean
        sqr_dev_sum = sum([(my_list[x] - mean)**2 for x in range(len(my_list))])
        #print "sqr_dev_sum of the series is", sqr_dev_sum
        if sample == True:
            #print "Compute sample std_dev"
            return (float(sqr_dev_sum)/float(len(my_list)-1))**0.5
        elif sample == False:
            #print "Compute population std_dev"
            return (float(sqr_dev_sum)/float(len(my_list)))**0.5

# Define the stop-loss function
def stop_at_low(state, std_dev, sl_coeff):
    return state - sl_coeff*std_dev

def stop_at_high(state, std_dev, sl_coeff):
    return state + sl_coeff*std_dev
        
# Define the threshold functions
def upper(m, std_dev, std_dev_coeff):
    return m+std_dev_coeff*std_dev

def lower(m, std_dev, std_dev_coeff):
    return m-std_dev_coeff*std_dev

# Debugging mode: 1
debug = 0

## Name of the sectors 
#sec_1_str = "PM"
#sec_2_str = "WH"

## Getting the data for main contract
#sec_1 = DataAPI.MktMFutdGet(tradeDate=u"",mainCon=u"1",contractMark=u"",contractObject=sec_1_str,startDate=u"",endDate=u"",field=u"",pandas="1")
#sec_2 = DataAPI.MktMFutdGet(tradeDate=u"",mainCon=u"1",contractMark=u"",contractObject=sec_2_str,startDate=u"",endDate=u"",field=u"",pandas="1")

## Drop the rows where "closePrice" is NaN
#sec_1 = sec_1.dropna(subset=["closePrice"])
#sec_2 = sec_2.dropna(subset=["closePrice"])

## Sort rows by "tradeDate" column
#sec_1 = sec_1.sort("tradeDate")
#sec_2 = sec_2.sort("tradeDate")

## Inner join the two dataframes
#sec_12 = pd.merge(sec_1, sec_2, on="tradeDate")

# Sort the merged dataframes by "tradeDate"
sec_12 = pd.read_csv("sec_12.csv", encoding = "GBK")

n_fit = int(len(sec_12.index)/2) # Number of data for fitting and estimating the results
n_fit = 500 # Number of data for fitting and estimating the results

print("Number of periods used for fitting is ", n_fit)
print("Last date of the data is ", sec_12.tail(1)["tradeDate"])

# Subset the data used for trading
sec_12_t = sec_12.iloc[n_fit:-1,]

# Get OLS estimate for analysis period
ols = OLS(sec_12.closePrice_x[0:n_fit], add_constant(sec_12.closePrice_y[0:n_fit])).fit()
coint_results = coint(sec_12.closePrice_x, sec_12.closePrice_y)
mean = ols.params[0]
slope = ols.params[1]
print("Number of data for fitting is: ", n_fit)
print("OLS has the following estimates: \n", ols.params, "\n")
print("Cointegration test has results:\n", coint_results)
print("The p-value of the cointegration test is ", coint_results[1], "\n")

# Compute the ratio pair 
ratio = contract_ratio(slope)
print("The ratio of the contracts is ", ratio)

# Compute the price series
price = np.array([])
for index, row in sec_12.iterrows():
    # Actual price of the portfolio
    p = ratio[0]*row["closePrice_x"] - ratio[1]*row["closePrice_y"]
    price = np.hstack((price,p))
    #print(row["tradeDate"]) 
np.savetxt("pair_trade_2_price.txt", price)

# Compute the tradeDate series
tradeDate = np.array([])
for index, row in sec_12.iterrows():
    # Actual price of the portfolio
    tradeDate = np.hstack((tradeDate, row["tradeDate"]))

n_t = len(price) - n_fit # number of periods for trading
print(len(price), n_fit, n_t)
    
# Subset the price series for trading
price_t = price[n_fit:]
#print len(price), len(price_t)

# Subset the tradeDate series for trading
tradeDate_t = tradeDate[n_fit:]

# Plot the close price
plt.xlabel("All price series (Day)")
plt.ylabel("Close Price")
plt.plot(price)
#plt.show()

# Plot the close price for testing periods
plt.xlabel("Testing period (Day)")
plt.ylabel("Close Price")
plt.plot(price_t)
#plt.show()




# Define strategy parameters
if debug == 1:
    ma_len = np.array([10,15]) # window length for computing moving average of the price
    std_dev_len = np.array([10, 15]) # window length for computing the standard deviation
    std_dev_coeff = np.array([0.5, 1.0]) # threshold of the buy sell
    sl_coeff = np.array([1.0, 2.0]) # the coefficent of std_dev used for stop-loss decision
else:
    ma_len = np.arange(10, 65, 5) # window length for computing moving average of the price
    std_dev_len = np.arange(10, 65, 5) # window length for computing the standard deviation
    std_dev_coeff = np.arange(0.5, 2.4, 0.2) # threshold of the buy sell
    sl_coeff = np.arange(1.0, 3.0, 0.2) # the coefficent of std_dev used for stop-loss decision

# Define multi-dimensional array to save for profit for each combination of parameters
#profit_multi = np.zeros(len(ma_len)*len(std_dev_len)*len(std_dev_coeff)*len(sl_coeff)).reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
profit_multi = np.array([])

# Define multi-dimensional array to save for win rate
win_multi = np.array([])

# Iterate over all parameters. Index: 0: ma_len; 1: std_dev_len; 2: std_dev_coeff; 3: sl_coeff

for x in itertools.product(ma_len, std_dev_len, std_dev_coeff, sl_coeff):
    
    # Intialize position and profit information
    position = int(0) # number of contract for the portfolio, positive for long and negative for short
    state = 0 # current state of position, positive for long and negative for short
    profit = int(0) # single trade profit
    cum_profit = int(0) # cumulative profit
    commission = 0.0 # cumulative commission
    comm_rate = 1e-4 # commission rate
    unit = 10 # ton/contract, trading unit
    t_c = int(0) # Trade counter that records the number of trades
    t_c_win = int(0) # Trade counter that records the number of winning trades
    profit_series = np.array([]) # net profit series
    book_series = np.array([]) # book value series
    ma_series = np.zeros(n_t) # moving average series
    std_dev_series = np.zeros(n_t) # standard deviation series
    bs = np.zeros(len(price_t)) # mark buy any sell
    period = int(0) # variable to store period information
    bs_price = np.zeros(len(price_t)) # Price at which buy or sell occurs
    
    # Compute the first ma_len moving average
    for i in range(x[0]):
        my_list = price[(n_fit - x[0] + i):(n_fit+ i)]
        ma_series[i] = ma(my_list)
    print(ma_series[0:(x[0]+1)])

    # Compute the first ma_len moving average
    for i in range(x[1]):
        my_list = price[(n_fit - x[1] + i):(n_fit+ i)]
        std_dev_series[i] = std_dev(my_list)
    print(std_dev_series[0:(x[1]+1)])

    # Compute the first 

    # Buy low, sell high strategy, with stop-loss
    for i in range(len(price_t)):   
        # Calculate the moving average
        if abs(ma_series[i]) <= 1e-9:
            ma_series[i] = ma(price_t[(i-x[0]):i])

        # Calculate the sample standard deviation
        if abs(std_dev_series[i]) <= 1e-9:
            #print "The price series used to compute standard deviation is ", price_t[(i-x[1]):i]
            std_dev_series[i] = std_dev(price_t[(i-x[1]):i])
        #print "Standard deviation is ", std_dev_series[i], "Moving average is ", ma_series[i]

        # If NOT holding position:
        if position == 0:
            print(tradeDate_t[i])
            print("Not holding any position")

            # if profit_series is empty  
            if len(profit_series) == 0:
                # Append 0
                profit_series = np.hstack((profit_series, 0))
            # if not empty
            else:
                # Append the cumulative net profit stays the same
                profit_series = np.hstack((profit_series, profit_series[-1]))

            # Check if book_series is empty
            # if it's empty
            if len(book_series) == 0:
                # initialize by appending 0
                book_series = np.hstack((book_series, 0))
            # if not empty, current book_series value should be the same as the previous period
            else:
                book_series = np.hstack((book_series, book_series[-1]))

            # if the price is lower than the mean:
            if price_t[i] <= lower(ma_series[i], std_dev_series[i], x[2]):
                print(tradeDate_t[i])
                print("Portfolio price is: ", price_t[i])
                print("Moving average of the past data is", ma_series[i])
                # long the portfolio
                position = 1

                # record state value
                state = price_t[i]
                print("Long the portfolio. The state of the position is", state)


    #             # calculate cumulative commission
    #             commission += abs(sec_1_position)*row["closePrice_x"]*unit*comm_rate + \
    #              abs(sec_2_position)*row["closePrice_y"]*unit*comm_rate

                #update the count for trade
                t_c += 1 

                # Store the buy information
                bs_price[i] = price_t[i]
                bs[i] = int(1)

            # If the price is higher than the threshold:    
            elif price_t[i] >= upper(ma_series[i], std_dev_series[i], x[2]):
                print(tradeDate_t[i])
                print("Portfolio price is: ", price_t[i])
                print("Moving average of the past data is", ma_series[i])
                # short the portfolio
                position = -1
                state = price_t[i]

    #             # Record the state
    #             state = -sec_1_position*row["closePrice_x"]*unit - sec_2_position*row["closePrice_y"]*unit 
    #             print "Short the portfolio. The state of the position is", state

    #             # calculate cumulative commission
    #             commission += abs(sec_1_position)*row["closePrice_x"]*unit*comm_rate + \
    #              abs(sec_2_position)*row["closePrice_y"]*unit*comm_rate

                # update the counter for trade
                t_c += 1 

                # Store the sell information
                bs_price[i] = price_t[i]
                bs[i] = int(-1)

        # if holding position:
        # (in the case of holding position, book_series will not be empty)
        elif position != 0:        
            # if we previously longed and price went up, close by short
            if position > 0 and ( price_t[i] >= upper(ma_series[i], std_dev_series[i], x[2]) ):

                # record the single profit
                print(tradeDate_t[i], ": Close by short to earn profit and short another" )
                print("Portfolio price is", price_t[i])

                # Calculate the single profit 
                profit = price_t[i] -state
                print("Single trade profit is ", profit)
                
                # If earned positive profit, update the win counter
                if profit > 0:
                    t_c_win += 1

                # Store the buy sell information
                bs_price[period] = price_t[i]
                bs[period] = int(-1)     

                # update net profit_series
                profit_series = np.hstack((profit_series, profit+profit_series[-1]))         
                # update the book_series by appending the cumulative profit after this trade
                book_series = np.hstack((book_series, profit_series[-1]))   

                # Calculate the cumulative profit
                cum_profit = cum_profit + profit
                print("Cumulative profit is ", cum_profit, "\n"  )

                # update the count for trade
                t_c += 1 

                # update the position and state
                position = -1
                state = price_t[i]
                print("Long the portfolio. The state of the position is", state)

    #             # Calculate the commission
    #             commission += abs(sec_1_position)*row["closePrice_x"]*unit*comm_rate + \
    #              abs(sec_2_position)*row["closePrice_y"]*unit*comm_rate
    #             print "Cumulative commission is ", commission



            # if we previously shorted and price went down, close by long and long another
            elif position < 0 and ( price_t[i] <= lower(ma_series[i], std_dev_series[i], x[2]) ):

                # record the single profit
                print(tradeDate_t[i], ": Close by long to earn profit and long another" )
                print("Portfolio price is", price_t[i])

                # Calculate the single profit 
                profit = state - price_t[i]
                print("Single trade profit is ", profit)
                
                # If eared positive profit, update the win counter
                if profit > 0:
                    t_c_win += 1

                # Store the buy sell information
                bs_price[period] = price_t[i]
                bs[period] = int(1)     

                # update net profit_series
                profit_series = np.hstack((profit_series, profit+profit_series[-1]))         
                # update the book_series by appending the cumulative profit after this trade
                book_series = np.hstack((book_series, profit_series[-1]))   

                # Calculate the cumulative profit
                cum_profit = cum_profit + profit
                print("Cumulative profit is ", cum_profit, "\n" ) 

                # update the count for trade
                t_c += 1 

                # update the position and state
                position = 1
                state = price_t[i]
                print("Long the portfolio. The state of the position is", state)

    #             # calculate cumulative commission
    #             commission += abs(sec_1_position)*row["closePrice_x"]*unit*comm_rate + \
    #              abs(sec_2_position)*row["closePrice_y"]*unit*comm_rate         

            # if previously longed high and the price went down too much, stop-loss and long another
            elif position > 0 and  ( price_t[i] <= stop_at_low(state, std_dev_series[i], x[3]) ):

                # record the single profit
                print(tradeDate_t[i])
                print("Portfolio price is", price_t[i])
                print(tradeDate_t[i], ": Previously longed and the price went too low, stop-loss by short and long another") 

                # Calculate the price of clearing the position
                profit = price_t[i] - state

                # update the position and state
                position = 1
                state = price_t[i]

                # Calculate the cumulative profit
                cum_profit = cum_profit + profit

                # # Calculate the commission
                # commission += abs(sec_1_position)*row["closePrice_x"]*unit*comm_rate + \
                #  abs(sec_2_position)*row["closePrice_y"]*unit*comm_rate
                # print "Cumulative commission is ", commission

                # Store the buy sell information
                bs_price[period] = price_t[i]
                bs[period] = int(1)

                # update the count for trade
                t_c += 1 

                # update net profit_series
                profit_series = np.hstack((profit_series, profit+profit_series[-1]))         
                # update the book_series by appending the cumulative profit after this trade
                book_series = np.hstack((book_series, profit_series[-1]))

                print("Single trade profit is ", profit)
                print("Cumulative profit is ", cum_profit, "\n")

            # if previously shorted and the price went up too much, stop-loss by long and short another
            elif position < 0 and  ( price_t[i] >= stop_at_high(state, std_dev_series[i], x[3]) ):

                # record the single profit
                print(tradeDate_t[i])
                print("Portfolio price is", price_t[i])
                print(tradeDate_t[i], ": Previously shorted and the price went too high, stop-loss by long and short another") 

                # Calculate the price of clearing the position
                profit = state - price_t[i]

                # update the position and state
                position = 1
                state = price_t[i]

                # Calculate the cumulative profit
                cum_profit = cum_profit + profit

                # # Calculate the commission
                # commission += abs(sec_1_position)*row["closePrice_x"]*unit*comm_rate + \
                #  abs(sec_2_position)*row["closePrice_y"]*unit*comm_rate
                # print "Cumulative commission is ", commission

                # Store the buy sell information
                bs_price[period] = price_t[i]
                bs[period] = int(-1)

                # update the count for trade
                t_c += 1 

                # update net profit_series
                profit_series = np.hstack((profit_series, profit+profit_series[-1]))         
                # update the book_series by appending the cumulative profit after this trade
                book_series = np.hstack((book_series, profit_series[-1]))

                print("Single trade profit is ", profit)
                print("Cumulative profit is ", cum_profit, "\n")

            # In the case of holding postion where no trade in the current period:
            # (in this case, the profit_series will be non-empty)
            else:
                # update the profit_series
                profit_series = np.hstack((profit_series, profit_series[-1]))

                # update the book_series, which should be the sum of previous net profit and 
                #the mark-to-market fluctuations. 
                #Should distinuguish between currently long and currently short
                # If the state is long
                if position > 0:
                    book_series = np.hstack((book_series, profit_series[-1] +                      price_t[i] - state))
                if position < 0:
                    book_series = np.hstack((book_series, profit_series[-1] +                      state - price_t[i])) 
        # Update the period
        period += 1

    print("Final profit is ", cum_profit)
    #print "Net profit is ", cum_profit - commission
    print("Total number of trades is ", t_c)
    #print "The price series of the portfolio is ", ps

    # Compute Bollinger channer
    k1_upper = np.add(ma_series, std_dev_series*x[2])
    k1_lower = np.subtract(ma_series, std_dev_series*x[2])

    print(k1_upper, k1_lower)

    # Plot the profit_series

    plt.subplot(3,1,1)
    plt.ylabel("Profit_series")
    plt.plot(profit_series, linewidth=0.1)

    # Plot the book_series
    plt.subplot(3,1,2)
    plt.ylabel("Book_series")
    plt.plot(book_series, linewidth=0.1)


    # Plot the buy, sell information
    plt.subplot(3,1,3)
    for i in range(len(bs)):
        if bs[i] == 1:
            plt.xlim([0,2500])
            plt.scatter(i,bs_price[i], color="r",s=0.1)
            plt.xlim([0,2500])
        if bs[i] == -1:
            plt.scatter(i,bs_price[i], color="g",s=0.1)
    plt.plot(price_t,linewidth=0.1)
    plt.plot(ma_series, linewidth=0.1)
    plt.plot(k1_upper, linewidth=0.1)
    plt.plot(k1_lower, linewidth=0.1)
    plt.xlabel("Testing period (Day)")
    plt.savefig("pair_trade_2.eps", format="eps")
    plt.close()


    # # Check if profit_series and book_series is the same
    # for i in range(len(profit_series)):
    #     if profit_series[i] != book_series[i]:
    #         print i, profit_series[i], book_series[i]
    print(len(profit_series), len(book_series), len(price_t))

    min_index = np.argmin(abs(k1_upper - k1_lower))
    print(np.min(abs(k1_upper - k1_lower)), ma_series[min_index], std_dev_series[min_index])
    
    # Save the profit for this set of parameters
    profit_multi = np.hstack((profit_multi, profit_series[-1]))

#profit_multi = profit_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
np.savetxt("pair_trade_2_profit_multi.txt", profit_multi)
