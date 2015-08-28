#!/usr/bin/python

from multiprocessing import Pool
from random import randint

pool = Pool(processes=4)

def problem(iterations):
	y = 0
	
	#for i in range(iterations):
	y = 875164926 ** 307407024 * 30284451 + 163721008 - 841819296 / 78024825 - 564784244 % 643620825
	
	return y
	
result = pool.apply_async(problem, [1])
