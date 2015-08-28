

class test(object):

	def __init__(self,dog):
		self.dog=dog
		print "1" + self.dog

	def __enter__(self):
		print "2" + self.dog
		return self

	def __exit__(self, *args):
		print "3" + self.dog
		#return True

	def print_bear(self):
		print self.dog

if __name__=="__main__":
	classe=test("cat")
	with classe as mouse:
		mouse.print_bear()

	with test("Elephant") as ant:
		ant.print_bear()

	print "filo"
	classe.print_bear()
