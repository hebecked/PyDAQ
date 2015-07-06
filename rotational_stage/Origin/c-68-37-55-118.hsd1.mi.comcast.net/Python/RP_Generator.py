#!/usr/bin/python

import random

#random.randint(1, 10)

l_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
c_letters = []
symbols = ['!', '@', '#', '$', '%', '&', '*', '.', '?', ',']
gen_password = ''
i = 0

for l in l_letters:
	c_letters.append(l.upper())


l = raw_input('Enter length of password: ')

while i < int(l):
	char_type = random.randint(1, 4)
	
	
	if char_type == 1:
		gen_password += l_letters[random.randint(0, 25)]
	elif char_type == 2:
		gen_password += c_letters[random.randint(0, 25)]
	elif char_type == 3:
		gen_password+= str(random.randint(0,9))
	elif char_type == 4:
		gen_password += symbols[random.randint(0, len(symbols) - 1)]
	
	i += 1
	
print '\nPassword:\n\n%s' % (gen_password)
