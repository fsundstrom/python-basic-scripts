#!/usr/bin/python2.7

# Python script to import switch MACs into mongoBD
# Ver 1.03 3/29/18
#
# By Frank L. Sundstrom
# f_sundstrom@yahoo.com
#

# load modules

import json
import re
import os
import time
import datetime
import logging
import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

#################
# Default vars  #
#####################################################################
device_list = []
device_ip_list = []

# set up logging

#############
# Main code #
#####################################################################
#####################################################################


# reae in config file list
with open("test.lst","r") as list:
   file = " "
   while file:
      file = list.readline()
      file = '/tftpboot/prod/backup-configs/'+str(file) 
      new_file = file.rstrip("\n")
      new_file = new_file+'-confg'
      print(new_file)

      # parse config
      try: 
         with open(new_file,"r") as config:
            line = " "
            while line:
               line = config.readline()
               if re.match(r'^interface Management.*',line):
                  while '!' not in line:
                     line = config.readline()
                     if "ip address" in line:
                       print new_file,line
      except:
         print(file,' ','ERROR No Config')

