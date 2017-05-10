from function import *
test_list = [1,2,3,4,5,6]
print(gain_osci(test_list))
print(loss_disp(2,10))

x = 10
def my_print():
	print(x)

my_print()
def my_change():
	global x
	x = 20
	return 
my_change()
print(x)
