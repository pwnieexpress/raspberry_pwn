#!/usr/bin/env python

import time
import subprocess
import os
import re
import sys

definepath=os.getcwd()

# define metasploit path
meta_path=file("%s/config/fasttrack_config" % (definepath),"r").readlines()
for line in meta_path:
    line=line.rstrip()
    match=re.search("METASPLOIT_PATH",line)
    if match:
       line=line.replace("METASPLOIT_PATH=","")
       metapath=line

# Define ranges for scanning here
try:
   scanfirst1=sys.argv[4]
except IndexError: 
   if not os.path.isfile("bin/appdata/hostfile"):
	scanfirst1=raw_input("Enter the IP Range to scan for SQL Scan (example 192.168.1.1-255): ")

   if os.path.isfile("bin/appdata/hostfile"):
	hostfile=raw_input("Enter path to the file of ip addresses to scan: ")	

# decide to do advanced identification of sql servers
sqlping=raw_input("""
Do you want to perform advanced SQL server identification on non-standard SQL ports? This will use UDP footprinting in order to determine where the SQL servers are at. This could take quite a long time.

Do you want to perform advanced identification, yes or no: """)
# default to yes
if sqlping == '': sqlping=("yes")
# if no, do regular scan
if sqlping == 'n' or sqlping == 'no': 
   print ("Alright. Moving on...")
   print """There may be a slight delay while scanning... be patient..."""

   if os.path.isfile("bin/appdata/hostfile"):
	scan1=os.system("nmap -sT -v -P0 -p1433 -iL %s > bin/appdata/SqlScan.txt 2> /dev/null" % (hostfile))

   # start scan looking just for 1433
   if not os.path.isfile("bin/appdata/hostfile"):
	   scan1=os.system("nmap -sT -v -P0 -p1433 %s > bin/appdata/SqlScan.txt 2> /dev/null" % (scanfirst1))

   print "\n"
   scanres=os.popen("grep Discovered* bin/appdata/SqlScan.txt").read()
   if not scanres:
      print "\nNo SQL servers were found during scanning...Sorry.\n"
      print "Exiting Fast-Track....\n\n"
      rmold=subprocess.Popen("rm bin/appdata/SqlScan.txt 2>/dev/null", shell=True).wait()
      sys.exit(1)
   # display discovered sql servers
   print "%s" % scanres
   bb=subprocess.Popen('grep "Discovered" bin/appdata/SqlScan.txt | cut -c34-48 > bin/appdata/sqlip.txt', shell=True).wait()
   fileopen=file("bin/appdata/sqlip.txt","r").readlines()
   filewrite=file("bin/appdata/sqlopen.txt","w")
   for line in fileopen:
       # remove line breaks
       line=line.rstrip()
       # append 1433 as port
       line=line+":1433"
       filewrite.write(line)
       filewrite.write("\n")
   filewrite.close()
   time.sleep(2)
# advanced sql footprinting using metasploit aux module
if sqlping == 'y' or sqlping == 'yes':
 try:
   match=re.search("-",scanfirst1)
   if match:
      print ("""Fast-Track currently only supports cidr notations or one IP address at a time.\n\nExample: 192.168.1.1/24 or 192.168.1.35\n\nExiting Fast-Track...""")
      print "\n\nNOTE THE REASON FOR EXITING WAS DUE TO FAST-TRACK ONLY SUPPORTING CIDR NOTATION, PLEASE PUT THE IP ADDR IN A 192.168.1.1/24 LIKE FORMAT\n\n"
      sys.exit()
   # set variables, log paths, fix / in filenames
   print ("\n[-] Launching SQL Ping, this may take a while to footprint.... [-]\n")
   sanitize=scanfirst1.replace(r"/",".cidr.")
   logpath=("%s/bin/logs/" % (definepath))
   filename=("SQLServersUDP%s" % (sanitize))
   launchsqlping=subprocess.Popen(r"""%smsfcli auxiliary/scanner/mssql/mssql_ping THREADS=10 RHOSTS=%s E > %s%s""" % (metapath,scanfirst1,logpath,filename), shell=True).wait()
   parse1=file("bin/logs/%s" % (filename),"r").readlines()
   filewrite=file("bin/appdata/sqlopen.txt","w")
   for line in parse1:
       match1=re.search("SQL Server information for", line)
       # find IP addr from results
       if match1:
          # parse through metasploit output
          ipaddr=line.replace(":","")
          ipaddr=ipaddr.split()
          ipaddr=ipaddr[5]
       # find port from results
       match2=re.search("tcp",line)
       if match2:  
          port=line.split()
          port=port[3]
          ipaddr1=ipaddr+":"+port
          ipaddr1=ipaddr1.rstrip()
          filewrite.write(ipaddr1)
          filewrite.write("\n")  
   filewrite.close()
 except Exception,e:
      print "\nSomething went wrong...Printing error "+e+"\n\n"
