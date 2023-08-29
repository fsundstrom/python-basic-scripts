#!/usr/bin/python
try:
    number = int(input("Enter a number"))
    print (number)
except ValueError:
    print ("Exception --- Data type is Invalid")

try:
    number = input("Enter a number")
    print (number)
    a = [1,2,3]
    print (a[2])
    if a[0] == 1:
    print ("equal")
    else:
        print ("not equal")
except NameError:
    print ("Exception --- Name is not defined")
except IndexError:
    print ("Exception --- Index out of range")
except SyntaxError:
    print ("Exception --- Syntax Error")

try:
   fh = open("testfile", "r")
   fh.write("This is my test file for exception handling!!")
except IOError:
   print ("Error: can\'t find file or read data")
else:
   print ("Written content in the file successfully")
