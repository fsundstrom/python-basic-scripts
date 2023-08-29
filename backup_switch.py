#!/usr/bin/env python

# Python script to run commands on devices
# Ver 1.00 
# 
#
# By Frank L. Sundstrom
# f_sundstrom@yahoo.com
#

# load standard modules
from datetime import datetime
import json
import logging
import os
import re
import sys
import threading
import time
import random

# some standard modules were renamed for py3, make sure we get the right ones
try:
    import configparser
    from queue import PriorityQueue
except ImportError:
    import ConfigParser as configparser
    from Queue import PriorityQueue

# load venv modules
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException

#################
# Default vars  #
#####################################################################
device_file = 'devices.lst'
command_file = 'commands.lst'



# setup message queue
q = PriorityQueue()


#############
# Main code #
#####################################################################
#####################################################################

def main():
    logging.info("%s: Started ", str(datetime.now()))

    # Get list of swithces 
    #################################
    myfile = open(device_file,"r")
    myfile2 = open(command_file,"r")
    devices = myfile.read()
    devices = devices.rstrip('\n')
    devices = devices.split('\n')
    print devices
    commands = myfile2.read()
    myfile.close()
    myfile2.close()
    # retrieve info and run commands

    logging.info("%s: running commands for: %s",
    str(datetime.now()), devices)
    results = __run_commands(devices,commands)
    logging.debug("got rsults %s", results)

    for result in results:
        device = result['device'].replace('.net.a.com','')
        if len(result['output']) > 127:
           file = '/tftpboot/prod/backup-configs/'+device+'-confg'
           myfile = open(file,"w")
           result = myfile.write(result['output'])
           myfile.close()
           print file , "Done"
        else:
           print device," ERROR"

################################################
# Private methods, helpers and error handlers  #
#####################################################################
#####################################################################

# Class for multi thread OS call
#########################################################
class CommandSub(threading.Thread):
    # set up session
    def __init__(self, slot, device, commands):
        super(CommandSub, self).__init__()
        self.slot = slot
        self.device = device
        self.commands = commands

    # run OS command and get output
    def run(self):
        # note start time
        thread_start = datetime.utcnow()
        logging.info("%s: thread %s started for %s", str(thread_start), self.ident, self.device)

        #NEt miko stuff
        switch = {'device_type': 'cisco_ios',
                  'host': self.device,
        #######################
        ## user and password ##
        #######################
                  'username': 'Insert_user_name',  # belongs in config.ini
                  'password': 'Insert_password',  # belongs in config.ini
                  'timeout': 25             # belongs in config.ini
                  }

        # connect to device and get command output
        try:
            net_connect = ConnectHandler(**switch)

        except NetMikoTimeoutException:
            print("SSH timeout ERROR",self.device)
            output = "SSH Timout ERROR"
            logging.error("%s: SSH Timeout ERROR: for %s", str(datetime.now()), self.device)

        except NetMikoAuthenticationException:
            print("Auth ERROR",self.device)
            output = "SSH AUTH ERROR"
            logging.error("%s: SSH Auth ERROR: for %s", str(datetime.now()), self.device)

        else:
            output = net_connect.send_command(self.commands)
            net_connect.disconnect()

            logging.debug("Data = %s", output)

            print("got response")

        # note end time
        thread_end = datetime.utcnow()
        logging.info("%s: thread %s done", str(thread_end), self.ident)

        # record the result
        q.put({'thread_id': self.ident,
               'thread_start': thread_start,
               'thread_end': thread_end,
               'slot': self.slot,
               'device': self.device,
               'output': output})

        # terminate the thread
        return


# get count of active CommandSub threads
###########################################
def __active_probes():
    return len(filter(lambda x: isinstance(x, CommandSub),
                      threading.enumerate()))


# map function to process thread results for a single device
##################################################################
def __process_thread_result(thread_result):
    # init tracking vars
    total_macs = 0
    port_detail = {}

    # obtain short device name for logging
    key = str(re.sub(r'\..*', '', thread_result['device']))
    output = thread_result['output']

    # output should be a JSON struct; if it isn't, log errors and abort
    if not isinstance(output, dict):
#        if "ERROR" in output or "FAILED" in output or "denied" in output:
#            print(key, " ERROR no MIB Responce ", output)
#            logging.error("%s: bad response for thread %s device %s",
#                          str(datetime.now()), thread_result['thread_id'], key)
#            logging.debug(output)

        if "UNREACHABLE" in output:
            print(key, " UNREACHABLE ")
            logging.error("%s: UNREACHABLE %s", str(datetime.now()), key)

        if "Authorization denied" in output:
            print(key, " Authorization denied ")
            logging.error("%s: Authorization denied %s",
                          str(datetime.now()), key)

        if "no output" in output:
            print(key, " No Output !")
            logging.error("%s: No Output %s", str(datetime.now()), key)

        return False

    # parse MAC address table
    return (key,output)


# get MAC table on switch via Ansible
#########################################################
def __run_commands(device_names,commands):
    max_threads = 20  # belongs in config.ini
    all_results = []

    # setup collectors
    collectors = [None] * max_threads

    # run collector threads
    while len(device_names) > 0 or __active_probes() > 0 or not q.empty():
        # if there are messages in the queue, retrieve them
        while not q.empty():
            thread_result = q.get_nowait()
            thread_id = thread_result['thread_id']
            logging.debug('Capturing results from thread {}'.format(thread_id))
            all_results.append(thread_result)

        # run up to max_threads concurrent threads until all devices have
        # been probed
        for i in range(max_threads):
            if collectors[i] is None or not collectors[i].is_alive():
                # get the next device name
            
                try: 
                    name = device_names.pop(0)
                    print "run for",name
                    logging.debug('Starting new thread for {} in slot {}'
                                  .format(name, i))
                    collectors[i] = CommandSub(i, name, commands)
                    collectors[i].start()
                # if no device names are left, we're done probing
                except IndexError:
                    break

        # wait for active probes to finish
        active_probe_count = __active_probes()
        if active_probe_count > 0:
            logging.debug('Waiting for {} active device probes to finish'
                          .format(active_probe_count))
            logging.debug(threading.enumerate())
            time.sleep(3)
 
    print "DONE !!!!!"
    logging.debug('Raw thread result: %s', str(all_results))

    # process thread output
    error,result = (__process_thread_result, all_results)

    # return thread output to caller
    return result


#############
# Call MAIN #
#############

# run def main
if __name__ == "__main__":
    global config

    # config.ini lives in the same dir as the main module, so to find
    # config.ini, we first need to find main
    main_mod = sys.modules['__main__'].__file__
    working_dir = main_mod[:main_mod.rfind('/')]

    # load the config
    config = configparser.RawConfigParser()
    config.read(working_dir + '/config.ini')

    # set up logging
    logging.basicConfig(filename=config.get('config', 'LOGFILE'),
                        level=config.get('config', 'LOGLEVEL'))

    # start me up
    main()
