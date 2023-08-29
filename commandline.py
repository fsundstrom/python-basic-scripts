#!/usr/bin/python
import sys

print (sys.argv)

for i in range(len(sys.argv)):
    if i == 0:
        print "Scriptname is %s" % (sys.argv[0])
    else:
        print "%d argument is %s" % (i,sys.argv[i])

