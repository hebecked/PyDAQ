#!/usr/bin/python


def write_file(dates, hours):
	data_file = open('/home/andrew/Documents/Python/hours.dat', 'w')
	t = ''
	i = 0
	#data_file.write('')
	
	for d in dates:
		t += d + '\n' + hours[i] + '\n'
		i += 1
	t += '\\'
	
	data_file.write(t)
	data_file.close()



data_file = open('/home/andrew/Documents/Python/hours.dat', 'rw')
dates  = []
hours = []
i = 0
r = True

#reading data file
while r:
	d = data_file.readline()
	if d == '\\':
		r = False
	else:
		h = data_file.readline()
		dates.append(d[0:len(d) - 1])
		hours.append(h[0:len(h) - 1])
	
	i += 1
	


done = False

#main menu
while not done:

	print '1) Enter Hours'
	print '2) List Hours'
	print '3) Remove Entry'
	print '4) Clear Database'
	print '5) exit'
	choice = raw_input('\nEnter a number to continue: ')
	
	if choice == '1' or choice == '2' or choice == '3' or choice == '4' or choice == '5':
		if choice == '1':
			b = True
			
			while b:
				print 
				d = raw_input('Enter work date [mm/dd/yy]: ')
				h = raw_input('Enter number of hours worked: ')
				dates.append(d)
				hours.append(h)
				
				
				c = raw_input('Enter more hours? [y/n]: ')
				if c != 'y':
					b = False
			
			#write changes to file
			write_file(dates, hours)
			
			print
			
		elif choice == '2':
			i = 0
			total_hours = 0
			
			print '\nDates          Hours'
			
			for d in dates:
				print '%s      %s' % (d, hours[i])
				i += 1
			
			for h in hours:
				t = int(h)
				total_hours += t
			
			print '\nTotal hours: %s\n\n' % (total_hours)
			
		elif choice == '3':
			i = 0
			rem = raw_input('\nEnter Date of entry to remove. [mm/dd/yy]: ')
			
			if rem in dates:
				i = dates.index(rem)
				
				dates.pop(i)
				hours.pop(i)
				
				#write changes to file
				write_file(dates, hours)
				
				print '\n\n'
			else:
				print 'Entry not found.\n\n'
				
		elif choice == '4':
			c = raw_input('\nClear all entries from database? [yes/n]: ')
			
			if c == 'yes':
				for n in range(0, len(dates)):
					dates.pop(n)
					hours.pop(n)
					
				write_file(dates, hours)
			print '\n'
		elif choice == '5':
			done = True
	
	
