#!/usr/bin/env python

import sys
import time
import paramiko 
import os
import cmd
import datetime

###set date and time
now = datetime.datetime.now()

###authentication
USER = 'netadmin'
PASSWORD = 'Pa$$word2019'
secret = 'eNableP@ssWord'

###start FOR ...in 
f = open('cisco_routerswitch')
for ip in f.readlines():
	ip = ip.strip()
	###prefix files for backup
	filename_prefix ='/var/netbackup/' + ip
	
	###session start
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip, username=USER, password=PASSWORD)

	###ssh shell
	chan = client.invoke_shell()
	time.sleep(2)
	###enter enable secret
	chan.send('en\n')
	chan.send(secret +'\n')
	time.sleep(1)
	###terminal lenght for no paging 
	chan.send('term len 0\n')
	time.sleep(1)
	###show config and write output
	chan.send('sh run\n')
	time.sleep(30)
	output = chan.recv(999999)
	###show output config and write file with prefix, date and time
	print (output)
	#filename = "%s_%.2i-%.2i-%i_%.2i-%.2i-%.2i" % (filename_prefix,now.day,now.month,now.year,now.hour,now.minute,now.second)
	filename = "%s_%.2i%.2i%i_%.2i%.2i%.2i" % (filename_prefix,now.year,now.month,now.day,now.hour,now.minute,now.second)
	ff = open(filename, 'a')
	#ff.write(output)
	ff.write(output.decode("utf-8") )
	ff.close()
	###close ssh session
	client.close() 
	
	print (ip)
	f.close()
