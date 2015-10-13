#!/usr/bin/python

a = 3
b = 10
c = 7
i = 0
x = [0.0, 0.0]

# when 4 of these are run at once the processor will end up at about 40 degrees C
while i < 100000000 * 4:
	try:
		x[0] = -b + (b ** 2 - 4 * a * c) ** .5 / 2 * a
	
		x[1] = -b - (b ** 2 - 4 * a * c) ** .5 / 2 * a
	except ValueError:
		print 'Value Error'
	
	i += 1
