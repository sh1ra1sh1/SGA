import random
import math

# イカサマコイン
def coin(prob):
	flip = random.random()
	if flip < prob:
		return 0
	else:
		return 1

# n-dimension Rastrigin function
def rastrigin_function(x):
	d = len(x)

	temp = 0.0
	for i in range(0, d):
		temp += pow(x[i], 2) - 10.0 * math.cos(2.0 * math.pi * x[i])
	fx = 10 * d + temp
	return fx

