#!/usr/bin/python
import os
mem=str(os.popen('free -t -m').readlines())
#print (mem)
T_ind=mem.index('T')
mem_G=mem[T_ind+14:-4]
#print (mem_G)
S1_ind=mem_G.index(' ')
mem_T=mem_G[0:S1_ind]

print 'Summary = ' + mem_G
print 'Total Memory = ' + mem_T +' MB'

mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
print (mem_bytes)
mem_gib = mem_bytes/(1024.**3)
print (mem_gib)
