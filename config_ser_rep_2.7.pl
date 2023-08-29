#!/usr/bin/env python

# Python script to modify device configs
# Ver 0.01 7/11/19
#
# By Frank L. Sundstrom
# f_sundstrom@yahoo.com
#

# load standard modules
import os
import re
import sys

# get input
config_file = raw_input("config file = ")
csv_file = raw_input("CSV file = ")

# read config
myfile = open(config_file,"r")
config=myfile.read()
myfile.close()

# read CSV 
with open(csv_file,"r") as file:
   line = "1"
   x = 1
   while line:
     line = file.readline()
     if line :
       values = line.split(",")
       print (values[0]) 
       print (values[1]) 
       config= config.replace(values[0],values[1])

print ("--------------------------")
print (config)
newfile = open(config_file+".new","w+")
newfile.write(config)
newfile.close()
     
