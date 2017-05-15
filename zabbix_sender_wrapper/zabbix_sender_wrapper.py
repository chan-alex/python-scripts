#!/usr/bin/env python

import sys
import time
import subprocess
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('-z', '--zabbix-server ', dest='zabbix_server',
                    help="Zabbix server host or ip address", required=True)

parser.add_argument('-p', '--port', dest='zabbix_server_port',
                    help="Zabbix server port. default is 11051", default='10051')

parser.add_argument('-s', '--host', dest='host',
                    help="Specify host name as registered in Zabbix frontend. Host IP address and DNS name will not work", required=True)

parser.add_argument('-k', '--key', dest='zabbix_key',
                    help="Zabbix item key", required=True)

parser.add_argument("cmd", nargs=argparse.REMAINDER,
                    help="command to wrap")

args = parser.parse_args()

if len(args.cmd) == 0:
    print "No input cmd given. exiting."
    sys.exit(1)
    
print "Command to wrap is: " + str( args.cmd)
print "Zabbix key is: " + args.zabbix_key
print "Zabbix server is: " + args.zabbix_server
print "Zabbix server port is: " + args.zabbix_server_port
print "Zabbix key is: " + args.zabbix_key

start_time =  time.time()
error_code = subprocess.call(args.cmd)
end_time =  time.time()


elapsed_time = round(end_time - start_time, 2)
start_time_asc =  time.asctime(time.localtime(time.time()))
end_time_asc =  time.asctime(time.localtime(time.time()))


log_message_template = "Cmd: {0}\nStatus: {1} \nStart: {2}\nEnd: {3}\nElapsed: {4} seconds\n"
log_message = log_message_template.format(" ".join(args.cmd), error_code, start_time_asc, end_time_asc, elapsed_time)  

zabbix_sender_cmd = ['/bin/zabbix_sender',
                     '-z', args.zabbix_server,
                     '-p', args.zabbix_server_port,
                     '-s', args.host,
                     '-k', args.zabbix_key,
                     '-o', log_message ]

print zabbix_sender_cmd
error_code = subprocess.call(zabbix_sender_cmd)
