class dataIO:

	class files:


	class serialports:
		import PyQt5.QtSerialPort
		element = PyQt5.QtSerialPort.QSerialPortInfo()
		ports=a.availablePorts()
		realloc=[]
		for port in ports:
			realloc.append(port.systemLocation())
