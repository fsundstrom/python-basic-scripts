#!/usr/bin/env python

# Python script to run API commands Arista switfches
# Ver 1.00
#
#
# By Frank L. Sundstrom
# f_sundstrom@yahoo.com
#


import os
import requests
import json
import re
import sys
import getopt
import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# defaults (can be in coanfig file...)
URL_api = "/command-api"
host = "test"
user = "admin"
password = "test"

# get command line options
####################################

# Remove 1st argument for program name
argumentList = sys.argv[1:]

options = "p:u:t:c:"
long_options = ["password", "user", "target", "commandfile"]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ('-p','--password'):
           password = currentValue
        if currentArgument in ('-u','--user'):
           user = currentValue
        if currentArgument in ('-t','--target'):
           host = currentValue
        if currentArgument in ('-c','--commandfile'):
           filename = currentValue

except getopt.error as err:
    print "input error"


# is this guy smart and used the options ?
if host == "test":
   print "usage: -p password -u username -t tagget host -c file_of_commands"
   exit()


# main code to run Arista commnads  
######################################
def main():
  
  file = open(filename,"r")
  data = file.read()
  commands = data.rstrip('\n')
  commands = commands.split('\n')
  print "\nrunning commnads:"
  print commands

  result = __run_commands(commands)
  try: 
   if not result.status_code == 200: 
     print "connect Error !",result.status_code
     exit()
  except:
     print "connect Error !"
     exit()
  print "\n---Result----"
  print result.text


##################################################################
##################################################################


# subruteen to run command 
def __run_commands(commands):
  data = { 
       "jsonrpc": "2.0",
       "method": "runCmds",
       "params": {
         "format": "json",
         "timestamps": False,
         "autoComplete": False,
         "expandAliases": True,
         "cmds": commands, 
         "version": 1
       },
       "id": "EapiExplorer-1"
     }
  url = 'https://'+host+URL_api
  
  try: 
      result = requests.post(
                 url,
                 headers = {'Content-Type': 'application/json'},
                 auth=HTTPBasicAuth(user,password),
                 json = data, 
                 verify=False
                )
  except:
     result = "connect error"

  return(result)

#############
# Call MAIN #
#############

# run def main
if __name__ == "__main__":
  # manin env
  main()
