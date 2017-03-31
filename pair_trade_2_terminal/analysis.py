
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import seaborn as sns

# 1 for debug mode, 2 for test optimal mode
debug = 0

delta = [5.0, 5.0, 0.2, 0.2]
# Do NOT change the order of the definition!!

if debug == 1:
    ma_len = np.array([10,15]) # window length for computing moving average of the price
    std_dev_len = np.array([10, 15]) # window length for computing the standard deviation
    std_dev_coeff = np.array([0.5, 1.0]) # threshold of the buy sell
    sl_coeff = np.array([1.0, 2.0]) # the coefficent of std_dev used for stop-loss decision
    

else:
    ma_len = np.arange(5, 40, 5) # window length for computing moving average of the price
    std_dev_len = np.arange(35, 50, 5) # window length for computing the standard deviation
    std_dev_coeff = np.arange(0.1, 0.6, 0.1) # threshold of the buy sell
    sl_coeff = np.arange(3.0, 5.0, 0.3) # the coefficent of std_dev used for stop-loss decision

strat_param = np.array([ma_len, std_dev_len, std_dev_coeff, sl_coeff])

# Load the data
profit_multi = np.loadtxt("./data/profit_multi.txt")
win_multi = np.loadtxt("./data/win_multi.txt")
profit_std_dev_multi = np.loadtxt("./data/profit_std_dev_multi.txt")
max_drawdown_multi = np.loadtxt("./data/max_drawdown_multi.txt")
max_drawdown_rate_multi = np.loadtxt("./data/max_drawdown_rate.txt")
max_drawdown_period_multi = np.loadtxt("./data/max_drawdown_period_multi.txt")

# Compute the kama
profit_multi = profit_multi.astype(float)
kama_multi = profit_multi/max_drawdown_multi

# Compute the Sharpe ratio 
sharpe_multi = profit_multi/profit_std_dev_multi

print("The number of parameters considered is", len(strat_param))

# Resahpe the multi series
profit_multi = profit_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("The optimal profit is \n", profit_multi.max(), "\n")
o_i = np.unravel_index(profit_multi.argmax(), profit_multi.shape) # optimum index for profit

win_multi = win_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("The win rate for each parameter combination is \n", win_multi, "\n")
oi_win = np.unravel_index(win_multi.argmax(), win_multi.shape) # Optimum index for profit
print("The optimal win rate is ", win_multi[oi_win], "for index ", oi_win, "\n")

profit_std_dev_multi = profit_std_dev_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("Profit standard deviatin for each set of parameters is \n", profit_std_dev_multi, "\n")

max_drawdown_multi = max_drawdown_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("Maximum drawdown for each set of parameters is \n", max_drawdown_multi, "\n")

max_drawdown_rate_multi = max_drawdown_rate_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("Maximum drawdown rate for each set of parameters is \n", max_drawdown_rate_multi, "\n")

max_drawdown_period_multi = max_drawdown_period_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("Maximum drawdown period for each set of parameters is \n", max_drawdown_period_multi, "\n")

kama_multi = kama_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("Kama ratio for each set of parameters is \n", kama_multi, "\n")

sharpe_multi = sharpe_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("Sharpe ratio for each set of parameters is \n", sharpe_multi, "\n")



print("The optimal profit is ", profit_multi[o_i]) 
print("Optimal parameter index for profit is ", o_i)

profit_plot = sns.heatmap(profit_multi[1][1][:][:])
profit_plot.set_title("Net profit")
profit_plot.set(xlabel = "Standard deviation", ylabel = "Stop-loss standard deviation")
profit_fig = profit_plot.get_figure()
profit_fig.savefig("./plot/profit_heatmap.eps")
plt.close()

win_plot = sns.heatmap(win_multi[1][1][:][:])
win_plot.set_title("Win rate")
win_plot.set(xlabel = "Standard deviation", ylabel = "Stop-loss standard deviation")
win_fig = win_plot.get_figure()
win_fig.savefig("./plot/win_heatmap.eps")
plt.close()

profit_std_dev_plot = sns.heatmap(profit_std_dev_multi[1][1][:][:])
profit_std_dev_plot.set_title("Standard deviation of net profit")
profit_std_dev_plot.set(xlabel = "Standard deviation", ylabel = "Stop-loss standard deviation")
profit_std_dev_fig = profit_std_dev_plot.get_figure()
profit_std_dev_fig.savefig("./plot/profit_std_dev_heatmap.eps")
plt.close()

