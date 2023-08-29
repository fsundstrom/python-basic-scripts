#!/usr/bin/python3

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
import subprocess
import getopt
import netmiko
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException

# note for python 2.7 pip install netmiko==2.4.2

# defaults (can be in coanfig file...)
URL_api = "/command-api"
host = "test"
user = "admin"
password = "test"

# get command line options
####################################

# Remove 1st argument for program name
argumentList = sys.argv[1:]

options = "p:u:s:c:"
long_options = ["password", "user", "switch", "config"]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ('-p','--password'):
           password = currentValue
        if currentArgument in ('-u','--user'):
           user = currentValue
        if currentArgument in ('-s','--switch'):
           host = currentValue
        if currentArgument in ('-c','--config'):
           config = currentValue

except getopt.error as err:
    print( "input error")
    print( "usage: -p password -u username -s host -c config_file")
    exit()

# is this guy smart and used the options ?
if host == "test":
   print( "usage: -p password -u username -s host -c config_file")
   exit()


# main code to run Arista commnads  
######################################
def main():
#  commands = [
#      "enable",
#      "show running-config"
#     ]
  commands = ['show running']
  result = __run_commands(commands,host,user,password)
  if "ERROR:" in result or  len(result) < 127:
     print ("Error reading config from ",host,result)
     exit()

  newfile = open("/var/tmp/tmpconfig","w")
  write = newfile.write(result) 
  newfile.close()
  
  output = subprocess.run(['diff', "--ignore-space-change", "--minimal", "--ignore-blank-lines", "/var/tmp/tmpconfig", config],stdout=subprocess.PIPE)  
  print ('\n'.join(str(output.stdout).split('\\n')))
 
  
  


##################################################################
##################################################################


# subruteen to run command 
def __run_commands(commands,host,user,passwd):
  
  switch = {'device_type': 'cisco_ios',
                  'host': host,
                  'username': user,  
                  'password': passwd,  
                  'timeout': 25 
                  }

  print (switch)
  
  try: 
     net_connect = ConnectHandler(**switch)

  except NetMikoTimeoutException:
     output = "ERROR: timeout"
     print("SSH timeout ERROR")

  except NetMikoAuthenticationException:
     output = "ERROR: SSH AUTH"
     print("Auth ERROR")

  except:
     output = "ERROR: SSH connect"
     print("connect ERROR")

  else:
     output = net_connect.send_command("enable", expect_string=r'#')
     for command in commands:
        output = net_connect.send_command(command)
     net_connect.disconnect()

  return(output)

#############
# Call MAIN #
#############

# run def main
if __name__ == "__main__":
  # manin env
  main()
