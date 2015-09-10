#Operators
#
# Operator      Function 
#    +              Addition
#    -              Subtraction
#    *              Multiplication
#    /              Division
#    %              Remainder
#    **             Exponent


#Declairing a variable

a = 0
b = "Test sucessful"


#Printing Text

print("Text", b, a)



#Taking input from a user

c = input("Enter some words: ")

print(c)


#While loop

while a < 10:
    a = a + 1
    print(a)


#Logical Operators
#
# Operator      Function 
#    <              less than
#    <=             less than or equal to
#    >              greater than
#    >=             greater than or equal to
#    !=             not equal to 
#    <>             not equal to 
#    ==             equal to


#if Statement

y = 5

if y > 6:
    print("y is less than 6 so this shouldn't happen")
elif y > 10:
    print("y is still less than 10 so this shouldn't happen")
else:
    print("nothing else worked so this should happen")


#Creating a function

e = 0

def add(f, g): #Defines function, using f and g as parameters
    e = f + g
    return e

#Calling the function

print(add(2, 2))

    
#Tuples- like an array marked as final in java

months = ('january', 'february', 'march', 'april', 'june', 'july', 'august', 'september', 'november', 'december')


#Lists- like an array in java

names = ['Tom', 'joe', 'george', 'john']

#Printing a list value

print(names[2]) #The numbering starts at 0 so this will print "george"

#Add to a list

names.append('andrew')

#Remove an item from a list

del names[0]


#Dictionaries- kinda like 2D arrays in java

phonenumbers = {'Tom' :6873654, 'Joe' :6844468, 'George' :4688869, 'John' :9874433}

#Add to the Dictionary

phonenumbers['Andrew'] = 5468937

#Delete an entry

del phonenumbers['Tom']

#Simple dictionary search example

ages = {'andrew' :16, 'john' :19, 'tom' :29}
n = input("Enter a name to search: ")

#if ages.has_key(n): ages.has_key is an error.
#    print(n, "is in the dictionary, he is ", ages[n], "years old.")
#else:
#    print(n, "is not in the dictionary")

#There is more to dictionaries but I dont feel like typing it out, moving on...



#for Loops

#create a list to loop through
list = ['All', 'of', 'the', 'values', 'in', 'the', 'list', 'get', 'printed']

for value in list: #This is a lot like a for-each loop in java, the variable value can be changed.
    print(value)


























