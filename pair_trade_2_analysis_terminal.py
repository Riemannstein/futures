
# coding: utf-8

# In[ ]:


import numpy as np
import itertools

debug = 1

delta = [5.0, 5.0, 0.2, 0.2]
# Do NOT change the order of the definition!!

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
strat_param = np.array([ma_len, std_dev_len, std_dev_coeff, sl_coeff])

profit_multi = np.loadtxt("pair_trade_2_profit_multi.txt")
win_multi = np.loadtxt("pair_trade_2_win_multi.txt")
profit_std_dev_multi = np.loadtxt("pair_trade_2_profit_std_dev_multi.txt")
print("The number of parameters considered is", len(strat_param))

# Resahpe the multi series
profit_multi = profit_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("The optimal profit is ", profit_multi.max())
o_i = np.unravel_index(profit_multi.argmax(), profit_multi.shape) # optimum index for profit

win_multi = win_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("The win rate for each parameter combination is ", win_multi)
oi_win = np.unravel_index(win_multi.argmax(), win_multi.shape) # Optimum index for profit
print("The optimal win rate is ", win_multi[oi_win], "for index ", oi_win)

profit_std_dev_multi = profit_std_dev_multi.reshape(len(ma_len),len(std_dev_len),len(std_dev_coeff),len(sl_coeff))
print("Profit standard deviatin for each set of parameters is ", profit_std_dev_multi)






print("The optimal profit is ", profit_multi[o_i]) 
print("Optimal parameter index is ", o_i)

d_i = np.array([-1,1])

for di in d_i:
	if di >0 and (di + o_i[0]) < len(strat_param[0]):
		print("Optimal profit is ", profit_multi[o_i[0]+di][o_i[1]][o_i[2]][o_i[3]]) 
	elif di <0 and (di + o_i[0]) >= 0:
		print("Optimal profit is ", profit_multi[o_i[0]-di][o_i[1]][o_i[2]][o_i[3]]) 
		
for di in d_i:
	if di >0 and (di + o_i[1]) < len(strat_param[1]):
		print("Optimal profit is ", profit_multi[o_i[0]][o_i[1]+1][o_i[2]][o_i[3]]) 
	elif di <0 and (di + o_i[1]) >= 0:
		print("Optimal profit is ", profit_multi[o_i[0]-di][o_i[1]-1][o_i[2]][o_i[3]]) 
		
for di in d_i:
	if di >0 and (di + o_i[2]) < len(strat_param[2]):
		print("Optimal profit is ", profit_multi[o_i[0]+di][o_i[1]][o_i[2]+1][o_i[3]]) 
	elif di <0 and (di + o_i[2]) >= 0:
		print("Optimal profit is ", profit_multi[o_i[0]-di][o_i[1]][o_i[2]-1][o_i[3]]) 
		
for di in d_i:
	if di >0 and (di + o_i[3]) < len(strat_param[3]):
		print("Optimal profit is ", profit_multi[o_i[0]+di][o_i[1]][o_i[2]][o_i[3]+1]) 
	elif di <0 and (di + o_i[3]) >= 0:
		print("Optimal profit is ", profit_multi[o_i[0]-di][o_i[1]][o_i[2]][o_i[3]-1]) 
		
print(ma_len[0], std_dev_len[6], std_dev_coeff[0], sl_coeff[9])



	
	




