


class DAQ_handler(object):
	"""docstring for DAQ_handler"""
	def __init__(self):
		'''takes:dict with ports and settings'''
		inicialises pipe
		init data storage
		creates subprocess with dict and pipe


	def update():
		while True:
			result=que.get()
			if result==None:
				break
			self.datastorage.append(result)

	def send_signal(signal):
		if signal=='pause'/'stop/kill'/'continue'

