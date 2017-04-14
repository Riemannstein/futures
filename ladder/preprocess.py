import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from param import *



# Sum of the absolute value of the change in price
tv = 0.0

# Absolute value of the difference between close and open price 
displacement = abs( df.iloc[-1]["closePrice"] - df.iloc[-1]["openPrice"] )
print("Displacement of date ", df.iloc[-1]["dataDate"], " is ", displacement)


# Compute the total variation to displacement ratio
tv_to_disp = 0.0

for i in range(len(df)):
	if i == 0:
		tv = 0.0
	else:
		tv += abs( df.iloc[i]["lastPrice"] - df.iloc[i-1]["lastPrice"] )

print("The total variation of the lastPrice series is ", tv)

if displacement == 0:
	tv_to_disp = float("inf")
else:
	tv_to_disp = tv/float(displacement)

print("Total variation to displacement ratio is ", tv_to_disp)
	
