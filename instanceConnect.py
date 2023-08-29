#!/usr/bin/python
import paramiko
import time
try:
    k = paramiko.RSAKey.from_private_key_file("transit-VPC-resources.pem")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    ip = "10.3.254.12";
    s.connect(ip, username = "ec2-user", pkey = k )
    c = s.invoke_shell()
    print("connected")
except paramiko.AuthenticationException as e:
    print e
