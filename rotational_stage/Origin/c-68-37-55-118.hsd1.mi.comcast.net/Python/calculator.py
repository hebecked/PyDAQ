#Python Calculator program
#Andrew Ozimek

r = 1

def add(a, b):
    sum = a + b
    return sum

def subtract(a, b):
    difference = a - b
    return difference

def multiply(a, b):
    product = a * b
    return product

def divide(a, b):
    quotient = a / b
    return quotient

while r == 1:
    print "(1) Add"
    print "(2) Subtract" 
    print "(3) Multiply" 
    print "(4) Divide"
    print "(5) Exit"
    print ""
    choice = input("Enter a number to continue: ")
    
    if choice == 1:
        a = input("Enter the first number to be added: ")
        b = input("Enter the second number to be added: ")
        answer = add(a, b)
        print "\nThe sum of ", a, " and ", b, " is ", answer, "\n"
    elif choice == 2:
        a = input("Enter the first number to be subtracted: ")
        b = input("Enter the second number to be subtracted: ")
        answer = subtract(a, b)
        print "\nThe difference of ", a, " and ", b, " is ", answer, "\n"
    elif choice == 3:
    	a = input("Enter the first number to be multiplied: ")
        b = input("Enter the second number to be multiplied: ")
        answer = multiply(a, b)
        print "\nThe product of ", a, " and ", b, " is ", answer, "\n"
    elif choice == 4:
	a = input("Enter the first number to be divided: ")
        b = input("Enter the second number to be divided: ")
        answer = divide(a, b)
        print "\nThe quotient of ", a, " and ", b, " is ", answer, "\n"
    elif choice == 5:
	r = 0
    else:
	print "\nInvalid Choice\n"
   
