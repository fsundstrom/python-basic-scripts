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
   while list:
      file = list.readline()
      file = '/tftpboot/prod/backup-configs/'+str(file) 
      new = file.rstrip("\n")
      new = new+'-confg'
      print(new)
      time.sleep(1)

      # parse config
      try:
         myfile = open(new,"r")
         data=myfile.read()
         myfile.close()

         config = requests.post("HTTP://beacon.d.aws.a:8008/arista/parser",
               data= data,
               params={'mlag':'1'},
               verify=False,
               )
         if config.status_code == 200:
            config = config.json()
            #pprint(config)
            if 'interface Management1' in config['downlinks'] :
               print(file,' ',config['downlinks']['interface Management1']) 
            else:
               print(file,' ','ERROR No Managment found')
         else:
            print(file,' ','ERROR Parse error')
      except:
         print(file,' ','ERROR No Config')
