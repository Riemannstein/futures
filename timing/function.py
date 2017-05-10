import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import os
import time
from statsmodels.tsa.stattools import adfuller
from param import *

def loss_disp(minPriceChange, displacement):
	"""Calculates the loss due to displacement"""
	
	n = int(displacement/minPriceChange)
	return -minPriceChange*n*(n+1)/2

def gain_osci(price):
	"""Calculates the gain due to oscillation"""
	
	gain_cum = 0.0
	for i in range(1,len(price)):
		gain_cum += abs(price[i]-price[i-1])
	
	return gain_cum/2

def sma(list):
    "Compute the moving average of a list of non-zero length by using simple arithematic mean"
    if len(list) == 0:
        print("Empty list, moving average not defined")
    else:
        return float(sum(list))/float(len(list))
 
def sma_r(prev_sum, old, new, n):
	"""Compute the simple moving average recursively"""
	if n <= 0:
		print("No data, simple moving average not define") 
	else:
		return (prev_sum + new - old)/n  

# Compute simple moving average and adjust position if necessary
def process_tick(sma_short, sma_long, lastPrice, position, profit_cum, i, book):
	new_position = position
	new_profit_cum = profit_cum
	if sma_short > sma_long and position < 0:
		new_profit_cum = new_profit_cum + ( -position - lastPrice)
		new_position = lastPrice 
		book[i] = new_profit_cum
	elif sma_short < sma_long and position > 0:
		new_profit_cum = new_profit_cum + (lastPrice - position)
		new_position = -lastPrice 
		book[i] = new_profit_cum
	elif position > 0:
		book[i] = profit_cum + (lastPrice -position)
	elif position < 0:
		book[i] = profit_cum + (-lastPrice -position)

 
	return new_position, new_profit_cum

