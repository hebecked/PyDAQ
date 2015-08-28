#!/usr/bin/python

file_r = open('/home/andrew/Documents/Web_Server/index.html', 'r')
file_w = open('/home/andrew/Documents/Web_Server/index.py', 'w')

lines = []
read = True

while read:
	temp = file_r.readline()
	
	if temp != '':
		lines.append(temp)
	else:
		read = False
		
text = ['#!/usr/env/python\n', "print 'Content-Type: html\\n'\n"]
p = "print '"

for line in range(1, len(lines)):
	text.append(p + lines[line] + "'")
	
for line in text:
	file_w.write(line)
