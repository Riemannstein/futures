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
		
