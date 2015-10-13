import sys

class Item:
    def __init__(self, nm, pr, qt, num):
        self.name = nm
        self.price = pr
        self.quantity = qt
        self.itemnum = num
    
    def getName(self):
        return self.name
    
    def getPrice(self):
        return self.price
    
    def getQuantity(self):
        return self.quantity
    
    def getItemNum(self):
        return self.itemnum


print 'Welcome to Inventory.py\n'

r = 0
items = []

while r == 0:
    choice = input('1) Add Item\n2) Remove Item\n3) Display All Items\n4) Exit\nEnter a number to continue --> ')

    if choice == 1:
        nm = raw_input('Enter the item name --> ')
        pr = raw_input('Enter the item price --> ')
        qt = raw_input('Enter the item quantity --> ')
        num = raw_input('Enter the item number --> ')
        
        items.append(Item(nm, pr, qt, num))
    elif choice == 3:
        print items[0].getName()
    elif choice == 3:
        i = 2
    elif choice == 4:
        #sys.exit()
        print 'this should exit'


