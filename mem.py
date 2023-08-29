#!/usr/bin/python
import os
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
print (mem_bytes)
mem_gib = mem_bytes/(1024.**3)
print (mem_gib)