max_drawdown_plot = sns.heatmap(max_drawdown_multi[1][1][:][:])
max_drawdown_plot.set_title("Maximum drawdown")
max_drawdown_plot.set(xlabel = "Standard deviation", ylabel = "Stop-loss standard deviation")
max_drawdown_fig = max_drawdown_plot.get_figure()
max_drawdown_fig.savefig("./plot/max_drawdown_heatmap.eps")
plt.close()

max_drawdown_rate_plot = sns.heatmap(max_drawdown_rate_multi[1][1][:][:])
max_drawdown_rate_plot.set_title("Maximum drawdown rate")
max_drawdown_rate_plot.set(xlabel = "Standard deviation", ylabel = "Stop-loss standard deviation")
max_drawdown_rate_fig = max_drawdown_rate_plot.get_figure()
max_drawdown_rate_fig.savefig("./plot/max_drawdown_rate_heatmap.eps")
plt.close()

max_drawdown_period_plot = sns.heatmap(max_drawdown_period_multi[1][1][:][:])
max_drawdown_period_plot.set_title("Maximum drawdown period")
max_drawdown_period_plot.set(xlabel = "Standard deviation", ylabel = "Stop-loss standard deviation")
max_drawdown_period_fig = max_drawdown_period_plot.get_figure()
max_drawdown_period_fig.savefig("./plot/max_drawdown_period_heatmap.eps")
plt.close()


kama_plot = sns.heatmap(kama_multi[1][1][:][:])
kama_plot.set_title("Kama")
kama_plot.set(xlabel = "Standard deviation", ylabel = "Stop-loss standard deviation")
kama_fig = kama_plot.get_figure()
kama_fig.savefig("./plot/kama_heatmap.eps")
plt.close()

sharpe_plot = sns.heatmap(profit_multi[1][1][:][:])
sharpe_plot.set_title("Sharpe ratio")
sharpe_plot.set(xlabel = "Standard deviation", ylabel = "Stop-loss standard deviation")
sharpe_fig = sharpe_plot.get_figure()
sharpe_fig.savefig("./plot/sharpe_heatmap.eps")
plt.close()



#if debug != 1:

	#d_i = np.array([-1,1])

	#for di in d_i:
		#if di >0 and (di + o_i[0]) < len(strat_param[0]):
			#print("Optimal profit is ", profit_multi[o_i[0]+di][o_i[1]][o_i[2]][o_i[3]]) 
		#elif di <0 and (di + o_i[0]) >= 0:
			#print("Optimal profit is ", profit_multi[o_i[0]-di][o_i[1]][o_i[2]][o_i[3]]) 
			
	#for di in d_i:
		#if di >0 and (di + o_i[1]) < len(strat_param[1]):
			#print("Optimal profit is ", profit_multi[o_i[0]][o_i[1]+1][o_i[2]][o_i[3]]) 
		#elif di <0 and (di + o_i[1]) >= 0:
			#print("Optimal profit is ", profit_multi[o_i[0]-di][o_i[1]-1][o_i[2]][o_i[3]]) 
			
	#for di in d_i:
		#if di >0 and (di + o_i[2]) < len(strat_param[2]):
			#print("Optimal profit is ", profit_multi[o_i[0]+di][o_i[1]][o_i[2]+1][o_i[3]]) 
		#elif di <0 and (di + o_i[2]) >= 0:
			#print("Optimal profit is ", profit_multi[o_i[0]-di][o_i[1]][o_i[2]-1][o_i[3]]) 
			
	#for di in d_i:
		#if di >0 and (di + o_i[3]) < len(strat_param[3]):
			#print("Optimal profit is ", profit_multi[o_i[0]+di][o_i[1]][o_i[2]][o_i[3]+1]) 
		#elif di <0 and (di + o_i[3]) >= 0:
			#print("Optimal profit is ", profit_multi[o_i[0]-di][o_i[1]][o_i[2]][o_i[3]-1]) 
			
	#print(ma_len[0], std_dev_len[6], std_dev_coeff[0], sl_coeff[9])



	
	




