#!/usr/bin/python3

class Fraction:
	undefined = False
	numerator = 0
	denominator = 0
	
	def __init__(self, numerator, denominator):
		self.numerator = numerator
		self.denominator = denominator
		
		if denominator == 0:
			self.numerator = 0
			self.denominator = 0
			undefined = True
		
		self.reduce_fraction()
		
	def getNumerator(self):
		return self.numerator
	
	def getDenominator(self):
		return self.denominator
	
	def get_fraction(self):
		return str(int(self.numerator)) + '/' + str(int(self.denominator))
	
	
	def add(self, fraction):
		return Fraction((self.numerator * fraction.denominator) + (fraction.numerator * self.denominator), (self.denominator * fraction.denominator))
	
	def subtract(self, fraction):
		return Fraction((self.numerator * fraction.denominator) - (fraction.numerator * self.denominator), (self.denominator * fraction.denominator))
	
	def multiply(self, fraction):
		return Fraction((self.numerator * fraction.numerator), (self.denominator * fraction.denominator))
	
	def divide(self, fraction):
		return Fraction((self.numerator * fraction.denominator), (self.denominator * fraction.numerator))
	
	def reciprocal(self):
		return Fraction(self.denominator, self.numerator)
	
	
	def greatest_common_divisor(self, number_one, number_two):
		if number_one == 0 or number_two == 0:
			return number_one
		else:
			return self.greatest_common_divisor(number_one, number_one % number_two)
		
	def reduce_fraction(self):
		gcd = self.greatest_common_divisor(self.numerator, self.denominator)
		
		if gcd != 0:
			self.numerator /= gcd
			self.denominator /= gcd
		
		self.fix_negatives()
	
	def fix_negatives(self):
		if (self.numerator > 0 and self.denominator < 0) or (self.numerator < 0 and self.denominator < 0):
			self.numerator = -self.numerator
			self.denominator = -self.denominator
