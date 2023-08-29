#!/usr/bin/python
from timeit import Timer

def listTest():
    list_data=[3,2,1,4,7,9,5,8,6,10,11,12,14,13,15,19,20,18,16,17,876,345,123,34,45,98,5432,4354,65,99]
    list_data2=[13,76,98,99,1,4,5,7,6]
    #list_data.sort()
    #print list_data
    #list_data.index(14)
    max(list_data)
    #len(list_data)
    #list_data + list_data2
    #list(set(list_data + list_data2))

def tupleTest():
    tuple_data=(3,2,1,4,7,9,5,8,6,10,11,12,14,13,15,19,20,18,16,17,876,345,123,34,45,98,5432,4354,65,99)
    tuple_data2=(13,76,98,99,1,4,5,7,6)
    tuple(sorted(tuple_data))
    #tuple_data.index(14)
    max(tuple_data)
    #len(tuple_data)
    #tuple_data + tuple_data2
    #tuple(set(tuple_data + tuple_data2))

t_listTest = Timer(listTest)
print("listTester: " + str(t_listTest.timeit())) 

t_tupleTest = Timer(tupleTest)
print("tupleTester:" + str(t_tupleTest.timeit()))


